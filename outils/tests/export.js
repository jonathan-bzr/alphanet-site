// Exporte les icônes, le logo en PNG et l'image de partage (Open Graph).
// Usage : node outils/tests/export.js <racine du dépôt> (site servi sur http://127.0.0.1:8766/)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [R, S] = process.argv.slice(2);
  const BASE = 'http://127.0.0.1:8766/';
  const img = (p) => BASE + 'assets/img/' + p;
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ deviceScaleFactor: 1, bypassCSP: true })).newPage();
  await page.goto(BASE + 'mentions-legales.html');

  const shotSvg = async (src, w, h, out, opts = {}) => {
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><body style="margin:0;background:${opts.bg || 'transparent'}"><img src="${src}" style="display:block;width:${w}px;height:${h}px;${opts.pad ? `padding:${opts.pad}px;box-sizing:border-box;` : ''}"></body></html>`);
    await page.waitForLoadState('networkidle'); await page.waitForTimeout(150);
    await page.screenshot({ path: out, omitBackground: !opts.bg, type: out.endsWith('.jpg') ? 'jpeg' : 'png', quality: out.endsWith('.jpg') ? 88 : undefined });
  };

  await shotSvg(img('favicon.svg'), 32, 32, path.join(R, 'assets/img/favicon-32.png'));
  await shotSvg(img('favicon.svg'), 180, 180, path.join(R, 'assets/img/apple-touch-icon.png'));
  await shotSvg(img('favicon.svg'), 512, 512, path.join(R, 'assets/img/logo/logo-icone-app-512.png'));
  // logo en PNG (fond transparent), 1200 px de large
  const ratio = 260 / 64;  // largeur du viewBox de logo-couleur.svg
  await shotSvg(img('logo/logo-couleur.svg'), 1200, Math.round(1200 / ratio), path.join(R, 'assets/img/logo/logo-couleur.png'));
  await shotSvg(img('logo/logo-blanc.svg'), 1200, Math.round(1200 / ratio), path.join(R, 'assets/img/logo/logo-blanc.png'));
  await shotSvg(img('logo/logo-noir.svg'), 1200, Math.round(1200 / ratio), path.join(R, 'assets/img/logo/logo-noir.png'));
  // logo pour la signature mail : 170 x 41 affiché, image en double résolution
  await shotSvg(img('logo/logo-couleur.svg'), 340, Math.round(340 / ratio), path.join(R, 'assets/img/signature/alphanet-group-signature.png'));

  // Image de partage 1200 x 630
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(`<!doctype html><html><head><style>
    @font-face{font-family:PJS;src:url(${BASE}assets/fonts/plus-jakarta-sans-latin.woff2) format('woff2');font-weight:200 800}
    body{margin:0;width:1200px;height:630px;font-family:PJS;color:#0c1a2e;position:relative;overflow:hidden;
      background:url(${img('fond/fond-clair-paysage-1440.webp')}) 70% center/cover}
    .veil{position:absolute;inset:0;background:linear-gradient(100deg,rgb(238 242 248/.85) 0%,rgb(238 242 248/.4) 50%,rgb(238 242 248/0) 75%)}
    .c{position:absolute;left:84px;top:96px;right:84px}
    .logo{height:92px;display:block}
    h1{margin:64px 0 0;font-size:56px;line-height:1.08;letter-spacing:-.025em;font-weight:800;max-width:780px}
    h1 span{color:#1f5ad6}
    p{margin:26px 0 0;font-size:26px;font-weight:600;color:#46566c}
    .tel{display:inline-block;margin-top:34px;padding:14px 26px;border-radius:999px;background:#1f5ad6;color:#fff;font-size:26px;font-weight:750}
  </style></head><body><div class="veil"></div><div class="c">
    <img class="logo" src="${img('logo/logo-couleur.svg')}">
    <h1>Nettoyage professionnel <span>dans l’Hérault (34) et en Occitanie</span></h1>
    <p>Bureaux · Hôtellerie · Copropriétés · Commerces</p>
    <div class="tel">07 58 34 04 07</div>
  </div></body></html>`);
  await page.waitForLoadState('networkidle'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(R, 'assets/img/og-image.jpg'), type: 'jpeg', quality: 86 });
  await browser.close();
})();
