#!/usr/bin/env python3
"""
LINK-X Capital Newsletter 发送脚本

用法:
    python send.py                    # 读取 config.py 并发送
    python send.py --dry-run          # 测试模式，不发信
    python send.py --test your@email.com  # 发到测试邮箱

前置条件:
    1. cp config.example.py config.py 并填入配置
    2. 准备好 subscribers/ 目录（放 emails.txt 或配置飞书）
"""

import os, sys, smtplib, ssl, re, argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

# ── 加载配置 ─────────────────────────────────────────────

CONFIG_PATH = Path(__file__).parent / "config.py"
if not CONFIG_PATH.exists():
    print("❌ 找不到 config.py，请先复制 config.example.py 为 config.py 并填入配置")
    sys.exit(1)

import importlib.util
spec = importlib.util.spec_from_file_location("config", CONFIG_PATH)
config = importlib.util.ModuleFromSpec(spec)
spec.loader.exec_module(config)

# ── 依赖检查 ─────────────────────────────────────────────

try:
    import feedparser
except ImportError:
    print("⚠ feedparser 未安装，文章抓取将基于 HTML 解析")
    feedparser = None


# ── 文章抓取 ─────────────────────────────────────────────

def parse_insights_page(site_dir):
    """从 insights.html 解析最新文章列表"""
    insights_path = Path(site_dir) / "insights.html"
    if not insights_path.exists():
        print(f"❌ 找不到 insights.html: {insights_path}")
        return []

    html = insights_path.read_text(encoding="utf-8")

    articles = []

    # 匹配 <a class="insight-item" href="xxx.html">
    item_blocks = re.findall(
        r'<a class="insight-item" href="([^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )

    for href, block in item_blocks:
        # 提取标题
        title_m = re.search(r'data-i18n="list\.([^"]+)\.title"[^>]*>(.*?)</h3>', block)
        if not title_m:
            title_m = re.search(r'<h3[^>]*>(.*?)</h3>', block)

        # 提取日期
        date_m = re.search(r'<span class="day">(\d+)</span>(\w+)', block)

        # 提取标签
        tags = re.findall(r'<span class="insight-tag"[^>]*>(.*?)</span>', block)

        if title_m:
            title = title_m.group(1) if title_m.group(1).startswith('data-i18n') else title_m.group(2)
            title = re.sub(r'<[^>]+>', '', title).strip()

            articles.append({
                "url": href if href.startswith("http") else f"https://yl0223-ai.github.io/linkx-site/{href}",
                "title": title,
                "date_day": date_m.group(1) if date_m else "",
                "date_mon": date_m.group(2) if date_m else "",
                "tags": [t.strip() for t in tags],
            })

    return articles[:config.TOP_N_ARTICLES]


# ── 邮件模板 ─────────────────────────────────────────────

def build_email_html(articles, subject_date):
    """渲染 HTML 邮件"""

    # 读模板
    tpl_path = Path(__file__).parent / "template.html"
    if tpl_path.exists():
        tpl = tpl_path.read_text(encoding="utf-8")
    else:
        tpl = _default_template()

    article_items = ""
    for a in articles:
        tags_html = "".join(
            f'<span class="tag">{t}</span>' for t in a.get("tags", [])
        )
        article_items += f"""
        <a href="{a['url']}" class="article-item">
          <div class="article-meta">{tags_html}</div>
          <div class="article-title">{a['title']}</div>
          <div class="article-date">{a['date_day']} {a['date_mon']}</div>
        </a>
        """

    html = tpl.replace("{{SUBJECT_DATE}}", subject_date)
    html = html.replace("{{ARTICLES}}", article_items)
    html = html.replace("{{YEAR}}", str(datetime.now().year))
    return html


def _default_template():
    return """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LINK-X Capital 前沿洞察</title>
</head>
<body>
  <div class="container">
    <header>
      <div class="logo">星连资本 LINK-X Capital</div>
      <p class="subtitle">前沿洞察 · {{SUBJECT_DATE}}</p>
    </header>

    <div class="articles">
      {{ARTICLES}}
    </div>

    <footer>
      <p>你收到这封邮件是因为曾在星连资本官网订阅前沿洞察。</p>
      <p>不想继续收到？<a href="mailto:hello@linkx.vc?subject=退订">点击退订</a></p>
      <p>&copy; {{YEAR}} 星连资本 · 北京清华科技园</p>
    </footer>
  </div>
  <style>
    body { font-family: -apple-system, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
    .container { max-width: 600px; margin: 0 auto; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,.1); }
    header { background: linear-gradient(135deg, #151012, #2A162F); color: #fff; padding: 32px; }
    .logo { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
    .subtitle { opacity: 0.7; font-size: 13px; }
    .articles { padding: 24px 32px; }
    .article-item { display: block; padding: 16px 0; border-bottom: 1px solid #eee; text-decoration: none; color: inherit; }
    .article-item:last-child { border-bottom: none; }
    .article-item:hover .article-title { color: #660874; }
    .article-meta { margin-bottom: 6px; }
    .tag { display: inline-block; font-size: 10px; padding: 2px 8px; border: 1px solid #660874; color: #660874; border-radius: 4px; margin-right: 6px; text-transform: uppercase; letter-spacing: .05em; }
    .article-title { font-size: 16px; font-weight: 500; color: #1C1917; margin-bottom: 4px; }
    .article-date { font-size: 12px; color: #999; }
    footer { padding: 24px 32px; background: #fafaf8; font-size: 12px; color: #999; line-height: 1.8; }
    footer a { color: #660874; }
    @media (max-width: 480px) { body { padding: 0; } .articles { padding: 16px; } header { padding: 24px 16px; } footer { padding: 16px; } }
  </style>
</body>
</html>"""


# ── 订阅人读取 ───────────────────────────────────────────

def load_subscribers():
    """从飞书或本地文件读取订阅人列表"""
    subscribers = []

    # 优先飞书
    if config.FEISHU_APP_ID and config.FEISHU_APP_SECRET and config.FEISHU_TABLE_ID:
        subscribers = _load_from_feishu()
    else:
        subscribers = _load_from_files()

    print(f"✓ 读取到 {len(subscribers)} 位订阅人")
    return subscribers


def _load_from_files():
    """从 subscribers/emails.txt 读取"""
    base = Path(__file__).parent / "subscribers"
    txt_path = base / "emails.txt"

    if not txt_path.exists():
        print(f"⚠ 找不到 {txt_path}，请创建并填入邮箱（每行一个）")
        return []

    emails = []
    for line in txt_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            # 简单格式校验
            if re.match(r"[^@]+@[^@]+\.[^@]+", line):
                emails.append(line)

    return emails


def _load_from_feishu():
    """从飞书多维表格读取订阅人"""
    try:
        import requests
    except ImportError:
        print("❌ 需要安装 requests: pip install requests")
        sys.exit(1)

    # 获取 tenant_access_token
    token_url = f"https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(token_url, json={
        "app_id": config.FEISHU_APP_ID,
        "app_secret": config.FEISHU_APP_SECRET,
    }, timeout=10)
    token_data = resp.json()
    token = token_data.get("tenant_access_token")
    if not token:
        print(f"❌ 飞书 token 获取失败: {token_data}")
        return []

    # 读取多维表格记录
    table_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{config.FEISHU_TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(table_url, headers=headers, timeout=10)
    records = resp.json().get("data", {}).get("items", [])

    emails = []
    for record in records:
        fields = record.get("fields", {})
        # 假设邮箱字段叫 "邮箱"
        email = fields.get("邮箱") or fields.get("email")
        if email:
            emails.append(str(email).strip())

    return emails


# ── 发送 ─────────────────────────────────────────────────

def send_email(to_list, subject, html_body, dry_run=False):
    """通过 SMTP 发送邮件"""
    if not to_list:
        print("⚠ 没有收件人，跳过发送")
        return

    if dry_run:
        print(f"\n📤 [DRY RUN] 邮件内容预览:")
        print(f"   收件: {', '.join(to_list[:3])}" + ("..." if len(to_list) > 3 else ""))
        print(f"   主题: {subject}")
        print(f"   大小: {len(html_body)} bytes")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{config.FROM_NAME} <{config.FROM_EMAIL}>"

    # 纯文本版本（降级用）
    text_body = re.sub(r"<[^>]+>", "", html_body)
    text_body = re.sub(r"\s+", " ", text_body).strip()

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # SSL 连接阿里云企业邮箱
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, context=context, timeout=30) as server:
            server.login(config.SMTP_USER, config.SMTP_PASS)

            # 分批 BCC 发送（保护隐私）
            for i in range(0, len(to_list), config.BATCH_SIZE):
                batch = to_list[i:i + config.BATCH_SIZE]
                # BCC 隐藏收件人
                msg.replace_header("To", ", ".join(batch))
                # Remove Bcc header and set envelope sender
                del msg["Bcc"]
                server.sendmail(
                    config.SMTP_USER,
                    batch,
                    msg.as_string()
                )
                print(f"  ✓ 批次 {i//config.BATCH_SIZE + 1}: 已发送 {len(batch)} 封 → {batch[0]}{'...' if len(batch)>1 else ''}")

        print(f"\n✅ 发送完成！共 {len(to_list)} 封")

    except smtplib.SMTPException as e:
        print(f"❌ SMTP 错误: {e}")
        raise


# ── 主程序 ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="发送 LINK-X Capital Newsletter")
    parser.add_argument("--dry-run", action="store_true", help="只打印，不发信")
    parser.add_argument("--test", metavar="EMAIL", help="只发到指定测试邮箱")
    args = parser.parse_args()

    site_dir = Path(__file__).parent.parent / config.SITE_DIR
    if not site_dir.exists():
        site_dir = Path(config.SITE_DIR)

    print(f"📖 抓取文章: {site_dir}")
    articles = parse_insights_page(site_dir)
    if not articles:
        print("❌ 没有找到文章，退出")
        sys.exit(1)

    print(f"✓ 找到 {len(articles)} 篇:")
    for a in articles:
        print(f"  · {a['title']}")

    # 主题行
    now = datetime.now()
    subject_date = now.strftime("%Y年%-m月")
    subject = f"LINK-X Capital 前沿洞察 · {subject_date}"

    # 渲染邮件
    html_body = build_email_html(articles, subject_date)

    # 确定收件人
    if args.test:
        to_list = [args.test]
        subject = f"[测试] {subject}"
    else:
        to_list = load_subscribers()

    if not to_list:
        print("❌ 没有订阅人，退出")
        sys.exit(1)

    # 发送
    print(f"\n📤 {'[DRY RUN] ' if args.dry_run else ''}发送邮件...")
    send_email(to_list, subject, html_body, dry_run=args.dry_run or config.DRY_RUN)


if __name__ == "__main__":
    main()