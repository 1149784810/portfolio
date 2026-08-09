# -*- coding: utf-8 -*-
"""作品集站点生成器：index.html + projects/*.html
运行：python3 site_gen.py
后续补充图片/修改文本，改 PROJECTS 数据后重新运行即可。
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.join(BASE, 'projects')
os.makedirs(PROJ_DIR, exist_ok=True)

# ───────────────────────── 项目数据 ─────────────────────────
PROJECTS = [
    {
        'id': 'unrealgenai',
        'title': 'UnrealGenAI',
        'subtitle': 'AI 驱动虚幻引擎游戏开发',
        'tagline': 'AI × GAME DEV · AI 驱动游戏开发',
        'chips': [
            ('dot', '进行中 · 2026.06.15 - 至今'),
            ('accent', '项目负责人 + 主程序'),
            ('', 'AI / 游戏开发 / 工具链'),
        ],
        'intro': '基于 Qwen3-32B 持续预训练的游戏布景与资产批量操作项目：让基座模型学会 3D 游戏布景与 UI 蓝图拼接，并通过 SFT 微调使其能够调用自研 Agent 工具，实现虚幻资产的批量操作。',
        'goal': '项目目标：选用 Qwen3-32B 作为基座模型，通过解析虚幻引擎场景与蓝图数据构建语料进行持续预训练，使基座模型学会 3D 游戏布景与 UI 蓝图拼接能力；在此基础上通过 SFT 微调对齐指令语义，使模型能够正确调用自研 agent 暴露的工具，实现虚幻资产的批量操作。',
        'groups': [
            ('训练语料生产管线', [
                '使用 C++ 在 UE 5.7 中实现战斗 / 平台跳跃 / 横版卷轴三套玩法变体（27 个 UCLASS、StateTree 自研 11 个 AI 条件/任务节点、UInterface + AnimNotify 解耦设计），作为场景数据来源与重建验证环境',
                '基于 UE Python Remote Execution 协议（UDP 服务发现 + TCP 命令通道）实现编辑器远程驱动层，沉淀 13 个场景操作命令与「场景分析 → 轨迹重建 → 自动校验」闭环',
                '产出场景轨迹 + 资产仓库 + 风格标注的结构化数据集（5 个场景、最大 2700 条操作）',
            ]),
            ('数据自动采集工具 — DataTracer', [
                '开发 DataTracer（Electron）调度无头 Claude 自动执行采集流程',
                '实现「填表标注（7 个风格 conditioning 字段）→ 自动采集 → 验证入库」全流程，内置 FIFO 串行任务队列、增量日志、严格安全防护',
            ]),
            ('自研多 Agent 工具调用框架 — MatrixEngine', [
                '设计并实现 MatrixEngine（Electron + React + TypeScript + Fastify + Prisma + PostgreSQL）：星型拓扑 4 角色 agent 协作（root 编排 + resource / ue_ops / code 专职执行）',
                '13 个工具（文件操作、正则搜索、远程操作 UE 编辑器、资源生成等），支持 LLM 双协议流式接入（OpenAI / Anthropic）、上下文自动压缩、分级权限审批与破坏性操作确认',
                '后端 JWT + Argon2id + Zod 双端共享校验 + owner-scoping 权限隔离',
            ]),
            ('动态场景生成', [
                '采用第三方 Houdini Agent + Houdini + 虚幻 PCG 流程进行动态场景生成，与训练数据管线衔接',
            ]),
            ('工程实践', [
                'Electron 安全加固（contextIsolation / contextBridge / DPAPI 加密）、UE 命令并发互斥、fail-closed 安全护栏、测试覆盖（Vitest / node:test + c8 ≥80%）',
            ]),
        ],
        'stack': ['Qwen3-32B', '虚幻引擎 5.7', 'C++', 'Python', 'Electron', 'React', 'TypeScript', 'Fastify', 'Prisma', 'PostgreSQL', 'Houdini', 'UE Python Remote Execution'],
        'gallery': [
            ('assets/unrealgenai-3.jpg', '项目截图 3', True),
            ('assets/unrealgenai-1.jpg', '项目截图 1', False),
            ('assets/unrealgenai-2.jpg', '项目截图 2', False),
            ('assets/unrealgenai-4.jpg', '项目截图 4', False),
            ('assets/unrealgenai-5.jpg', '项目截图 5', False),
        ],
    },
    {
        'id': 'rl4rts',
        'title': 'RL4RTS',
        'subtitle': '二战 RTS 游戏强化学习 Bot 训练框架',
        'tagline': 'REINFORCEMENT LEARNING · 强化学习 × 游戏 AI',
        'chips': [
            ('dot', '进行中 · 2026.05.25 - 至今'),
            ('accent', '项目负责人 + 主程序'),
            ('', 'Python / PyTorch / DDP'),
        ],
        'links': [
            ('RL4RTS 训练指标观测', 'https://u937336-a523-5e36e2ef.westc.seetacloud.com:8443'),
        ],
        'intro': '面向二战题材联机竞技 RTS 的强化学习训练框架。最终目标：训练可上线 PvP Bot，按段位生产不同强度、模拟真人，填充排位匹配（当前里程碑：1v1 完整对局击败规则 AI 胜率 ≥60%，且在 2+ 张地图泛化）。路线：百万级录像模仿学习（BC）→ 门禁评测 → KL 锚定 PPO → 自博弈阶梯（League）。',
        'groups': [
            ('C++/Python 桥接层（headless 训练环境）', [
                '基于 pybind11 将游戏战斗核心（BattleCore，50+ 子模块）剥离为 headless 确定性训练环境（CMake 只读引用游戏源码，零 sim-to-real gap）',
                '录像重放器（replay_player）按 Order==Executed+1 定位稀疏输入，动作捕获率 ~2%→接近 100%；输入编码器（input_encoder）重写 29 种 EInputType（修复 8 个编组/技能/移动命令错位 bug）',
                '每决策帧输出 glob(64)+group_summaries(10×14)+card_state(8×88)+commander(40) 特征；C++ 内嵌推理（rl_inference），最终战斗服务器内嵌',
            ]),
            ('数据工程（零人工标注）', [
                '百万级录像库（00-FF 分桶）+ 崩溃弹性调度（进程池崩溃→重建+重试，连崩 3 次隔离）；剔除含 bot 局、按胜负加权采样（赢家 ×1.0/输家 ×0.3）',
                '50 张 CSV 战斗数值表 → pydantic 可演化 schema 生成器（外键/ENUM/克制字段识别、版本哈希防漂移、漂移校验器）',
            ]),
            ('模型架构', [
                '时序 Transformer 统一策略（SeqUnifiedPolicy，~7.9M 参数）：16 决策帧=8s 滑窗 + 相邻帧 delta 差分 + 可学习时间位置编码',
                '语义目标动作空间（换图泛化关键）：主目标=(类型,序号)联合选择头 + 相对偏移（8 方向×3 距离桶）+ 意图，不输出绝对坐标，per-group 10 槽动作头',
                '辅助预测头（VP 曲线/对手下一动作/资源兵力轨迹/终局胜负）+ 动作空间对齐引擎（7 类全局动作）',
            ]),
            ('训练工程', [
                'BC 预训练（DDP 多卡）：acc_at 0.67-0.72/acc_sub 0.75-0.85，门禁评测采用采样解码；KL 锚定 PPO（anchor=BC 冻结副本，β 1.0→0 退火，闭式逐头 KL，价值冻结副本 reward shaping）',
                '自博弈阶梯：opponent_pool + scripted opening bootstrap（开局 90 帧环境级操作）+ 行为侧 logit 增强（采样增强分布、logprob 记原始分布保 PPO ratio 一致）+ 编组指令冷却（6 决策帧）',
            ]),
            ('部署流程', [
                'ONNX 推理导出（export_onnx_seq + 一致性验证）、推理服务器（rl_inference_server + 协议测试）；43 个单测全绿（环境/数据/策略/PPO 全套）',
            ]),
        ],
        'stack': ['Python 3.11', 'PyTorch', 'Gymnasium', 'pydantic', 'uv', 'C++17', 'pybind11', 'CMake/ninja', 'ONNX Runtime', 'DDP 分布式训练（6×RTX 5090）'],
        'gallery': None,
    },
    {
        'id': 'hanhang',
        'title': '瀚航咨询',
        'subtitle': '企业咨询大模型微调与数据飞轮平台（GLM-4-9B）',
        'tagline': 'LLM FINE-TUNING · 大模型微调 × 数据飞轮',
        'chips': [
            ('', '2026.07.15 - 2026.07.30'),
            ('accent', '项目负责人 + 主程序'),
            ('', '企业外包项目'),
        ],
        'links': [
            ('测试服公网访问', 'http://175.24.41.9/'),
        ],
        'intro': '面向企业战略/财务/人力/法务等咨询场景的 AI 咨询顾问平台（企业外包项目）：以 GLM-4-9B 为基座，构建「官网获客 + AI 智能咨询 + 人工修正沉淀 + 模型微调迭代」的数据飞轮闭环，实现「越用越聪明」的私有化咨询模型；已上线腾讯云公网。',
        'groups': [
            ('官网（React）', [
                'React 19 + Vite 7 + Tailwind + shadcn/ui（40+ 组件）官网（首页/服务/案例/关于 + 6 个脱敏真实咨询案例）',
                'AI 智能咨询对话（OpenAI 兼容协议 + SSE 流式逐字输出 + 思考过程透传，无后端自动降级演示模式）、预约/报名表单 + 评分反馈、响应式 + SEO + SPA 路由',
            ]),
            ('数据收集后台（数据飞轮核心）', [
                '三通道采集（AI 问答自动落库 qa_logs、评分反馈回填、公众纠错池）+ 两级权限（审核员/管理员，JWT）',
                'qa_logs 只增不改（原始数据 immutable）、人工修正单独写入 finetune_entries；审核通过导出 Alpaca/JSONL（可选 ChatML-think 包装思考过程），累计 1000 条触发下一轮微调',
                'Dashboard 统计 + CSV 批量导入 + 微调库管理',
            ]),
            ('GLM-4-9B 微调管线（SFT）', [
                '语料五步管线：自动提取问答对 → CoT 思维链生成 → LLM 重写增强 → 清洗去重 + 人设越狱负样本 → 多格式导出（Alpaca/ChatML/阿里百炼）',
                '训练方案：Unsloth（提速 2 倍、显存减半）+ GLM-4-9B-Chat 4bit + LoRA（r=64, alpha=128），3000-8000 条指令对，max_seq_length 4096',
                '先智谱云端验证，后本地 vLLM 私有化部署（OpenAI 兼容 + 合并权重导出）',
            ]),
            ('部署与运维（腾讯云）', [
                '单 80 端口 Nginx：官网静态 + /admin/ 后台 + /api/ 反代；rsync 一键部署 + PM2 守护 + SQLite；官网/后台/API 公网在线',
            ]),
        ],
        'extra': [
            ('技术难点与解决', [
                '原始数据不可变 vs 人工修正（只增不改 + 修正单独写库，训练数据可追溯不污染）',
                'SFT 数据稀缺（五步管线放大语料质量而非堆量）',
            ]),
        ],
        'stack': ['React 19', 'Vite 7', 'Tailwind 3.4', 'shadcn/ui', 'Node.js', 'Express', 'TypeScript', 'SQLite', 'JWT', 'GLM-4-9B-Chat', 'Unsloth', 'LoRA', 'TRL', 'vLLM', 'Nginx', 'PM2', '腾讯云'],
        'gallery': None,
    },
    {
        'id': 'yuan',
        'title': '源世界平台',
        'subtitle': '视觉小说创作与分发全栈平台',
        'tagline': 'FULL-STACK PLATFORM · 视觉小说创作与分发',
        'chips': [
            ('', '2026.04.15 - 2026.05.30'),
            ('accent', '项目负责人 + 主程序'),
            ('', 'React / FastAPI / AI 生成'),
        ],
        'intro': '专注视觉小说（galgame）创作与分发的平台：为创作者提供低门槛的 AI 辅助创作工具，为读者提供内容市场（一次性购买 + 按章节订阅），含社区互动、钱包积分、支付结算、创作者收益、管理后台等完整商业闭环。',
        'groups': [
            ('后端服务（FastAPI 模块化架构）', [
                'FastAPI 模块化后端 35+ 路由模块（认证/项目/剧情/章节/支付/订单/创作者收益/社区/搜索/存储/发布/审核/后台统计）+ 商业系统（支付 Provider 抽象、订阅与买断、积分体系、创作者分成、审计日志）',
                'AI 生成管线接入 ComfyUI + Seedream/MiniMax/火山引擎/Holopix（文生图/图生图/语音），统一 client 抽象 + 任务队列 + 成本与 token 统计；AI 对话 Agent（agent_chat）多轮助手',
            ]),
            ('Web 端视觉小说游戏框架', [
                '自研互动叙事运行时（逐字显示、多角色立绘 + 表情切换、背景淡入淡出、BGM/音效独立控制）',
                '≥10 档存档（读档完全恢复）+ 成就系统 + 故事回看 + 用户编辑（实时预览、资源替换 100% 生效）；WebGAL 打包器',
            ]),
            ('前端与工程配套', [
                '剧情流程图编辑器（@xyflow/react + dagre）；React 组件体系（shadcn/ui + Ant Design 管理端）+ MetaGPT Web SDK AI 助手；市场端（分类/热度/评分筛选、购买/订阅、个人中心）',
                'test_framework 自动化测试 + Playwright 视觉回归（全功能入口覆盖）+ 跨浏览器兼容（Chrome/Firefox/Safari/Edge 验证）；demo/tutorial 站点；AI 辅助开发流程（CLAUDE.md 规则、索引优先工作流、完成性 Review）',
            ]),
        ],
        'stack': ['Python FastAPI', 'Pydantic', 'SQLite', 'React 18', 'Vite', 'TypeScript', 'Ant Design', 'shadcn/ui', 'Tailwind', 'React Query', '@xyflow/react', 'ComfyUI', 'Seedream', 'MiniMax', '火山引擎', 'WebGAL', 'Playwright'],
        'gallery': None,
    },
    {
        'id': 'yinghuo',
        'title': '萤火智创（FireflyMind）',
        'subtitle': 'AI 辅助一人创业全流程平台',
        'tagline': 'AI PRODUCT · 一人公司的 AI 总工程师',
        'chips': [
            ('', '2026.05.10 - 2026.05.30'),
            ('accent', '项目负责人 + 主程序'),
            ('', 'Next.js / NestJS / AI Agent'),
        ],
        'intro': '「一人公司的 AI 总工程师」：用户输入一句话想法，经历头脑风暴 → 市场调研 → 二次调整 → 产品研发四个强制分阶段（每阶段依赖前一阶段产出，但可随时跳过并补做），AI 产品经理角色贯穿全程主动提问与建议，商业画布自动生成并随阶段更新；所有操作消耗积分（初始免费额度可完成首个项目至 MVP）；研发阶段由沙箱 Agent 生成代码，关键检查点需用户审批。',
        'groups': [
            ('全栈 monorepo 架构（pnpm + Turborepo）', [
                'apps/web（Next.js 14，auth/main/admin 路由隔离，六页签导航 + developmentUnlocked 研发门控）',
                'apps/api（NestJS 10，12 个业务模块，Prisma 5 + PostgreSQL 16 模型，Redis session，BullMQ）；packages/shared 类型契约包（ApiResponse 信封 + 全实体 DTO，前后端单一事实来源）',
            ]),
            ('四阶段产品流程引擎', [
                'phase-gated 布尔门控推进 + 头脑风暴子阶段状态机（自由讨论→市场调研→冲突消解→完成）',
                '文档版本化（ProjectDocument 按阶段记录，商业画布自动生成并随阶段更新）；模块级 TDD 研发管线（design→test_generation→implementation→verification→regression 五步）',
            ]),
            ('AI Agent 与积分经济', [
                'AgentEvent 事件协议（progress/ask/finish/error + ask 人机确认，SSE 实时传输）；积分两阶段预扣费（pre_deduct→settle_refund/settle_extra）',
                '每项目独立 K8s Namespace + 沙箱预览 + Agent Job Pod 即用即毁 + BullMQ + WebSocket 日志；改造 Claude Code CLI 实现 Remote Control bridge（可分享 URL 远程查看/审批，密钥 8 类正则脱敏，fail-closed）',
            ]),
            ('前端体验（Phase A）', [
                'Tailwind 品牌色系 + Radix UI + Lucide + TipTap + Monaco + ECharts',
            ]),
        ],
        'stack': ['Next.js 14', 'React 18', 'Tailwind', 'Radix UI', 'TipTap', 'Monaco', 'ECharts', 'NestJS 10', 'Prisma 5', 'PostgreSQL（pgvector）', 'Redis', 'BullMQ', 'TypeScript', 'pnpm', 'Turborepo', 'Vitest / Jest / Playwright'],
        'gallery': None,
    },
    {
        'id': 'waralert',
        'title': '战争警戒（WarAlert）',
        'subtitle': '联机竞技 RTS · 移动端 / PC 端',
        'tagline': 'REAL-TIME STRATEGY · 联机竞技 RTS',
        'chips': [
            ('', '移动端 2022.07.16 - 2024.08.25 ｜ PC端 2025.07.10 - 2026.02.10'),
            ('accent', '项目核心负责人之一'),
            ('', '虚幻引擎 / C++ / 帧同步'),
        ],
        'links': [
            ('移动端游戏主页（B站）', 'https://space.bilibili.com/3546679032678620'),
            ('PC端游戏主页（B站）', 'https://space.bilibili.com/3546938527975850'),
        ],
        'intro': '从项目立项初期参与开发、持续到上线稳定运营的联机竞技 RTS。作为项目核心负责人之一，几乎参与了项目的每个部分：表现层、逻辑层、服务器、图形材质，并带队完成移动端与 PC 端的性能优化。',
        'groups': [
            ('移动端（2022.07.16 - 2024.08.25）', [
                '负责表现层、逻辑层、服务器、图形材质等多条业务线的设计与实现',
                '参与搭建并完善战斗层原生 C++ 帧同步框架：固定步长逻辑帧 + 输入指令队列驱动，配合定点数计算保证多端对战的一致性与确定性',
                '负责项目早期的移动端打包流程与 SDK 接入',
                '使用 KDTree 重构底层碰撞查询，显著降低大规模单位同屏下的查询开销',
                '参考虚幻 GAS 在逻辑层实现技能系统，技能行为与数值效果分层设计，支持策划配置扩展',
                '实现战斗 UI 系统、录像观战系统以及各类外围活动系统（客户端与服务器双端，覆盖大厅、匹配、活动等）',
                '开发一套完整的教程关卡编辑器，策划通过拖拽即可编排教学流程，显著降低教程关卡制作成本',
                '实现各类项目优化工具与资产管理系统，将移动端包体由 4.7G 优化到 1.2G',
                '通过 AnimProxy 优化虚幻动画多线程计算、全面检查优化材质复杂度、降低动画和骨骼的计算复杂度、简化逻辑帧计算复杂度，实现 RTS 游戏在移动端中高画质下 60FPS 畅玩',
                '使用 C# 与 WPF 开发可视化压力测试工具，模拟大量玩家并发进入大厅与匹配战斗，在项目测试前完成服务器压力测试',
                '解决线上 iOS 系统视频无法播放的问题和内存泄露触发 OOM 导致游戏崩溃的问题',
            ]),
            ('PC端（2025.07.10 - 2026.02.10）', [
                '协助团队将移动端由虚幻 4 升级迁移至虚幻 5，处理引擎升级带来的代码、资源与插件兼容问题',
                '成立游戏优化组，带领团队成员开展 GPU 渲染（DrawCall、材质与着色器复杂度）与游戏线程（动画、逻辑帧）的性能优化',
                '在公司内部开设技术课堂，系统性加速新人程序员熟悉项目架构与开发流程',
                '为研发组提供技术支持，包括丧尸模式的顶点动画以及 ECS 相关框架的研究',
            ]),
        ],
        'stack': ['虚幻引擎（UE4/UE5）', 'C++', 'C#', '帧同步', 'GAS 技能系统', 'KDTree', 'AnimProxy', 'WPF 压测工具', 'SDK 接入', 'UE5 移植', 'DrawCall 优化'],
        'gallery': None,
    },
    {
        'id': 'shenxuan',
        'title': '神选者（The Chosen One）',
        'subtitle': '支持联机的恶魔城',
        'tagline': 'INDIE GAME · 独立游戏开发',
        'chips': [
            ('', '2023.09.10 - 2026.01.10'),
            ('accent', '项目负责人 + 主程序'),
            ('', 'Unity / C#'),
        ],
        'links': [
            ('游戏视频（B站）', 'https://space.bilibili.com/433695963'),
        ],
        'intro': '与朋友合作开发的联机动作恶魔城游戏（朋友负责像素美术，本人负责客户端和服务器程序），采用 Unity 开发，支持多人联机对战。',
        'groups': [
            ('核心工作', [
                '采用类似状态帧同步的设计，实现死亡回溯等效果，并具备状态同步的数据快照特性，加入其他玩家世界时可瞬间加载',
                '支持多人联机、死亡回溯与技能系统的完整战斗循环',
                '实现一套基于 Timeline 的复杂动作系统和技能系统，支持特定帧拥有状态 Buff 或产生碰撞体造成伤害，导出数据支持客户端预测和服务器逻辑计算',
                '使用 C# 原生实现一套可以双端运行的行为树 AI 框架，支持对怪物行为进行复杂配置',
            ]),
        ],
        'stack': ['Unity', 'C#', '状态帧同步', 'Timeline 动作系统', '行为树 AI'],
        'gallery': None,
    },
    {
        'id': 'chd',
        'title': 'CHD 科创平台',
        'subtitle': '长安大学线上赛事交流微信小程序',
        'tagline': 'CAMPUS PROJECT · 校园项目',
        'chips': [
            ('', '2018.09.01 - 2022.06.22（大学期间）'),
            ('accent', '项目负责人 + 主程序'),
            ('', '微信小程序 / 20000+ 注册用户'),
        ],
        'links': [
            ('学校官方报道', 'https://webplus.chd.edu.cn/_s179/2021/0518/c9351a193006/page.psp'),
        ],
        'intro': '为长安大学设计的线上赛事交流平台，已上架微信平台，校内注册用户 20000+，解决科创活动中队友难组、项目难找等问题。',
        'groups': [
            ('核心工作', [
                '线上赛事交流平台，可在后台内容管理网站实时查看数据',
                '带领学弟组成学习小组进行前端后端技术学习，并完成平台从 0 到 1 的开发与上线',
            ]),
        ],
        'stack': ['JavaScript', 'Java', '腾讯云开发', '微信小程序'],
        'gallery': None,
    },
]

# ───────────────────────── 页面模板 ─────────────────────────
LIGHTBOX_JS = """
<script>
(function () {
  var figures = Array.prototype.slice.call(document.querySelectorAll('.gallery figure'));
  var srcs = figures.map(function (f) { return f.getAttribute('data-src'); });
  var lb = document.getElementById('lightbox');
  var img = document.getElementById('lbImg');
  var idx = 0;
  if (!lb || srcs.length === 0) return;
  function open(i) {
    idx = (i + srcs.length) % srcs.length;
    img.src = srcs[idx];
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function close() { lb.classList.remove('open'); document.body.style.overflow = ''; }
  figures.forEach(function (f, i) { f.addEventListener('click', function () { open(i); }); });
  document.getElementById('lbClose').addEventListener('click', close);
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.getElementById('lbPrev').addEventListener('click', function (e) { e.stopPropagation(); open(idx - 1); });
  document.getElementById('lbNext').addEventListener('click', function (e) { e.stopPropagation(); open(idx + 1); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') open(idx - 1);
    if (e.key === 'ArrowRight') open(idx + 1);
  });
})();
</script>
"""


def chips_html(chips):
    out = []
    for kind, text in chips:
        if kind == 'dot':
            out.append('<span class="chip"><span class="dot"></span>%s</span>' % text)
        elif kind == 'accent':
            out.append('<span class="chip accent">%s</span>' % text)
        else:
            out.append('<span class="chip">%s</span>' % text)
    return '\n        '.join(out)


def groups_html(groups):
    cards = []
    for idx, (name, subs) in enumerate(groups, 1):
        lis = '\n'.join('          <li>%s</li>' % s for s in subs)
        cards.append(
            '      <div class="work-item">\n'
            '        <div class="work-num">%02d</div>\n'
            '        <div class="work-body">\n'
            '          <h3>%s</h3>\n'
            '          <ul>\n%s\n          </ul>\n'
            '        </div>\n'
            '      </div>' % (idx, name, lis)
        )
    return '\n'.join(cards)


def stack_html(stack):
    return '\n        '.join('<span>%s</span>' % t for t in stack)


def project_page(p):
    sections = []
    # 链接
    if p.get('links'):
        links = '\n'.join(
            '        <div class="link-item"><a href="%s" target="_blank" rel="noopener">%s</a></div>' % (u, n)
            for n, u in p['links'])
        sections.append(
            '  <section id="links">\n    <div class="wrap">\n      <h2>链接</h2>\n'
            '      <div class="link-list">\n%s\n      </div>\n    </div>\n  </section>' % links)
    # 简介
    intro = p.get('intro', '')
    goal = p.get('goal')
    if goal:
        intro += '\n      </p>\n      <p class="intro-text" style="margin-top:14px">' + goal
    if intro:
        sections.append(
            '  <section id="intro">\n    <div class="wrap">\n      <h2>项目简介</h2>\n'
            '      <p class="intro-text">%s</p>\n    </div>\n  </section>' % intro)
    # 截图（紧跟项目简介；无图项目不显示该板块）
    if p.get('gallery'):
        figs = []
        for src, cap, wide in p['gallery']:
            cls = ' class="wide"' if wide else ''
            href = '../' + src
            figs.append(
                '        <figure%s data-src="%s">\n          <img src="%s" alt="%s" loading="lazy">\n'
                '          <figcaption>%s</figcaption>\n        </figure>' % (cls, href, href, cap, cap))
        gallery = '\n'.join(figs)
        sections.append(
            '  <section id="screenshots">\n    <div class="wrap">\n      <h2>项目截图</h2>\n'
            '      <div class="gallery">\n%s\n      </div>\n    </div>\n  </section>' % gallery)
    # 核心工作
    work = []
    if p.get('groups'):
        work.append(groups_html(p['groups']))
    if p.get('extra'):
        work.append(groups_html(p['extra']))
    if work:
        sections.append(
            '  <section id="work">\n    <div class="wrap">\n      <h2>核心工作</h2>\n'
            '      <div class="work-list">\n%s\n      </div>\n    </div>\n  </section>' % '\n'.join(work))
    # 技术栈
    sections.append(
        '  <section id="stack">\n    <div class="wrap">\n      <h2>技术栈</h2>\n'
        '      <div class="stack">\n%s\n      </div>\n    </div>\n  </section>' % stack_html(p['stack']))

    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s — %s</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>

<nav class="topnav">
  <div class="wrap">
    <a href="../index.html">← 返回项目列表</a>
    <span class="site">何健乐 · 个人项目作品集</span>
  </div>
</nav>

<header class="hero hero-sm">
  <div class="wrap">
    <div class="tagline">%s</div>
    <h1>%s<span class="grad"> · %s</span></h1>
    <div class="meta-row">
      %s
    </div>
  </div>
</header>

<main>
%s
</main>

<footer>
  <div class="wrap">何健乐 · 个人项目作品集</div>
</footer>

<div class="lightbox" id="lightbox">
  <span class="close" id="lbClose">×</span>
  <span class="nav prev" id="lbPrev">‹</span>
  <img id="lbImg" src="" alt="预览">
  <span class="nav next" id="lbNext">›</span>
</div>
%s
</body>
</html>
''' % (p['title'], p['subtitle'], p['intro'][:60], p['tagline'], p['title'], p['subtitle'],
       chips_html(p['chips']), '\n'.join(sections), LIGHTBOX_JS)


def index_page():
    cards = []
    for p in PROJECTS:
        cards.append(
            '        <a class="proj-card" href="projects/%s.html">\n'
            '          <div class="proj-name">%s</div>\n'
            '          <div class="proj-desc">%s</div>\n'
            '          <div class="proj-tag">查看详情 →</div>\n'
            '        </a>' % (p['id'], p['title'], p['subtitle']))
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>何健乐项目作品集</title>
<meta name="description" content="AI 驱动游戏开发与全栈项目作品展示">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<header class="hero">
  <div class="wrap">
    <div class="tagline">PERSONAL PORTFOLIO</div>
    <h1>何健乐<span class="grad"> 项目作品集</span></h1>
    <p class="sub">
      AI 驱动游戏开发与全栈项目作品展示：大模型微调、强化学习、虚幻引擎、Web 全栈……
      个人项目持续更新中。
    </p>
    <div class="meta-row">
      <span class="chip"><span class="dot"></span>持续更新中</span>
      <span class="chip accent">个人项目</span>
      <span class="chip">AI × 游戏开发 × 全栈</span>
    </div>
  </div>
</header>

<main>
  <section id="projects">
    <div class="wrap">
      <h2>项目列表</h2>
      <p class="sec-desc">点击项目卡片查看详情（各项目截图持续补充中）</p>
      <div class="proj-grid">
%s
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">何健乐 · 个人项目作品集</div>
</footer>

</body>
</html>
''' % '\n'.join(cards)


# ───────────────────────── 生成 ─────────────────────────
index = index_page()
with open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index)
print('index.html OK')

for p in PROJECTS:
    html = project_page(p)
    with open(os.path.join(PROJ_DIR, p['id'] + '.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('projects/%s.html OK' % p['id'])
