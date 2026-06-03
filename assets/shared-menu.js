(function () {
  const script = document.currentScript;
  const current = script?.dataset.current || "";
  const base = script?.dataset.base || "";
  const menuId = script?.dataset.menuId || "siteMenu";
  const overlayAttrs = menuId === "menu-overlay"
    ? 'aria-hidden="true" aria-label="Navigation" aria-modal="true" class="menu-overlay" id="menu-overlay" role="dialog"'
    : 'aria-hidden="true" class="menu-overlay" id="siteMenu"';
  const styleId = "linkx-shared-menu-style";
  const css = `
.menu-overlay {
  width: min(720px, 50vw) !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  scrollbar-width: none !important;
  background:
    radial-gradient(circle at 78% 26%, rgba(176, 124, 192, 0.14), transparent 30%),
    radial-gradient(circle at 10% 80%, rgba(102, 8, 116, 0.18), transparent 34%),
    linear-gradient(135deg, #171218 0%, #241827 48%, #171218 100%) !important;
}
.menu-overlay::-webkit-scrollbar {
  display: none !important;
}
.menu-overlay::before {
  content: "LinkX" !important;
  position: absolute !important;
  right: -0.08em !important;
  bottom: -0.28em !important;
  font-family: var(--font-serif, "Instrument Serif", Georgia, serif) !important;
  font-size: clamp(130px, 24vw, 360px) !important;
  line-height: 1 !important;
  color: rgba(250, 248, 244, 0.045) !important;
  pointer-events: none !important;
  letter-spacing: 0 !important;
  transform: none !important;
  z-index: 0 !important;
}
.menu-shell {
  position: relative !important;
  overflow: hidden !important;
  min-height: 100dvh !important;
  display: grid !important;
  grid-template-rows: auto 1fr auto !important;
  padding: 0 clamp(22px, 3vw, 40px) 28px !important;
}
.menu-shell::before {
  content: none !important;
}
.menu-top,
.menu-grid,
.menu-footer {
  position: relative !important;
  z-index: 1 !important;
}
.menu-top {
  height: 76px !important;
}
.menu-grid {
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: clamp(20px, 2.8vh, 32px) !important;
  align-items: stretch !important;
  padding: clamp(24px, 3.6vh, 40px) 0 clamp(18px, 2.6vh, 28px) !important;
  min-height: 0 !important;
}
.menu-primary {
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: 0 !important;
  border-top: 1px solid rgba(250, 248, 244, 0.18) !important;
}
.menu-primary a {
  display: grid !important;
  grid-template-columns: clamp(44px, 5vw, 64px) minmax(0, 1fr) minmax(86px, auto) !important;
  grid-template-rows: 1fr !important;
  align-items: center !important;
  min-height: clamp(76px, 9.4vh, 104px) !important;
  padding: 0 !important;
  border-right: 0 !important;
  border-bottom: 1px solid rgba(250, 248, 244, 0.18) !important;
  gap: clamp(14px, 2vw, 24px) !important;
  position: relative !important;
  overflow: hidden !important;
  text-decoration: none !important;
}
.menu-primary .menu-num {
  margin-bottom: 0 !important;
  align-self: center !important;
  justify-self: start !important;
  font-family: var(--font-mono, ui-monospace, monospace) !important;
  font-size: clamp(10px, 0.78vw, 12px) !important;
  letter-spacing: 0.1em !important;
  color: rgba(232, 213, 238, 0.54) !important;
}
.menu-primary strong {
  align-self: center !important;
  justify-self: start !important;
  font-family: var(--font-serif, "Instrument Serif", Georgia, serif) !important;
  font-size: clamp(34px, 4.3vw, 58px) !important;
  font-weight: 400 !important;
  line-height: 0.98 !important;
  letter-spacing: -0.035em !important;
  color: rgba(250, 248, 244, 0.92) !important;
  transform: none !important;
}
.menu-primary em {
  align-self: center !important;
  justify-self: end !important;
  min-width: 0 !important;
  text-align: right !important;
  font-family: var(--font-mono, ui-monospace, monospace) !important;
  font-size: clamp(9px, 0.75vw, 11px) !important;
  font-style: normal !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  color: rgba(250, 248, 244, 0.38) !important;
}
.menu-side {
  display: block !important;
  max-width: none !important;
  justify-self: stretch !important;
}
.menu-panel.menu-build-card {
  min-height: clamp(176px, 20vh, 236px) !important;
  border-radius: 28px !important;
  border: 1px solid rgba(250, 248, 244, 0.16) !important;
  background:
    radial-gradient(circle at 18% 16%, rgba(176, 124, 192, 0.22), transparent 36%),
    radial-gradient(circle at 92% 88%, rgba(250, 248, 244, 0.09), transparent 30%),
    linear-gradient(180deg, rgba(250, 248, 244, 0.085), rgba(250, 248, 244, 0.038)) !important;
  box-shadow:
    inset 0 1px 0 rgba(250, 248, 244, 0.10),
    0 18px 52px rgba(0, 0, 0, 0.10) !important;
  padding: clamp(22px, 2.7vw, 34px) !important;
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: 18px !important;
  align-content: end !important;
  overflow: hidden !important;
}
.menu-contact-cta {
  min-width: min(240px, 58%) !important;
  justify-content: space-between !important;
}
.menu-footer {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) auto !important;
  align-items: center !important;
  gap: clamp(18px, 2.4vw, 32px) !important;
  margin-top: clamp(10px, 1.6vh, 18px) !important;
  padding-top: 24px !important;
  border-top: 1px solid rgba(250, 248, 244, 0.12) !important;
}
.menu-overlay .menu-copyright-fixed {
  justify-self: start !important;
  color: rgba(250, 248, 244, 0.58) !important;
  font-family: var(--font-mono, ui-monospace, monospace) !important;
  font-size: 10px !important;
  line-height: 1.5 !important;
  letter-spacing: 0.04em !important;
  text-transform: none !important;
  white-space: normal !important;
}
html[data-lang="en"] .menu-overlay .menu-copyright-fixed {
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
}
.menu-overlay .menu-footer-brand {
  display: none !important;
}
.menu-social-matrix {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0 !important;
  margin-left: auto !important;
}
.menu-social-links {
  display: inline-flex !important;
  align-items: center !important;
  flex-wrap: nowrap !important;
  gap: 8px !important;
}
.menu-social-item {
  position: relative !important;
  display: inline-flex !important;
}
.menu-social-icon {
  width: 28px !important;
  height: 28px !important;
  display: inline-grid !important;
  place-items: center !important;
  padding: 0 !important;
  border: 1px solid rgba(250, 248, 244, 0.18) !important;
  border-radius: 50% !important;
  border-bottom-color: rgba(250, 248, 244, 0.18) !important;
  background: rgba(250, 248, 244, 0.045) !important;
  color: rgba(250, 248, 244, 0.84) !important;
  text-decoration: none !important;
}
.menu-social-icon:hover,
.menu-social-icon:focus-visible {
  transform: translateY(-2px) !important;
  border-color: rgba(250, 248, 244, 0.48) !important;
  background: rgba(250, 248, 244, 0.12) !important;
  color: #fff !important;
  outline: none !important;
}
.menu-social-icon svg,
.menu-social-icon img {
  width: 14px !important;
  height: 14px !important;
  display: block !important;
  fill: currentColor !important;
  object-fit: contain !important;
}
.menu-social-icon img.icon-xhs {
  width: 15px !important;
  height: 15px !important;
}
.menu-social-icon img.icon-douyin {
  width: 14px !important;
  height: 14px !important;
}
.menu-qr-popover {
  position: absolute !important;
  right: 50% !important;
  top: auto !important;
  bottom: calc(100% + 14px) !important;
  width: 168px !important;
  padding: 12px !important;
  border-radius: 8px !important;
  background: rgba(250, 248, 244, 0.98) !important;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.32) !important;
  opacity: 0 !important;
  visibility: hidden !important;
  transform: translate(50%, 8px) !important;
  pointer-events: none !important;
  transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s ease !important;
  z-index: 20 !important;
}
.menu-qr-popover::after {
  content: "" !important;
  position: absolute !important;
  right: 50% !important;
  bottom: -7px !important;
  width: 14px !important;
  height: 14px !important;
  background: rgba(250, 248, 244, 0.98) !important;
  transform: translateX(50%) rotate(45deg) !important;
}
.menu-qr-popover img {
  width: 100% !important;
  aspect-ratio: 1 !important;
  object-fit: cover !important;
  border-radius: 4px !important;
}
.menu-qr-popover span {
  display: block !important;
  margin-top: 9px !important;
  color: var(--text, #1C1917) !important;
  font-size: 12px !important;
  line-height: 1.4 !important;
  text-align: center !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
}
.menu-social-item:hover .menu-qr-popover,
.menu-social-item:focus-within .menu-qr-popover {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translate(50%, 0) !important;
  pointer-events: auto !important;
}
@media (max-width: 860px) {
  .menu-overlay {
    width: 100vw !important;
  }
  .menu-shell::before {
    content: none !important;
  }
  .menu-grid {
    padding: 28px 0 !important;
    gap: 24px !important;
  }
  .menu-primary strong {
    font-size: clamp(26px, 8vw, 34px) !important;
  }
  .menu-primary a {
    grid-template-columns: 36px 1fr !important;
    min-height: 72px !important;
  }
  .menu-panel.menu-build-card {
    min-height: 210px !important;
    padding: 24px !important;
  }
  .menu-footer {
    grid-template-columns: 1fr !important;
    align-items: start !important;
  }
  .menu-social-matrix {
    margin-left: 0 !important;
    justify-content: flex-start !important;
  }
  .menu-social-links {
    flex-wrap: wrap !important;
  }
  .menu-social-icon {
    width: 30px !important;
    height: 30px !important;
  }
}`;

  const items = [
    { key: "home", href: "index.html#slogan", i18n: "menu.home", zh: "首页", en: "Home" },
    { key: "portfolio", href: "portfolio.html", i18n: "menu.nav.portfolio", zh: "投资组合", en: "Portfolio" },
    { key: "team", href: "team.html", i18n: "menu.nav.team", zh: "团队", en: "Team" },
    { key: "insights", href: "insights.html", i18n: "menu.nav.insights", zh: "洞察", en: "Insights" }
  ].filter(item => item.key !== current);

  const href = value => `${base}${value}`;
  const nav = items.map((item, index) => `
<a data-menu-link="" href="${href(item.href)}"><span class="menu-num">${String(index + 1).padStart(2, "0")}</span><strong data-i18n="${item.i18n}">${item.zh}</strong><em>${item.en}</em></a>`).join("");

  const html = `
<div ${overlayAttrs}>
<div class="menu-shell">
<div class="menu-top">
<div class="menu-label"><span data-i18n="menu.label">导航</span><i>/</i><em>Menu</em></div>
<button aria-label="Close menu" class="menu-close" data-menu-close="" type="button"><span></span><span></span></button>
</div>
<div class="menu-grid">
<nav aria-label="Primary navigation" class="menu-primary">${nav}
</nav>
<aside aria-label="Featured links" class="menu-side">
<div class="menu-panel menu-build-card">
<div class="menu-build-copy">
<div class="menu-kicker" data-i18n="menu.contact.kicker">Build With Us</div>
<p data-i18n="menu.contact.text"><span class="phrase">如果你正在寻找、定义，</span><span class="phrase">或亲手建造一个尚未被市场命名的未来，</span><span class="phrase">我们希望更早与你相遇。</span></p>
</div>
<a class="menu-contact-cta" data-menu-link="" href="${href("contact.html")}"><span data-i18n="menu.contact.link">联系我们</span><span aria-hidden="true">→</span></a>
</div>
</aside>
</div>
<div class="menu-footer">
<span class="menu-copyright-fixed" aria-label="版权信息" data-i18n="footer.copyright">@2026 北京星连肇基私募基金管理有限责任公司</span>
<span class="menu-footer-brand" data-i18n="menu.footer.meta">LINKX CAPITAL</span>
<div aria-label="社媒账号" class="menu-footer-social menu-social-matrix">
<div class="menu-social-links">
<div class="social-item menu-social-item">
<button aria-label="基金微信公众号二维码" class="social-icon menu-social-icon" type="button">
<img alt="" aria-hidden="true" src="https://cdn.simpleicons.org/wechat/FFFFFF"/>
</button>
<div class="qr-popover menu-qr-popover" role="tooltip">
<img alt="基金微信公众号二维码" onerror="this.closest('.qr-popover').classList.add('qr-missing'); this.style.display='none';" onload="this.closest('.qr-popover').classList.remove('qr-missing'); this.style.display='block';" src="${href("assets/wechat-linkx-capital.jpg")}"/><div aria-hidden="true" class="qr-fallback">QR</div>
<span data-i18n="footer.wechatFund">基金微信公众号</span>
</div>
</div>
<div class="social-item menu-social-item">
<button aria-label="孵化器微信公众号二维码" class="social-icon menu-social-icon" type="button">
<img alt="" aria-hidden="true" src="https://cdn.simpleicons.org/wechat/FFFFFF"/>
</button>
<div class="qr-popover menu-qr-popover" role="tooltip">
<img alt="孵化器微信公众号二维码" onerror="this.closest('.qr-popover').classList.add('qr-missing'); this.style.display='none';" onload="this.closest('.qr-popover').classList.remove('qr-missing'); this.style.display='block';" src="${href("assets/wechat-qingzhi-incubator.jpg")}"/><div aria-hidden="true" class="qr-fallback">QR</div>
<span data-i18n="footer.wechatIncubator">孵化器微信公众号</span>
</div>
</div>
<a aria-label="小红书账号" class="social-icon menu-social-icon" href="https://xhslink.com/m/UjLFumWxau" rel="noopener" target="_blank">
<img alt="" aria-hidden="true" class="icon-xhs" src="https://cdn.simpleicons.org/xiaohongshu/FFFFFF"/>
</a>
<a aria-label="抖音账号" class="social-icon menu-social-icon" href="https://www.douyin.com/user/MS4wLjABAAAAHYtbwIVUi113kSYUweZGc-tFiJGG1WPk8Jgldgk9Fhw?previous_page=app_code_link" rel="noopener" target="_blank">
<img alt="" aria-hidden="true" class="icon-douyin" src="https://cdn.simpleicons.org/tiktok/FFFFFF"/>
</a>
<a aria-label="LinkX Capital on X" class="social-icon menu-social-icon" href="https://x.com/LinkXCapital" rel="noreferrer" target="_blank">
<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24"><path d="M13.93 10.36 21.38 2h-1.77l-6.47 7.25L7.98 2H2.03l7.82 11.02L2.03 22h1.77l6.83-7.65L16.09 22h5.95l-8.11-11.64Zm-2.42 2.71-.79-1.09L4.42 3.29h2.71l5.08 7.01.79 1.09 6.61 9.12H16.9l-5.39-7.44Z" fill="currentColor"></path></svg>
</a>
<a aria-label="LinkX Capital on LinkedIn" class="social-icon menu-social-icon" href="https://www.linkedin.com/company/link-x-%E6%98%9F%E8%BF%9E%E8%B5%84%E6%9C%AC/?viewAsMember=true" rel="noreferrer" target="_blank">
<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5ZM.36 8.12h4.25V23H.36V8.12ZM7.5 8.12h4.07v2.03h.06c.57-1.08 1.96-2.22 4.03-2.22 4.31 0 5.1 2.84 5.1 6.53V23h-4.24v-7.56c0-1.8-.03-4.12-2.51-4.12-2.52 0-2.9 1.97-2.9 4V23H7.5V8.12Z" fill="currentColor"></path></svg>
</a>
</div>
</div>
</div>
</div>
</div>`;

  if (!document.getElementById(styleId)) {
    const style = document.createElement("style");
    style.id = styleId;
    style.textContent = css;
    document.head.appendChild(style);
  }

  const mount = script?.previousElementSibling?.matches?.("[data-shared-menu]") ? script.previousElementSibling : null;
  if (mount) {
    mount.outerHTML = html;
  } else if (script) {
    script.insertAdjacentHTML("beforebegin", html);
  }

  const menu = document.getElementById(menuId);
  const setMenuOpen = open => {
    if (!menu) return;
    menu.classList.toggle("is-open", open);
    menu.setAttribute("aria-hidden", open ? "false" : "true");
    document.body.classList.toggle("menu-open", open);
    document.querySelectorAll("[data-menu-open]").forEach(button => {
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
  };

  document.addEventListener("pointerdown", event => {
    if (!menu?.classList.contains("is-open")) return;
    if (menu.contains(event.target) || event.target.closest("[data-menu-open], [data-menu-close]")) return;
    setMenuOpen(false);
  }, true);

  document.addEventListener("click", event => {
    if (!menu?.classList.contains("is-open")) return;
    if (menu.contains(event.target) || event.target.closest("[data-menu-open], [data-menu-close]")) return;
    event.preventDefault();
    event.stopPropagation();
    setMenuOpen(false);
  }, true);

  document.addEventListener("click", event => {
    const link = event.target.closest("a[href]");
    if (!link || link.target || link.origin !== location.origin) return;
    const lang = document.documentElement.dataset.lang || document.documentElement.lang || "";
    const shortLang = lang.toLowerCase().startsWith("en") ? "en" : lang.toLowerCase().startsWith("zh") ? "zh" : "";
    if (!shortLang || link.searchParams?.get?.("lang") === shortLang) return;
    if (!/\.html(?:$|[?#])/.test(link.getAttribute("href")) && !link.pathname.endsWith("/")) return;
    const url = new URL(link.href);
    url.searchParams.set("lang", shortLang);
    link.href = url.href;
  }, true);
})();
