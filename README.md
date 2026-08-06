# 2026 金融分析知识库

这是一个本地优先、GitHub 同步的金融研究与知识管理工作区。

目标不是搭一个自动交易系统，而是建立一套可长期迭代的研究体系：能持续积累基础知识、研究框架、公司观察、市场复盘和 AI 辅助工作流，并且把这些内容稳定地沉淀到一个结构清晰的知识库里。

当前工作区从 `preview.md` 中提炼出标准目录结构，并补充了安全的文件保存方案，目标是让以后生成的 Markdown、数据文件和研究记录都能稳定落到固定位置，同时避免覆盖已有文件。

## 快速导航

- 项目索引：`00_Project/Project_Index.md`
- 快速上手：`00_Project/Quick_Start.md`
- 目录说明：`00_Project/Directory_Map.md`
- Inbox 流程：`00_Project/Inbox_Workflow.md`
- GitHub 工作流：`00_Project/GitHub_Workflow.md`

## 当前状态

- 现有文件 `preview.md` 已保留，未改名、未覆盖。
- 本目录已于 2026-08-06 初始化为本地 Git 仓库，并已同步到 GitHub。
- GitHub 仓库：`funkiki-david/2026_financial_analysis_knowledge_base`
- 当前默认分支：`main`
- 自动保存脚本：`scripts/kb_save.sh`
- 快速归档脚本：`scripts/kb_capture.sh`
- 收件区转正式目录脚本：`scripts/kb_promote.sh`
- 路由配置：`config/kb.env`
- 默认时区：`America/Los_Angeles`
- 当前固定工作日期：`2026-08-06`

## 推荐使用方式

以后不管是你手动整理内容，还是我继续在本地帮你生成项目文件，都优先通过保存脚本写入：

```bash
./scripts/kb_save.sh --type company --title NVDA_Initial_Research --ext md <<'EOF'
# NVDA 初始研究

- 研究日期：2026-08-06
- 状态：进行中
EOF
```

脚本会自动：

1. 按 `type` 路由到正确目录。
2. 自动创建子目录。
3. 生成安全文件名。
4. 如果目标文件已存在，自动追加序号，不覆盖旧文件。
5. 把每次保存记录写入 `logs/save.log`。

如果一份内容已经先进了 Inbox，后面确认分类后可以这样转入正式目录：

```bash
./scripts/kb_promote.sh --from "90_Inbox/incoming/2026-08-06_某条线索.md" --type company --subdir NVDA --title NVDA_Follow_Up
```

这个过程会：

1. 在正式目录中生成一个非覆盖式新文件。
2. 把原草稿移动到 `90_Inbox/processed/`。

如果你想直接把剪贴板里的内容收进知识库，可以用：

```bash
./scripts/kb_capture.sh --type inbox --title 刚复制的研究片段 --clipboard
```

这个脚本会优先读取你指定的来源；如果你没传来源，它会先尝试读取剪贴板，剪贴板为空时再读取终端输入。

## 目录说明

```text
2026 金融分析知识库/
├── README.md
├── preview.md
├── 00_Project/
├── 01_Financial_Foundations/
├── 02_Market_Structure/
├── 03_Research_Frameworks/
├── 04_Company_Notes/
├── 05_Market_Reviews/
├── 06_Research_Templates/
├── 07_AI_Workflows/
├── 08_Data_and_Sources/
├── 09_Learning_Log/
├── 10_Glossary/
├── 90_Inbox/
├── config/
├── scripts/
└── logs/
```

主要用途如下：

- `00_Project/`：项目目标、规则、变更记录、说明文档
- `01_Financial_Foundations/`：金融基础知识沉淀
- `02_Market_Structure/`：市场结构与微观机制
- `03_Research_Frameworks/`：研究框架与方法论
- `04_Company_Notes/`：公司观察、深度研究、归档记录
- `05_Market_Reviews/`：日周月年复盘
- `06_Research_Templates/`：模板
- `07_AI_Workflows/`：提示词、工作流、自动化想法
- `08_Data_and_Sources/`：原始数据、处理后数据、参考资料
- `09_Learning_Log/`：问题、复盘、学习记录
- `10_Glossary/`：术语表
- `90_Inbox/`：尚未分类的临时输入

备注：

- 某些当前还没有正式内容的目录里放了 `.gitkeep` 占位文件，只是为了让 Git 保留目录结构。

## 常用类型映射

脚本内置了下面这些路由：

- `project` -> `00_Project/docs`
- `foundation` -> `01_Financial_Foundations`
- `market` -> `02_Market_Structure`
- `framework` -> `03_Research_Frameworks`
- `company` -> `04_Company_Notes/Active_Research`
- `watchlist` -> `04_Company_Notes/Watchlist`
- `review-daily` -> `05_Market_Reviews/Daily`
- `review-weekly` -> `05_Market_Reviews/Weekly`
- `review-monthly` -> `05_Market_Reviews/Monthly`
- `review-annual` -> `05_Market_Reviews/Annual`
- `template` -> `06_Research_Templates`
- `ai-workflow` -> `07_AI_Workflows/Research_Workflows`
- `prompt` -> `07_AI_Workflows/Prompt_Library`
- `source` -> `08_Data_and_Sources/references`
- `data-raw` -> `08_Data_and_Sources/raw_data`
- `data-processed` -> `08_Data_and_Sources/processed_data`
- `learning` -> `09_Learning_Log`
- `glossary` -> `10_Glossary`
- `inbox` -> `90_Inbox/incoming`

如需更细分类，可继续传 `--subdir`。

## 典型示例

保存到公司研究目录：

```bash
./scripts/kb_save.sh --type company --subdir NVDA --title Initial_Research --ext md --from /path/to/draft.md
```

保存到每周复盘目录：

```bash
./scripts/kb_save.sh --type review-weekly --title Week_32_Review --content "本周主要观察..."
```

把刚复制的网页摘要直接收进收件区：

```bash
./scripts/kb_capture.sh --type inbox --title FOMC_Notes --clipboard
```

先放进收件区，再人工整理：

```bash
./scripts/kb_save.sh --type inbox --title Broker_Notes --ext txt < notes.txt
```

## Git 使用建议

当前已经连接到 GitHub 远程仓库：

```text
https://github.com/funkiki-david/2026_financial_analysis_knowledge_base
```

以后可以继续使用：

```bash
git status
git add .
git commit -m "docs: update financial research knowledge base"
git push
```

如果后面你要继续细化 GitHub 协作流程，可以优先查看：

- `CONTRIBUTING.md`
- `00_Project/GitHub_Workflow.md`
- `.github/ISSUE_TEMPLATE/`
