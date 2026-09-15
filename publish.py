# -*- coding: utf-8 -*-
"""作品集一键发布。

    python publish.py                  # 重新生成站点 -> 提交 -> 推送 -> 同步到公开仓库 -> 等待上线
    python publish.py -m "新增项目"     # 自定义提交信息
    python publish.py --sync-only      # 只做推送与同步（不重新生成、不提交源码）
    python publish.py --dry-run        # 只展示将要执行的动作
    python publish.py --no-verify      # 不等待 GitHub Pages 构建完成

流程：
    portfolio-src（私有，源）  --push-->  同步到  portfolio（公开，GitHub Pages 站点）
    公开仓库主分支一有推送，GitHub Pages 会自动重新构建并上线。
"""
import argparse
import datetime
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

try:  # Windows 控制台默认不是 UTF-8，避免中文输出报错
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

SRC_REPO = os.path.dirname(os.path.abspath(__file__))
PUBLIC_REPO = os.path.join(os.path.dirname(SRC_REPO), 'portfolio')
PUBLIC_SLUG = '1149784810/portfolio'
LIVE_URL = 'https://1149784810.github.io/portfolio/'

# 只存在于源码仓库的开发文件，不发布到线上站点
EXCLUDE = {'.git', '.githooks', '.github', '__pycache__'}


def log(msg):
    print(msg, flush=True)


def run(cmd, cwd, check=True, quiet=False):
    """执行命令，出错时抛出带输出的 RuntimeError。"""
    proc = subprocess.run(
        cmd, cwd=cwd, capture_output=True,
        encoding='utf-8', errors='replace',
    )
    if proc.returncode != 0 and check:
        detail = (proc.stdout or '') + (proc.stderr or '')
        raise RuntimeError('%s 执行失败（%s）:\n%s' % (' '.join(cmd), cwd, detail.strip()))
    if not quiet:
        for line in (proc.stdout or '').splitlines():
            if line.strip():
                log('    ' + line)
    return proc


def git(repo, *args, **kwargs):
    return run(['git'] + list(args), cwd=repo, **kwargs)


def git_out(repo, *args):
    proc = subprocess.run(
        ['git'] + list(args), cwd=repo, capture_output=True,
        encoding='utf-8', errors='replace',
    )
    return (proc.stdout or '').strip()


def current_branch(repo):
    return git_out(repo, 'rev-parse', '--abbrev-ref', 'HEAD') or 'main'


def has_changes(repo):
    return bool(git_out(repo, 'status', '--porcelain'))


def commit(repo, message):
    """暂存并提交；没有改动则返回 False。"""
    if not has_changes(repo):
        return False
    git(repo, 'add', '-A', quiet=True)
    git(repo, 'commit', '-m', message, quiet=True)
    return True


def push(repo, dry_run=False):
    branch = current_branch(repo)
    git(repo, 'push', 'origin', branch, *(['--dry-run'] if dry_run else []), quiet=True)
    return branch


def sync_message(repo):
    """取源仓库最新提交信息，作为公开仓库的同步提交信息。"""
    subject = git_out(repo, 'log', '-1', '--pretty=%s')
    return ('同步站点：%s' % subject) if subject else '同步站点'


def mirror(dry_run=False):
    """把源码仓库内容镜像到公开仓库（删除公开仓库中多余的站点文件）。"""
    copied, removed = 0, 0

    # 1) 复制 / 覆盖
    for root, dirs, files in os.walk(SRC_REPO):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        rel = os.path.relpath(root, SRC_REPO)
        dst_dir = PUBLIC_REPO if rel == '.' else os.path.join(PUBLIC_REPO, rel)
        if not dry_run:
            os.makedirs(dst_dir, exist_ok=True)
        for name in files:
            src_file = os.path.join(root, name)
            dst_file = os.path.join(dst_dir, name)
            if os.path.exists(dst_file) and os.path.getsize(dst_file) == os.path.getsize(src_file):
                with open(src_file, 'rb') as f1, open(dst_file, 'rb') as f2:
                    if f1.read() == f2.read():
                        continue  # 内容一致，跳过
            log('    + %s' % os.path.relpath(dst_file, PUBLIC_REPO).replace('\\', '/'))
            if not dry_run:
                shutil.copy2(src_file, dst_file)
            copied += 1

    # 2) 删除公开仓库里已不存在的站点文件
    for root, dirs, files in os.walk(PUBLIC_REPO):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        rel = os.path.relpath(root, PUBLIC_REPO)
        src_dir = SRC_REPO if rel == '.' else os.path.join(SRC_REPO, rel)
        for name in files:
            if not os.path.exists(os.path.join(src_dir, name)):
                stale = os.path.join(root, name)
                log('    - %s' % os.path.relpath(stale, PUBLIC_REPO).replace('\\', '/'))
                if not dry_run:
                    os.remove(stale)
                removed += 1

    return copied, removed


def read_token():
    """从 git 凭据文件读取 GitHub token，仅用于查询 Pages 构建状态。"""
    path = os.path.join(os.path.expanduser('~'), '.git-credentials')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '@github.com' in line and '://' in line:
                    creds = line.split('://', 1)[1].split('@', 1)[0]
                    if ':' in creds:
                        return creds.split(':', 1)[1]
    except OSError:
        pass
    return None


def latest_pages_build(token):
    req = urllib.request.Request(
        'https://api.github.com/repos/%s/pages/builds/latest' % PUBLIC_SLUG,
        headers={'Authorization': 'token %s' % token, 'User-Agent': 'portfolio-publish'},
    )
    try:
        import json
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except (urllib.error.URLError, OSError, ValueError):
        return None


def wait_for_pages(commit_sha, timeout=180):
    """等待 GitHub Pages 构建出本次推送的提交。"""
    token = read_token()
    if not token:
        log('  ℹ 未找到 GitHub 凭据，跳过构建状态检查')
        return None
    log('  … 等待 GitHub Pages 构建上线（最长 %d 秒）' % timeout)
    deadline = time.time() + timeout
    while time.time() < deadline:
        build = latest_pages_build(token)
        if build and build.get('commit') == commit_sha and build.get('status') == 'built':
            log('  ✓ 已上线：%s' % LIVE_URL)
            return True
        time.sleep(6)
    log('  ⚠ 等待超时，稍后访问 %s 查看（构建通常 30-60 秒完成）' % LIVE_URL)
    return False


def main():
    parser = argparse.ArgumentParser(description='作品集一键发布')
    parser.add_argument('-m', '--message', help='源码仓库提交信息')
    parser.add_argument('--sync-only', action='store_true',
                        help='只推送并同步，不重新生成页面、不自动提交源码')
    parser.add_argument('--dry-run', action='store_true', help='只打印将执行的动作')
    parser.add_argument('--no-verify', action='store_true', help='不等待 Pages 构建完成')
    args = parser.parse_args()

    if not os.path.isdir(os.path.join(PUBLIC_REPO, '.git')):
        log('✗ 找不到公开仓库：%s' % PUBLIC_REPO)
        return 1

    # 本次提交会触发 post-commit 钩子；打标记让它跳过，避免重复推送与同步
    os.environ['PORTFOLIO_PUBLISHING'] = '1'

    # 1) 重新生成站点
    if not args.sync_only:
        log('① 生成站点页面')
        run([sys.executable, 'site_gen.py'], cwd=SRC_REPO)
    else:
        log('① 跳过生成（--sync-only）')

    # 2) 提交源码仓库
    stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    message = args.message or ('更新站点 %s' % stamp)
    if not args.sync_only:
        log('② 提交源码仓库')
        if args.dry_run:
            changes = git_out(SRC_REPO, 'status', '--porcelain')
            log('    %s' % (('将提交 %d 项改动' % len(changes.splitlines())) if changes else '无改动'))
        elif commit(SRC_REPO, message):
            log('    ✓ %s' % message)
        else:
            log('    无改动，跳过提交')
    else:
        log('② 跳过源码提交（--sync-only）')

    # 3) 推送源码仓库
    log('③ 推送 portfolio-src')
    if args.dry_run:
        branch = current_branch(SRC_REPO)
        git(SRC_REPO, 'push', 'origin', branch, '--dry-run')
    else:
        branch = push(SRC_REPO)
        log('    ✓ origin/%s' % branch)

    # 4) 同步到公开仓库
    log('④ 同步到 portfolio（公开站点仓库）')
    sync_msg = sync_message(SRC_REPO)
    copied, removed = mirror(dry_run=args.dry_run)
    if args.dry_run:
        log('    （--dry-run：将同步 %d 个文件，删除 %d 个）' % (copied, removed))
    elif commit(PUBLIC_REPO, sync_msg):
        log('    ✓ %s（同步 %d 个文件，删除 %d 个）' % (sync_msg, copied, removed))
    else:
        log('    公开仓库已是最新，无需提交')

    # 5) 推送公开仓库 -> 触发 GitHub Pages
    log('⑤ 推送 portfolio（触发 GitHub Pages 自动部署）')
    if args.dry_run:
        branch = current_branch(PUBLIC_REPO)
        git(PUBLIC_REPO, 'push', 'origin', branch, '--dry-run')
        log('  （--dry-run：未做任何实际推送）')
        return 0
    branch = push(PUBLIC_REPO)
    log('    ✓ origin/%s' % branch)

    # 6) 等待上线
    if not args.no_verify:
        log('⑥ 确认线上部署')
        wait_for_pages(git_out(PUBLIC_REPO, 'rev-parse', 'HEAD'))

    log('\n完成 ✅  站点地址：%s' % LIVE_URL)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except RuntimeError as exc:
        log('\n✗ %s' % exc)
        sys.exit(1)
