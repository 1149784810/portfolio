# 何健乐 · 个人项目作品集

AI 驱动虚幻引擎游戏开发作品展示。

线上地址：<https://1149784810.github.io/portfolio/>

## 项目

- [UnrealGenAI](index.html) — 基于 Qwen3-32B 持续预训练的游戏布景与资产批量操作项目（已上线）
- RL4RTS — 二战 RTS 游戏强化学习 Bot 训练框架（展示页制作中）
- 瀚航咨询 — 企业咨询大模型微调与数据飞轮平台（展示页制作中）
- 源世界平台 — 视觉小说创作与分发全栈平台（展示页制作中）
- 萤火智创（FireflyMind）— AI 辅助一人创业全流程平台（展示页制作中）
- 战争警戒（WarAlert）— 联机竞技 RTS（展示页制作中）
- 神选者（The Chosen One）— 支持联机的恶魔城（展示页制作中）
- CHD 科创平台 — 长安大学线上赛事交流微信小程序（展示页制作中）
- 冒险岛游戏大厅 — 公司内部网页游戏大厅与 Agent 部署平台（已收录）
- DSH GameMaker 插件 — DeepSeek Harness 游戏开发角色 subagent 与预设（已收录）

## 技术

单页静态站点：HTML + CSS + 原生 JS（无外部依赖），图片资源位于 `assets/`。

页面由 `site_gen.py` 生成（`index.html` + `projects/*.html`），**不要直接改生成的 HTML**，
改 `site_gen.py` 里的 `PROJECTS` 数据后重新生成即可。

---

## 发布流程

### 仓库结构

| 仓库 | 可见性 | 作用 |
| --- | --- | --- |
| `portfolio-src` | 私有 | 源码与数据（`site_gen.py`、`assets/`），**在这里改内容** |
| `portfolio` | 公开 | 线上站点，由 GitHub Pages 直接部署 |

推送 `portfolio` 的 `main` 分支后，GitHub Pages 会自动重新构建并上线，通常 30–60 秒完成。

### 日常更新（推荐）

```bash
# 1. 改 site_gen.py 里的 PROJECTS 数据，或往 assets/ 加图片
# 2. 提交即可，剩下的自动完成：
git add -A
git commit -m "新增 XXX 项目"
```

一次 `git commit` 会自动完成：

1. `pre-commit` 钩子：重新运行 `site_gen.py`，把生成好的 HTML 一起提交
2. `post-commit` 钩子：推送 `portfolio-src` → 同步到 `portfolio` → 触发 Pages 上线

### 手动发布（需要指定信息或重新生成时）

```bash
python publish.py                  # 重新生成 -> 提交 -> 推送 -> 同步 -> 等待上线
python publish.py -m "新增项目"     # 自定义提交信息
python publish.py --sync-only      # 只推送同步，不重新生成、不提交
python publish.py --dry-run        # 只演练，不做任何改动
python publish.py --no-verify      # 不等待 Pages 构建完成
```

### 需要跳过自动流程时

```bash
SKIP_AUTOPUSH=1 git commit -m "临时提交"   # 只提交，不推送不部署
SKIP_SITEGEN=1  git commit -m "只改文档"   # 不重新生成页面
```

之后再手动发布：`python publish.py`

### 说明

- 公开仓库同步的是**已提交**的内容（基于 `git archive HEAD`），
  因此两个仓库的站点内容始终一致，不会把未提交的改动发上线。
- 开发专用文件（`.githooks/`、`.github/`）不会同步到公开仓库。
- 自动发布失败不会阻塞提交，按提示手动运行 `python publish.py` 即可。

## 环境依赖

- Python 3（仅用于生成页面与发布脚本，无第三方库依赖）
- git 凭据：本机已配置 `credential.helper=store`，token 存于 `~/.git-credentials`
