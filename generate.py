#!/usr/bin/env python3
"""
LINK-X Capital 文章页生成器

用法:
    python generate.py <md文件> <日期YYYY-MM-DD> <标签1> [标签2...] [-o 输出名]

示例:
    python generate.py 敢想敢为，基金25AGM.md 2025-11-12 news perspectives
    python generate.py 敢想敢为，基金25AGM.md 2025-11-12 news perspectives -o news-agm-2025
"""

import sys, os, re, argparse, subprocess
from datetime import datetime
from pathlib import Path

DIR = Path(__file__).parent

# ── Config ──────────────────────────────────────────────────
TAG_MAP = {
    'news':         ('新闻',       'News'),
    'perspectives': ('观点',       'Perspectives'),
    'portfolio':    ('投资组合',   'Portfolio'),
    'research':     ('研究',       'Research'),
    'spotlight':    ('聚焦',       'Spotlight'),
}

MENU_ZH = '"menu.open": "Menu", "menu.label": "导航", "menu.home": "首页", "menu.research": "洞察", "menu.focus": "关注领域", "menu.portfolio": "投资组合", "menu.team": "团队", "menu.contact": "联系我们", "menu.footer.meta": "© 2026 · 保留所有权利", "menu.research.kicker": "Insights Feed", "menu.research.text": "持续跟踪模型、infra、agent 与前沿计算的真实变化，记录 AI 生态的一线信号。", "menu.research.link": "获取最新动态", "menu.contact.kicker": "Build With Us", "menu.contact.text": "创始人、LP、媒体与研究伙伴，可以从这里找到 LINK-X 团队。", "menu.contact.link": "联系我们"'

MENU_EN = '"menu.open": "Menu", "menu.label": "Navigation", "menu.home": "Home", "menu.research": "Insights", "menu.focus": "Focus", "menu.portfolio": "Portfolio", "menu.team": "Team", "menu.contact": "Contact", "menu.footer.meta": "© 2026 · All rights reserved", "menu.research.kicker": "Research Feed", "menu.research.text": "Tracking real developments in models, infra, agents and frontier computing — one signal at a time.", "menu.research.link": "Get Latest Updates", "menu.contact.kicker": "Build With Us", "menu.contact.text": "Founders, LPs, media and research partners can reach the LINK-X team here.", "menu.contact.link": "Contact Us"'


# ── MD parsing ──────────────────────────────────────────────

def parse_md(md):
    """Parse markdown → (title, body_lines)"""
    lines = md.strip().split('\n')
    title = ''
    body_start = 0

    for i, line in enumerate(lines):
        if line.startswith('# ') and not title:
            title = line[2:].strip()
            body_start = i + 1
            break

    # Skip subtitle
    if body_start < len(lines) and lines[body_start].startswith('副标题'):
        body_start += 1

    # Skip blanks
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    return title, lines[body_start:]


def inline_md(text):
    """**bold** → <em>"""
    return re.sub(r'\*\*(.+?)\*\*', r'<em>\1</em>', text)


def js_esc(s):
    """Escape for JS string literal"""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def build_body(lines):
    """Convert MD lines → (HTML string, {key: value} i18n dict)"""
    html, zh = [], {}
    pc = h2c = h3c = lic = 0
    in_ul = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            html.append('      </ul>')
            in_ul = False

    for raw in lines:
        s = raw.strip()

        if not s:
            close_ul()
            continue
        if s == '---':
            close_ul()
            continue

        # Image
        m = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', s)
        if m:
            close_ul()
            html.append(f'      <figure><img src="{m.group(2)}" alt="{m.group(1)}"></figure>')
            continue

        # H3
        if s.startswith('### '):
            close_ul()
            h3c += 1; k = f'h3_{h3c}'
            t = inline_md(s[4:])
            html.append(f'      <h3 data-i18n="{k}">{t}</h3>')
            zh[k] = t
            continue

        # H2
        if s.startswith('## '):
            close_ul()
            h2c += 1; k = f'h2_{h2c}'
            t = inline_md(s[3:])
            html.append(f'      <h2 data-i18n="{k}">{t}</h2>')
            zh[k] = t
            continue

        # List item
        m = re.match(r'^[-*]\s+(.+)', s)
        if m:
            if not in_ul:
                html.append('      <ul>')
                in_ul = True
            lic += 1; k = f'li{lic}'
            t = inline_md(m.group(1))
            html.append(f'        <li data-i18n="{k}">{t}</li>')
            zh[k] = t
            continue

        # Paragraph
        close_ul()
        pc += 1; k = f'p{pc}'
        t = inline_md(s)
        html.append(f'      <p data-i18n="{k}">{t}</p>')
        zh[k] = t

    close_ul()
    return '\n\n'.join(html), zh


# ── i18n builders ───────────────────────────────────────────

def build_tags_html(tags):
    parts = []
    for tag in tags:
        zh_name = TAG_MAP.get(tag, (tag, tag))[0]
        parts.append(f'<span class="article-tag" data-i18n="article.tag.{tag}">{zh_name}</span>')
    return '\n      '.join(parts)


def build_i18n_zh(title, zh_entries, tags):
    lines = [f'      {MENU_ZH},']
    for tag in tags:
        zh_name = TAG_MAP.get(tag, (tag, tag))[0]
        lines.append(f'      "article.tag.{tag}": "{zh_name}",')
    lines.append(f'      "article.back": "← 返回洞察",')
    lines.append(f'      "title": "{js_esc(title)}",')
    for k, v in zh_entries.items():
        lines.append(f'      "{k}": "{js_esc(v)}",')
    lines.append(f'      "footer.desc": "与 AGI 时代的定义者同行。",')
    lines.append(f'      "footer.copy": "© 2026 北京星连肇基私募基金管理有限责任公司",')
    lines.append(f'      "footer.legal": "法律声明"')
    return '\n'.join(lines)


def build_i18n_en(title, zh_entries, tags):
    lines = [f'      {MENU_EN},']
    for tag in tags:
        en_name = TAG_MAP.get(tag, (tag, tag))[1]
        lines.append(f'      "article.tag.{tag}": "{en_name}",')
    lines.append(f'      "article.back": "← Back to Insights",')
    lines.append(f'      "title": "{js_esc(title)}",')
    # zh as placeholder — update manually
    for k, v in zh_entries.items():
        lines.append(f'      "{k}": "{js_esc(v)}",')
    lines.append(f'      "footer.desc": "Partnering with the founders defining the AGI era.",')
    lines.append(f'      "footer.copy": "© 2026 LINK-X Capital",')
    lines.append(f'      "footer.legal": "Legal"')
    return '\n'.join(lines)


# ── insights.html update ────────────────────────────────────

def update_insights(output_name, title, date, tags):
    path = DIR / 'insights.html'
    content = path.read_text('utf-8')

    month_key = f'month.{date.strftime("%b%Y").lower()}'
    month_zh = f'{date.year} 年 {date.month} 月 · {date.strftime("%B")}'
    month_en = date.strftime('%B %Y')
    day = str(date.day)
    month_short = date.strftime('%b')

    tag_html = '\n            '.join(
        f'<span class="insight-tag" data-i18n="tag.{t}">{TAG_MAP.get(t, (t,t))[0]}</span>'
        for t in tags
    )

    entry = (
        f'\n      <a class="insight-item" href="{output_name}.html">\n'
        f'        <div class="insight-date"><span class="day">{day}</span>{month_short}</div>\n'
        f'        <div class="insight-body">\n'
        f'          <div class="insight-meta">\n'
        f'            {tag_html}\n'
        f'          </div>\n'
        f'          <h3 data-i18n="list.{output_name}.title">{title}</h3>\n'
        f'        </div>\n'
        f'      </a>\n'
    )

    month_marker = f'data-i18n="{month_key}"'

    if month_marker in content:
        # Month exists → insert after divider line
        idx = content.index(month_marker)
        line_end = content.index('\n', idx)
        content = content[:line_end + 1] + entry + content[line_end + 1:]
    else:
        # New month → insert at top of insight-list
        divider = f'      <div class="month-divider" data-i18n="{month_key}">{month_zh}</div>\n'
        list_start = content.index('class="insight-list')
        insert_pos = content.index('>\n', list_start) + 2
        content = content[:insert_pos] + '\n' + divider + entry + content[insert_pos:]

    # Add i18n keys to zh section
    title_key = f'"list.{output_name}.title": "{js_esc(title)}"'
    zh_section_end = content.index('\n    },\n    en: {')
    if month_key not in content[:zh_section_end]:
        # Find last month.* line in zh
        last_month = content[:zh_section_end].rfind('"month.')
        if last_month >= 0:
            line_end = content.index('\n', last_month)
            content = content[:line_end + 1] + f'      "{month_key}": "{month_zh}",\n' + content[line_end + 1:]
    # Add title key in zh
    last_list = content[:zh_section_end].rfind('"list.')
    if last_list >= 0:
        line_end = content.index('\n', last_list)
        content = content[:line_end + 1] + f'      {title_key},\n' + content[line_end + 1:]

    # Add i18n keys to en section
    en_start = content.index('en: {')
    if month_key not in content[en_start:]:
        last_month_en = content[en_start:].rfind('"month.')
        if last_month_en >= 0:
            abs_pos = en_start + last_month_en
            line_end = content.index('\n', abs_pos)
            content = content[:line_end + 1] + f'      "{month_key}": "{month_en}",\n' + content[line_end + 1:]
    last_list_en = content[en_start:].rfind('"list.')
    if last_list_en >= 0:
        abs_pos = en_start + last_list_en
        line_end = content.index('\n', abs_pos)
        content = content[:line_end + 1] + f'      {title_key},\n' + content[line_end + 1:]

    path.write_text(content, 'utf-8')
    print(f"✓ Updated insights.html")


# ── Main ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Generate article page for LINK-X Capital')
    parser.add_argument('md_file', help='Markdown source file')
    parser.add_argument('date', help='Article date (YYYY-MM-DD)')
    parser.add_argument('tags', nargs='+', help='Tags: news perspectives portfolio research spotlight')
    parser.add_argument('-o', '--output', help='Output filename without .html (default: <tag>-<date>)')
    args = parser.parse_args()

    # Read MD
    md = Path(args.md_file).read_text('utf-8')
    title, body_lines = parse_md(md)
    date = datetime.strptime(args.date, '%Y-%m-%d')

    # Generate body + i18n
    body_html, zh_entries = build_body(body_lines)
    i18n_zh = build_i18n_zh(title, zh_entries, args.tags)
    i18n_en = build_i18n_en(title, zh_entries, args.tags)
    tags_html = build_tags_html(args.tags)

    # Fill template
    output_name = args.output or f"{args.tags[0]}-{args.date}"
    tpl = (DIR / 'template-article.html').read_text('utf-8')

    replacements = {
        '{{PAGE_TITLE}}': f'{title} · LINK-X Capital',
        '{{META_DESC}}': title,
        '{{TAGS_HTML}}': tags_html,
        '{{DATE_DISPLAY}}': date.strftime('%Y.%m.%d'),
        '{{ARTICLE_TITLE}}': title,
        '{{ARTICLE_BODY}}': body_html,
        '{{I18N_ZH}}': i18n_zh,
        '{{I18N_EN}}': i18n_en,
    }
    for old, new in replacements.items():
        tpl = tpl.replace(old, new)

    # Write output
    out_path = DIR / f'{output_name}.html'
    out_path.write_text(tpl, 'utf-8')
    print(f"✓ Generated {out_path.name}")

    # Update insights.html
    update_insights(output_name, title, date, args.tags)

    # JS syntax check
    import subprocess
    r = subprocess.run(
        ['node', '-e', f'const fs=require("fs");const c=fs.readFileSync("{out_path}","utf8");const s=c.indexOf("<script>")+8;const e=c.indexOf("</script>");new Function(c.substring(s,e));console.log("JS OK")'],
        capture_output=True, text=True
    )
    if r.returncode == 0:
        print(f"✓ JS syntax OK")
    else:
        print(f"⚠ JS syntax error: {r.stderr.strip()}")

    print(f"\nDone! Next steps:")
    print(f"  1. Review & edit en translations in {out_path.name}")
    print(f"  2. cd {DIR} && git add -A && git commit -m 'add: {title[:30]}' && git push")


if __name__ == '__main__':
    main()
