# AI Intake Sample

## Scenario

用户给出一段零散内容，比如：

- 一段聊天整理结果
- 一个公司速记
- 一段新闻摘录
- 一段市场观察

## Example Decision

### Input

“今天看到一家半导体公司讨论很热，很多人都在说资本开支会继续上升。我还没看原始资料，只是先记一下。”

### Classification

- 当前状态：未验证
- 最合适目录：`90_Inbox/incoming/`
- 理由：它是线索，不是正式研究结论

### Next Step

1. 先保存到 Inbox
2. 补原始来源
3. 再决定是否转入公司研究或行业研究目录

### Example Save Command

```bash
./scripts/kb_capture.sh --type inbox --title 半导体资本开支线索 --text "今天看到一家半导体公司讨论很热，很多人都在说资本开支会继续上升。我还没看原始资料，只是先记一下。"
```

## Key Rule

AI 帮助整理，不替代验证。线索先收，结论后建。
