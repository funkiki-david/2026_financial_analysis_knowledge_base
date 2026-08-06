# AI Research Intake Workflow

## Purpose

把零散材料稳定地转成知识库内可用的研究资产。

## Input Types

- 分享链接整理结果
- 临时笔记
- 新闻摘要
- 财报电话会摘要
- 公司初步观察
- 市场复盘草稿

## Standard Flow

1. 判断内容属于正式研究、参考资料还是临时收件。
2. 如果不能立刻分类，先进入 `90_Inbox/incoming/`。
3. 提取标题、日期、主题、来源和内容类型。
4. 使用 `scripts/kb_save.sh` 或 `scripts/kb_capture.sh` 保存到对应目录。
5. 如果内容涉及结论，补齐来源、假设、风险和待验证事项。
6. 在适合的时候，把临时内容转写为模板化正式文档。

## Routing Guide

- 公司研究 -> `04_Company_Notes/Active_Research/<Ticker>/`
- 每日复盘 -> `05_Market_Reviews/Daily/`
- 每周复盘 -> `05_Market_Reviews/Weekly/`
- 方法论 -> `03_Research_Frameworks/`
- 模板 -> `06_Research_Templates/`
- 资料来源 -> `08_Data_and_Sources/references/`
- 未分类 -> `90_Inbox/incoming/`

## Minimum Metadata

- 标题
- 日期
- 内容类型
- 来源
- 当前状态：草稿 / 进行中 / 已整理 / 已归档

## Quality Check

- 是否区分事实、观点和推测？
- 是否保留日期？
- 是否能看出下一步动作？
- 是否能找到原始来源？
