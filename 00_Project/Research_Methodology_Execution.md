# Research Methodology Execution

- Version: v1.0
- Status: Active
- Created: 2026-08-06
- Repository: `2026_financial_analysis_knowledge_base`
- Scope: company, industry, macro, event, earnings, valuation, review, and AI-assisted research

> 本文件是项目的研究执行总规范。所有资料接入、研究笔记、AI 工作流和复盘模板，原则上都应遵守本文件。

---

## 1. Mission

建立一套能够长期复用、持续修正、证据可追溯的个人金融研究体系。

本项目不是自动交易系统，也不以输出买卖建议为目标。核心是持续提升：

- 提出研究问题的能力
- 获取和核验一手资料的能力
- 区分事实、观点、假设和市场叙事的能力
- 建立可验证结论的能力
- 记录错误并改进研究流程的能力
- 将零散资料沉淀为长期知识资产的能力

---

## 2. Research Operating Loop

```text
定义研究问题
    ↓
建立资料地图
    ↓
收集一手资料
    ↓
提取事实与数据
    ↓
形成假设与反方证据
    ↓
建立情景与初步结论
    ↓
设置跟踪指标
    ↓
等待新数据或事件
    ↓
复盘结果
    ↓
更新研究与方法论
```

阶段二的目标不是写出一篇看起来完整的报告，而是确认这条流程能够真正跑通并重复使用。

---

## 3. Core Principles

### 3.1 研究优先于预测

研究重点是理解驱动因素、关键变量、市场预期和失效条件，而不是预测每一次价格变化。

### 3.2 一手资料优先

资料优先级：

1. 监管披露和官方文件
2. 公司 Investor Relations
3. 财报、电话会和投资者演示
4. 官方宏观与行业数据
5. 经过验证的数据平台
6. 高质量研究机构与财经媒体
7. 社交媒体、论坛和社区观点

低优先级来源可以用于发现线索，但不能单独支撑重要结论。

### 3.3 事实、观点和假设必须分开

所有重要信息应标记为：

- **Fact**
- **Management Statement**
- **Market View**
- **Research Hypothesis**
- **Inference**
- **Unverified Information**

### 3.4 证据优先于结论

重要结论必须尽量保留：

- 原始来源
- 数据日期
- 关键事实
- 推理过程
- 支持证据
- 反方证据
- 不确定性
- 失效条件

### 3.5 主动寻找反方证据

每项重要研究至少回答：

- 什么事实会证明当前判断错误？
- 当前结论依赖哪些关键假设？
- 是否存在更简单的替代解释？
- 市场共识与当前研究判断有什么差异？

### 3.6 复盘优先于记忆

重要判断必须留下时间戳，记录当时知道什么、判断什么、依据什么，以及后来实际发生了什么。

### 3.7 不无痕覆盖历史判断

重大观点变化应保留 Git 历史，并在文件中说明新增证据和观点变化。

---

## 4. Standard Research Workflow

### Step 1: 定义研究问题

研究必须从问题开始，而不是从收集资料开始。

较好的问题应包含：

- 研究对象
- 时间范围
- 核心变量
- 验证条件

示例：

> 未来 12 至 24 个月，公司收入增长主要由哪些业务驱动，这些驱动是否已经反映在市场预期中？

### Step 2: 建立资料地图

在阅读前先列出所需资料：

- 监管文件
- 公司 IR
- 财务报表
- 行业数据
- 宏观数据
- 竞争对手资料
- 市场观点

### Step 3: 收集最低资料集

公司研究最低资料集：

- 最新 10-K
- 最新 10-Q
- 近期重要 8-K
- 最新财报新闻稿
- 最新投资者演示
- 最新电话会资料
- Proxy Statement（需要时）

宏观研究最低资料集：

- 数据发布机构
- 序列名称与代码
- 最新数据日期
- 发布频率
- 修订规则
- 历史范围

### Step 4: 提取事实

此阶段先不急于形成结论。重点记录：

- 数字和日期
- 同比与环比变化
- 管理层原始陈述
- 业务分部变化
- 资本配置
- 风险披露
- 数据口径

### Step 5: 建立研究假设

```markdown
## Hypothesis

- Hypothesis:
- Supporting Evidence:
- Contradicting Evidence:
- Key Variables:
- Validation Condition:
- Invalidation Condition:
- Confidence: Low / Medium / High
```

### Step 6: 建立情景分析

至少考虑：

- Bull Case
- Base Case
- Bear Case

情景分析应说明变量如何变化，而不是只给出价格目标。

### Step 7: 形成初步结论

结论必须写明：

- 当前判断
- 判断依据
- 判断信心
- 最大不确定性
- 与市场共识的差异
- 后续跟踪指标
- 什么新证据会改变判断

### Step 8: 设置跟踪指标

每个指标尽量标注：

- 数据源
- 更新频率
- 最近更新日期
- 触发重新研究的条件

### Step 9: 复盘

在财报、重大事件或预设日期后回答：

- 哪些事实发生变化？
- 哪些假设得到验证？
- 哪些假设被推翻？
- 哪些变量被遗漏？
- 哪些步骤重复、缺失或价值较低？
- 下一次如何调整？

### Step 10: 更新方法论

如果某个问题重复出现，应更新：

- 研究模板
- 来源规则
- 提问清单
- AI 工作流
- 复盘标准

---

## 5. Evidence Standard

### Tier 1: Primary Sources

- SEC EDGAR
- Company Investor Relations
- Federal Reserve
- BLS
- BEA
- EIA
- 其他官方监管和政府数据

### Tier 2: Structured Data Platforms

- FMP
- Alpha Vantage
- Koyfin
- FinanceCharts
- 其他经过验证的平台

### Tier 3: Research and Media

- 高质量研究机构
- 主流财经媒体
- 专业行业媒体

### Tier 4: Discovery Sources

- 社交媒体
- 博客
- YouTube
- 论坛
- 市场社区

Tier 4 只用于发现线索，不应直接作为核心证据。

正式研究中的重要数字和陈述至少应记录：

- 来源名称
- 文件或数据序列名称
- 日期
- 链接或仓库路径

涉及最新状态的数据必须标注：

- Data As Of
- Last Verified
- Update Frequency

---

## 6. AI Role and Boundaries

### AI 可以执行

- 总结长文
- 提取关键事实与数字
- 对比来源
- 转换为结构化 Markdown
- 生成研究问题
- 整理时间线
- 检查逻辑矛盾
- 提醒遗漏变量
- 生成复盘初稿
- 更新索引和标签

### AI 不应替代

- 最终研究判断
- 原始资料真实性核验
- 无证据的管理层可信度判断
- 证据不足时的确定性结论
- 买卖建议
- 自动交易
- 无痕覆盖历史研究

### AI 输出保存前检查

- 是否注明数据日期
- 是否可以追溯到原始来源
- 是否混淆事实与观点
- 是否存在未经验证的数字
- 是否遗漏反方证据
- 是否使用过度确定的语言
- 是否写明不确定性
- 是否保留人工最终判断

---

## 7. Research Quality Test

判断一套方法能否长期使用，需要同时检查：

### Repeatability

换一家公司、行业或时间后，流程是否仍能使用。

### Traceability

重要结论是否都能找到原始证据和形成时间。

### Efficiency

流程是否减少重复查找和无结构资料堆积。

### Error Diagnosis

复盘后能否区分：

- 数据错误
- 来源错误
- 假设错误
- 推理错误
- 执行错误

### Maintainability

新资料是否知道放在哪里，旧观点是否容易找到，方法变化是否有版本记录。

### Human Usability

最终判断者是项目所有者。流程如果太重、难以坚持或输出无法阅读，就不算可持续。

---

## 8. Required Outputs

每项正式研究至少应覆盖以下功能：

1. `Source_Log.md`
2. `Initial_Research.md`
3. `Research_Questions.md`
4. `Thesis_and_Risks.md`
5. `Tracking_Indicators.md`
6. `Review_Log.md`

第一轮可以合并为较少文件，但不能缺少这些功能。

---

## 9. GitHub and Version Policy

GitHub 是项目唯一正式版本中心。

所有正式方法论、模板、研究结果和复盘记录必须：

- 使用 Markdown
- 保存到本地知识库
- 同步到 GitHub
- 使用明确的 commit message
- 保留版本变化

推荐文件头：

```markdown
- Created:
- Last Updated:
- Data As Of:
- Version:
- Status:
```

重大观点变化不得无痕覆盖，应记录到：

```text
00_Project/Change_Log.md
```

---

## 10. Governance

最终方法论负责人是项目所有者。

AI、数据平台、GitHub skills 和自动化工具只负责：

- 建议
- 对比
- 执行
- 检查
- 记录

以下情况应触发方法论更新：

- 连续两次研究出现同类遗漏
- 某一步骤长期没有实际价值
- 新数据源显著提高证据质量
- 新工具明显改变研究效率
- 复盘发现模板无法解释关键变量

---

## 11. Phase Two Execution Standard

阶段二使用 NVDA 作为第一个样本研究闭环：

1. 收集 SEC 与 NVIDIA IR 一手资料
2. 建立 `NVDA_Source_Log.md`
3. 建立 `NVDA_Initial_Research.md`
4. 写出核心假设和反方证据
5. 定义跟踪指标
6. 在下一次财报或重大事件后复盘
7. 根据结果修改模板和方法论

阶段二完成标准不是“写完一篇报告”，而是证明流程能够：

- 重复使用
- 追溯证据
- 发现错误
- 支持更新
- 为下一次研究节省时间

---

## 12. Non-Goals

本方法论不用于：

- 自动交易
- 高频交易
- 股票推荐
- 收益承诺
- 只依赖技术指标的买卖模型
- 让 AI 替代独立研究判断

---

## 13. Project Statement

本知识库仅用于金融学习、研究训练、资料管理和认知复盘，不构成投资建议、交易建议、法律意见或税务意见。

任何真实资金决策，都应由使用者根据自身目标、风险承受能力和独立研究作出。
