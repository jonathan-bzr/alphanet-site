// Tests du site : node outils/tests/suite.js http://127.0.0.1:8766/ <chemin vers axe.min.js>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const assert = (cond, msg) => { console.log(`${cond ? 'OK  ' : 'FAIL'} ${msg}`); if (!cond) process.exitCode = 1; };
const PAGES = ['index', 'entreprise', 'services', 'engagements', 'contact', 'mentions-legales'];
const ROOT = path.resolve(__dirname, '..', '..');

(async () => {
  const [base, axePath] = process.argv.slice(2);
  const browser = await chromium.launch();

  // ---------- Liens internes : toutes les pages et ancres existent ----------
  const ids = {};
  for (const p of PAGES) {
    const html = fs.readFileSync(path.join(ROOT, `${p}.html`), 'utf8');
    ids[`${p}.html`] = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));
  }
  let badLinks = [];
  for (const p of PAGES) {
    const html = fs.readFileSync(path.join(ROOT, `${p}.html`), 'utf8');
    for (const m of html.matchAll(/href="([^"#?]*)(\?[^"#]*)?(#[^"]*)?"/g)) {
      const [, file, , hash] = m;
      if (/^(https?:|tel:|mailto:)/.test(file) || (!file && !hash)) continue;
      const target = file || `${p}.html`;
      if (!fs.existsSync(path.join(ROOT, target))) { badLinks.push(`${p}: ${target} introuvable`); continue; }
      if (hash && !(ids[target] && ids[target].has(hash.slice(1)))) badLinks.push(`${p}: ${target}${hash} introuvable`);
    }
    for (const m of html.matchAll(/(?:src|href)="(assets\/[^"?]+)/g)) {
      if (!fs.existsSync(path.join(ROOT, m[1]))) badLinks.push(`${p}: fichier ${m[1]} introuvable`);
    }
  }
  assert(badLinks.length === 0, `liens et fichiers internes valides ${badLinks.join(' | ')}`);
  const forbidden = PAGES.filter((p) => /partenaire|Atout-Box|marquee/i.test(fs.readFileSync(path.join(ROOT, `${p}.html`), 'utf8')));
  assert(forbidden.length === 0, `plus aucune mention de partenaires dans les pages (${forbidden.join(', ')})`);
  const css = fs.readFileSync(path.join(ROOT, 'assets/css/styles.css'), 'utf8') + fs.readFileSync(path.join(ROOT, 'assets/js/main.js'), 'utf8');
  assert(!/partner|marquee/i.test(css), 'plus de code de partenaires dans le CSS et le JS');

  // ---------- Thème : clair par défaut même si l'appareil est en sombre ----------
  let ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: 'dark' });
  let page = await ctx.newPage();
  const errors = [];
  page.on('console', (m) => { if (['error', 'warning'].includes(m.type())) errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(`${base}index.html`, { waitUntil: 'networkidle' });
  assert(await page.evaluate(() => document.documentElement.dataset.theme) === 'light', 'appareil en sombre : le site s’ouvre en clair');
  await page.click('.theme-fab'); await page.waitForTimeout(600);
  assert(await page.evaluate(() => document.documentElement.dataset.theme) === 'dark', 'bouton : passage en sombre');
  await page.goto(`${base}services.html`, { waitUntil: 'networkidle' });
  assert(await page.evaluate(() => document.documentElement.dataset.theme) === 'dark', 'le choix sombre suit sur les autres pages');
  await page.click('.theme-fab'); await page.waitForTimeout(600);
  assert(await page.evaluate(() => document.documentElement.dataset.theme) === 'light', 'retour en clair');

  // ---------- Menu : page active, 5 liens ----------
  for (const p of PAGES.slice(0, 5)) {
    await page.goto(`${base}${p}.html`, { waitUntil: 'networkidle' });
    const cur = await page.$$eval('.nav-list a[aria-current="page"]', (a) => a.map((x) => x.getAttribute('href')));
    assert(cur.length === 1 && cur[0] === `${p}.html`, `${p} : lien actif du menu = ${cur.join(',')}`);
  }
  const navHrefs = await page.$$eval('.nav-list a', (a) => a.map((x) => x.getAttribute('href')));
  assert(navHrefs.length === 5, `menu : ${navHrefs.join(', ')}`);

  // ---------- Chiffres clés ----------
  await page.goto(`${base}index.html`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1800);
  const nums = await page.$$eval('[data-count]', (e) => e.map((x) => x.textContent));
  const years = new Date().getFullYear() - 2014 - (new Date() < new Date(new Date().getFullYear(), 3, 10) ? 1 : 0);
  assert(nums.join() === `${years},6,1,34`, `chiffres clés : ${nums.join(' | ')} (années attendues : ${years})`);


  // ---------- En-tête allégé, formulation du secteur, sécurité statique ----------
  for (const p of PAGES) {
    const html = fs.readFileSync(path.join(ROOT, `${p}.html`), 'utf8');
    const head = html.slice(html.indexOf('<header'), html.indexOf('</header>'));
    const desk = head.slice(0, head.indexOf('id="menu"'));
    assert(!/header-phone|data-theme-toggle|href="tel:/.test(desk), `${p} : en-tête sans téléphone ni bouton de thème`);
    assert(/Content-Security-Policy/.test(html) && /require-trusted-types-for/.test(html), `${p} : CSP présente`);
    assert(!/<script(?![^>]*(\ssrc=|ld\+json))[^>]*>/.test(html) && !/\sstyle="/.test(html) && !/\son[a-z]+="/.test(html), `${p} : aucun script ni style en ligne`);
    for (const m of html.matchAll(/<a [^>]*href="https?:[^>]*>/g)) assert(/rel="[^"]*noopener/.test(m[0]), `${p} : lien externe protégé ${m[0].slice(0, 60)}`);
    assert(!/Société Service|id="apres-sinistre"/.test(html), `${p} : nom Alphanet Group, plus de service « Après sinistre » séparé`);
    assert(/Alphanet Group/.test(html), `${p} : nom Alphanet Group présent`);
  }
  for (const p of ['index', 'entreprise', 'services', 'contact']) {
    const h = fs.readFileSync(path.join(ROOT, `${p}.html`), 'utf8');
    assert(/Hérault \(34\)/.test(h) && /Occitanie/.test(h), `${p} : secteur « Hérault (34) » et Occitanie`);
  }
  {
    const h = fs.readFileSync(path.join(ROOT, 'services.html'), 'utf8');
    const ids = [...h.matchAll(/<article class="svc[^"]*" id="([^"]+)"/g)].map((m) => m[1]);
    assert(ids.join() === 'bureaux,hotellerie,coproprietes,commerces,vitrerie,remise-en-etat', `services : ${ids.join(', ')}`);
    const idx = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
    assert((idx.match(/service--featured/g) || []).length === 2, 'accueil : Bureaux et Hôtellerie mis en avant');
    assert(fs.existsSync(path.join(ROOT, 'robots.txt')) && /Sitemap:/.test(fs.readFileSync(path.join(ROOT, 'robots.txt'), 'utf8')), 'robots.txt avec le plan du site');
    for (const p of PAGES) {
      const t = fs.readFileSync(path.join(ROOT, `${p}.html`), 'utf8');
      for (const m of t.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
        let ok = true; try { JSON.parse(m[1]); } catch (e) { ok = false; }
        assert(ok, `${p} : données structurées JSON valides`);
      }
      assert((t.match(/<h1[\s>]/g) || []).length === 1, `${p} : un seul titre principal (h1)`);
      const d = (t.match(/<meta name="description" content="([^"]+)"/) || [])[1] || '';
      assert(d.length >= 70 && d.length <= 230, `${p} : description ${d.length} caractères`);
    }
  }
  await page.goto(`${base}index.html`, { waitUntil: 'networkidle' });
  assert(await page.$$eval('[data-theme-toggle]', (e) => e.length) === 1 && await page.$eval('.theme-fab', (b) => getComputedStyle(b).position === 'fixed'), 'un seul bouton clair / sombre, flottant');
  await page.evaluate(() => window.scrollTo({ top: 1500, behavior: 'instant' })); await page.waitForTimeout(400);
  await page.reload({ waitUntil: 'networkidle' }); await page.waitForTimeout(500);
  assert(await page.evaluate(() => Math.round(window.scrollY)) === 0, 'rechargement : la page repart du haut');
  await page.goto(`${base}services.html#vitrerie`, { waitUntil: 'networkidle' }); await page.waitForTimeout(900);
  const vit = await page.evaluate(() => ({ y: Math.round(window.scrollY), top: Math.round(document.getElementById('vitrerie').getBoundingClientRect().top), h: document.querySelector('.site-header').offsetHeight }));
  assert(vit.y > 0 && vit.top >= 0 && vit.top < vit.h + 40, `lien avec ancre : arrive sous l’en-tête (${JSON.stringify(vit)})`);
  // la page ne se laisse pas encadrer
  const framed = await browser.newContext({ viewport: { width: 800, height: 600 } });
  const fp = await framed.newPage();
  await fp.route(`${base}frame-test.html`, (r) => r.fulfill({ contentType: 'text/html', body: `<iframe src="index.html" width="700" height="500"></iframe>` }));
  await fp.goto(`${base}frame-test.html`, { waitUntil: 'load' }); await fp.waitForTimeout(1000);
  const fr = fp.frames().find((f) => f !== fp.mainFrame() && f.url().includes('index.html'));
  assert(fp.url().endsWith('/index.html') && fp.frames().length === 1, 'page encadrée dans une autre page : le site sort du cadre (anti-clickjacking)');
  await framed.close();

  // ---------- Formulaire : pré-remplissage et validation ----------
  await page.goto(`${base}contact.html?prestation=vitrerie#formulaire`, { waitUntil: 'networkidle' });
  assert(await page.$eval('#f-type', (s) => s.value) === 'Vitrerie', 'lien « devis » : prestation Vitrerie pré-remplie');
  await page.goto(`${base}contact.html?prestation=<script>alert(1)</script>`, { waitUntil: 'networkidle' });
  assert(await page.$eval('#f-type', (s) => s.value) === '', 'paramètre inconnu ou piégé ignoré');
  await page.click('.form-submit button');
  const errs = await page.$$eval('.field-error', (e) => e.map((x) => x.textContent).filter(Boolean));
  assert(errs.length === 4, `formulaire vide : ${errs.length} erreurs`);
  await page.fill('#f-nom', 'Test Client'); await page.fill('#f-telephone', '06 12 34 56 78');
  await page.fill('#f-email', 'client@exemple.fr'); await page.selectOption('#f-type', 'Vitrerie');
  const posts = [];
  await page.route('**/api/devis', (route) => {
    posts.push(route.request().postDataJSON());
    return route.fulfill({ status: posts.length === 1 ? 200 : 503, contentType: 'application/json', body: '{"ok":true}' });
  });
  await page.waitForTimeout(300);
  await page.click('.form-submit button');
  await page.waitForSelector('[data-form-status]:not([hidden])');
  await page.waitForFunction(() => !document.querySelector('.form-submit button').disabled);
  const status = await page.textContent('[data-form-status]');
  assert(/bien été envoyée/i.test(status) && await page.inputValue('#f-nom') === '', `formulaire valide envoyé : « ${status.trim()} »`);
  assert(posts[0] && posts[0].email === 'client@exemple.fr' && posts[0].type === 'Vitrerie' && posts[0].site_web === '' && typeof posts[0].t === 'number', `données envoyées (${JSON.stringify(posts[0] || {}).slice(0, 80)})`);
  assert(errors.length === 0, `aucune erreur console / CSP (${errors.join(' | ')})`);
  await page.fill('#f-nom', 'Test Client'); await page.fill('#f-telephone', '06 12 34 56 78');
  await page.fill('#f-email', 'client@exemple.fr'); await page.selectOption('#f-type', 'Vitrerie');
  await page.click('.form-submit button');
  await page.waitForFunction(() => document.querySelector('[data-form-status] a'));
  const mailto = await page.getAttribute('[data-form-status] a', 'href');
  assert(mailto.startsWith('mailto:contact@alphanet-group.fr?subject=') && !/[\r\n]/.test(decodeURIComponent(mailto.split('subject=')[1].split('&')[0])), `échec d’envoi : bouton messagerie vers la bonne adresse (${mailto.slice(0, 60)})`);
  await page.unroute('**/api/devis');
  errors.length = 0;

  // ---------- Débordement horizontal et en-tête à toutes les largeurs ----------
  for (const w of [320, 390, 768, 1024, 1100, 1280, 1440, 1920]) {
    await page.setViewportSize({ width: w, height: 900 });
    const bad = [];
    for (const p of PAGES) {
      await page.goto(`${base}${p}.html`, { waitUntil: 'networkidle' });
      const o = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      if (o > 0) bad.push(`${p}+${o}px`);
      if (w >= 1080) {
        const hdr = await page.evaluate(() => {
          const inner = document.querySelector('.header-inner');
          const kids = [...inner.children].filter((k) => k.getClientRects().length);
          const last = kids[kids.length - 1].getBoundingClientRect();
          const nav = document.querySelector('.nav-list').getBoundingClientRect();
          const act = document.querySelector('.header-actions').getBoundingClientRect();
          const links = [...document.querySelectorAll('.nav-list a')].map((a) => a.getBoundingClientRect().height);
          return { right: last.right, vw: window.innerWidth, overlap: nav.right > act.left + 1, wrapped: Math.max(...links) > 50 };
        });
        if (hdr.right > hdr.vw || hdr.overlap || hdr.wrapped) bad.push(`${p}: en-tête serré (${JSON.stringify(hdr)})`);
      }
    }
    assert(bad.length === 0, `${w}px : pas de débordement ni d’en-tête cassé ${bad.join(' ; ')}`);
  }
  await ctx.close();

  // ---------- Mobile : menu et barre d'action ----------
  ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  page = await ctx.newPage();
  await page.goto(`${base}index.html`, { waitUntil: 'networkidle' });
  assert(await page.evaluate(() => !document.querySelector('[data-mobile-bar]').classList.contains('is-visible')), 'barre mobile cachée en haut');
  await page.click('[data-nav-toggle]');
  assert(await page.evaluate(() => document.querySelector('[data-menu]').classList.contains('is-open')), 'menu ouvert');
  const items = await page.$$eval('[data-menu] .menu-list a', (a) => a.map((x) => x.textContent.trim()));
  assert(items.join() === 'Accueil,Entreprise,Services,Engagements,Contact', `menu mobile : ${items.join(', ')}`);
  assert(await page.evaluate(() => getComputedStyle(document.documentElement).overflow === 'hidden'), 'menu ouvert : la page derrière ne défile plus');
  await page.click('[data-menu] a[href="services.html"]');
  await page.waitForURL('**/services.html');
  await page.evaluate(() => window.scrollTo(0, 900));
  await page.waitForTimeout(500);
  assert(await page.evaluate(() => document.querySelector('[data-mobile-bar]').classList.contains('is-visible')), 'barre mobile visible après défilement (page Services)');
  await page.waitForTimeout(600);
  const fab = await page.evaluate(() => { const a = document.querySelector('.theme-fab').getBoundingClientRect(); const b = document.querySelector('[data-mobile-bar]').getBoundingClientRect(); return { fabBottom: Math.round(a.bottom), barTop: Math.round(b.top) }; });
  assert(fab.fabBottom <= fab.barTop, `mobile : bouton sombre au-dessus de la barre d’action (${JSON.stringify(fab)})`);
  await page.tap('.theme-fab'); await page.waitForTimeout(600);
  assert(await page.evaluate(() => document.documentElement.dataset.theme) === 'dark', 'mobile : bouton flottant passe en sombre');
  await page.tap('.theme-fab'); await page.waitForTimeout(600);
  await ctx.close();

  // ---------- Animations réduites et sans JavaScript ----------
  ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  page = await ctx.newPage();
  await page.goto(`${base}index.html`, { waitUntil: 'networkidle' });
  const hidden = await page.$$eval('.reveal', (e) => e.filter((x) => getComputedStyle(x).opacity !== '1').length);
  assert(hidden === 0, 'animations réduites : tout le contenu est visible immédiatement');
  assert((await page.$$eval('[data-count]', (e) => e.map((x) => x.textContent))).join() === `${years},6,1,34`, 'animations réduites : chiffres affichés directement');
  await ctx.close();
  ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, javaScriptEnabled: false });
  page = await ctx.newPage();
  for (const p of PAGES.slice(0, 5)) {
    await page.goto(`${base}${p}.html`, { waitUntil: 'networkidle' });
    const hid = await page.$$eval('.reveal', (e) => e.filter((x) => getComputedStyle(x).opacity !== '1').length);
    assert(hid === 0, `sans JavaScript (${p}) : contenu visible`);
  }
  await ctx.close();

  // ---------- Accessibilité (axe) sur chaque page, clair et sombre, PC et mobile ----------
  const axe = fs.readFileSync(axePath, 'utf8');
  for (const scheme of ['light', 'dark']) {
    for (const vp of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
      ctx = await browser.newContext({ viewport: vp, reducedMotion: 'reduce', bypassCSP: true });
      page = await ctx.newPage();
      if (scheme === 'dark') await page.addInitScript(() => { try { localStorage.setItem('alphanet-theme', 'dark'); } catch (e) {} });
      let total = 0; const detail = [];
      for (const p of PAGES) {
        await page.goto(`${base}${p}.html`, { waitUntil: 'networkidle' });
        await page.addScriptTag({ content: axe });
        const res = await page.evaluate(async () => await window.axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'] }));
        total += res.violations.length;
        res.violations.forEach((v) => detail.push(`${p}: ${v.id} (${v.nodes.slice(0, 2).map((n) => n.target.join(' ')).join(' ; ')})`));
      }
      assert(total === 0, `axe ${scheme} ${vp.width}px : ${total} problème(s) ${detail.join(' | ')}`);
      await ctx.close();
    }
  }
  await browser.close();
})();
