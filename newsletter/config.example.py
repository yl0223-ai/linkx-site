# 邮件发送配置
# 复制此文件为 config.py 并填入真实值

# ── SMTP 配置（阿里云企业邮箱）───────────────
SMTP_HOST = "smtp.mxmail.aliyun.com"
SMTP_PORT = 465           # SSL
SMTP_USER = ""            # 发件邮箱，如 newsletter@yourcompany.com
SMTP_PASS = ""            # 授权码（不是登录密码）

FROM_NAME = "星连资本 LINK-X Capital"
FROM_EMAIL = SMTP_USER

# ── 飞书多维表格（可选）──────────────────────
# 如不用飞书，直接在 subscribers/ 放 emails.txt
FEISHU_APP_ID = ""
FEISHU_APP_SECRET = ""
FEISHU_TABLE_ID = ""

# ── 发送控制 ─────────────────────────────────
BATCH_SIZE = 50           # 每批发送多少封
DRY_RUN = False           # True = 只打印，不发信（测试用）
TEST_EMAIL = ""           # 测试邮箱，比如 "your@company.com"

# ── 内容源 ──────────────────────────────────
SITE_DIR = "../linkx-site"  # linkx-site 仓库路径（相对或绝对）
TOP_N_ARTICLES = 5         # 每次发送几篇最新文章