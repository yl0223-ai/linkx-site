# Newsletter 自动化

星连资本前沿洞察邮件发送管线。

## 快速开始

### 1. 配置

```bash
cp config.example.py config.py
# 编辑 config.py，填入阿里云企业邮箱 SMTP 配置
```

### 2. 准备订阅人列表

**方式 A：本地文件（最简单）**
```bash
# 编辑 subscribers/emails.txt，每行一个邮箱
user1@company.com
user2@example.com
```

**方式 B：飞书多维表格**
```python
# 在 config.py 中填入飞书应用凭证
FEISHU_APP_ID = "cli_xxx"
FEISHU_APP_SECRET = "xxx"
FEISHU_TABLE_ID = "tblxxx"
```
飞书多维表格需要有「邮箱」字段。

### 3. 测试

```bash
# 测试模式（不发送）
python send.py --dry-run

# 发送到测试邮箱
python send.py --test your@email.com
```

### 4. 正式发送

```bash
python send.py
```

## 定时发送（GitHub Actions）

已配置每周一早上 9:00（北京时间）自动发送：

1. Settings → Secrets → 添加：
   - `SMTP_USER` = 你的邮箱
   - `SMTP_PASS` = 阿里云授权码
   - `TEST_EMAIL` = 可选，测试收件人

2. 触发方式：
   - **自动**：每周一 GitHub Actions 自动跑
   - **手动**：GitHub Actions 页面 → "Send Newsletter" → Run workflow

## 阿里云企业邮箱 SMTP 配置

```
主机:     smtp.mxmail.aliyun.com
端口:     465 (SSL)
用户名:   你的完整邮箱地址
授权码:  阿里云邮箱后台 → 设置 → 客户端授权码
```

## 飞书多维表格（可选）

如用飞书收集订阅人：

1. 打开[飞书开放平台](https://open.feishu.cn/) → 创建自建应用
2. 权限管理 → 开通 `bitable:app:readonly`
3. 多维表格 → 右上角 → 分享 → 复制链接（链接里有 table_id）
4. 填入 `config.py`

## 文件结构

```
newsletter/
├── send.py              # 主发送脚本
├── config.example.py    # 配置模板（复制为 config.py）
├── config.py             # 实际配置（不提交 git）
├── template.html         # 邮件 HTML 模板
├── subscribers/
│   └── emails.txt        # 订阅人邮箱列表
└── README.md
```

## 常见问题

**Q: 邮件发不出去？**
A: 先 `--dry-run` 测试，检查 SMTP 配置和授权码

**Q: 收件人显示为 BCC 会不会有问题？**
A: 不会，BCC 发送是标准做法，保护收件人隐私

**Q: 能发送附件吗？**
A: 可以，修改 `send.py` 的 `MIMEMultipart` 即可

**Q: 想先预览效果？**
A: `python send.py --test your@email.com` 会把内容发到测试邮箱