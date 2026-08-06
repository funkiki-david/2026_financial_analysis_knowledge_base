# Quick Start

## 以后最常用的两种方式

### 1. 正式保存到指定目录

```bash
cd "/Users/davidz/2026 金融分析知识库"
./scripts/kb_save.sh --type company --subdir NVDA --title 初始研究 --content "这里写研究内容"
```

### 2. 直接把剪贴板内容归档

```bash
cd "/Users/davidz/2026 金融分析知识库"
./scripts/kb_capture.sh --type inbox --title 刚复制的内容 --clipboard
```

## 推荐工作流

1. 临时材料先进 `90_Inbox/incoming/`
2. 整理后再转入正式目录
3. 重要内容定期提交到 Git

## 常见类型

- `company`：公司研究
- `watchlist`：观察名单
- `review-daily`：每日复盘
- `review-weekly`：每周复盘
- `framework`：研究框架
- `template`：模板
- `source`：资料来源
- `learning`：学习记录
- `inbox`：临时收件区
