# Inbox Workflow

## Purpose

`90_Inbox/` 用来接住所有还没分类、还没验证、还没整理的内容。

## Folder Roles

- `90_Inbox/incoming/`：新进来的临时内容
- `90_Inbox/processed/`：已经转写或归档完的原始草稿

## Recommended Flow

1. 先把零散内容放进 `incoming`
2. 判断它属于线索、正式研究、复盘还是资料来源
3. 用 `scripts/kb_promote.sh` 转入正式目录
4. 原始草稿自动移到 `processed`
5. 在正式文档中补齐来源、假设、风险和下一步动作

## Example

```bash
cd "/Users/davidz/2026 金融分析知识库"
./scripts/kb_promote.sh \
  --from "90_Inbox/incoming/2026-08-06_半导体资本开支线索.md" \
  --type company \
  --subdir NVDA \
  --title NVDA_Capex_Lead
```

## Rule

如果内容还只是模糊线索，不要直接当作正式结论写入研究文件。
