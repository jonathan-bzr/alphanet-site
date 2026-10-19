# Outils de fabrication du site

Ces fichiers ne font pas partie du site affiché : ils servent à le **générer** et à le **tester**.

## Générer les pages (`generer/`)

Les 6 pages HTML sont fabriquées par `build.py`, qui partage l'en-tête, le menu, le pied de page,
la règle de sécurité (`csp.html`), les données Google (`jsonld.html`) et le texte des mentions
légales (`legal-main.html`).

```bash
python3 outils/generer/build.py . 20261018-7   # racine du dépôt, puis numéro de version ?v=
```

- Toujours modifier `build.py` (ou les fichiers à côté), jamais les `.html` à la main : la
  prochaine génération écraserait la modification. Si une page a été modifiée à la main (par
  exemple via GitHub), reporter d'abord le changement dans `build.py`.
- Après chaque changement du CSS ou du JS, passer un **nouveau numéro de version**
  (`AAAAMMJJ-N`) pour que les navigateurs rechargent les fichiers.

## Tester (`tests/`)

Il faut Node, `playwright` et `axe-core` (`npm i playwright axe-core` dans un dossier de travail).

```bash
python3 -m http.server 8766          # à la racine du dépôt, dans un autre terminal
node outils/tests/suite.js http://127.0.0.1:8766/ <chemin>/axe-core/axe.min.js
```

La suite vérifie liens, menu, formulaire, mode sombre, mobile, accessibilité (axe) et absence
d'erreurs. Tout doit être `OK`.

- `export.js <racine>` : régénère les PNG du logo, les icônes, l'image de partage
  (`og-image.jpg`) et le logo de la signature mail, à partir des SVG (site servi sur le port 8766).
- `fakesmtp.py <fichier.eml>` : faux serveur mail (port 2525) pour tester
  `functions/api/devis.js` en local avec `wrangler pages dev . --binding SMTP_PASS=secret-test
  --binding SMTP_SECURE=off --binding SMTP_HOST=127.0.0.1 --binding SMTP_PORT=2525`.

## Logo (`logo/`)

`final.py` dessine le logo (« A » coupé par un trait de raclette) et écrit les SVG, l'icône
d'onglet et le symbole à coller dans `build.py` (`site-symbol.html`).

```bash
npm pack @fontsource-variable/archivo   # police libre (SIL OFL), puis décompresser
python3 outils/logo/final.py <archivo-latin-wdth-normal.woff2> <dossier de sortie>
```
