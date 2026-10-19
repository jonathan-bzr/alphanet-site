# Site Alphanet Group : consignes pour Claude

## Le client
- marcello, gérant d'Alphanet Group (nettoyage professionnel, Montpellier). Écrit en français et
  tutoie : répondre en français, simplement, sans jargon, étape par étape quand il doit agir.
- La sécurité compte beaucoup pour lui (données personnelles, champs du site, code).
- Il modifie peu lui-même : les changements sont faits directement sur `main` (pas de PR), il
  vérifie en rechargeant https://alphanet-group.fr (en ligne 1 à 2 minutes après un push).
- Ne jamais saisir un mot de passe ou un moyen de paiement à sa place : il le fait lui-même.

## Le site
- Site statique : 6 pages (`index`, `entreprise`, `services`, `engagements`, `contact`,
  `mentions-legales`), `assets/`, `functions/api/devis.js` (envoi du formulaire).
- Pages **générées** par `outils/generer/build.py` : modifier le générateur, pas les `.html`.
  Mode d'emploi complet : `outils/README.md`.
- Après un changement CSS/JS : nouveau `?v=AAAAMMJJ-N`, régénérer, lancer `outils/tests/suite.js`
  (tout `OK`), puis `git push` sur la branche de travail **et** sur `main`.
- Hébergement : Cloudflare Pages (projet `alphanet-site`, déploie `main` automatiquement).
  Domaine `alphanet-group.fr` chez OVH, DNS chez Cloudflare. `alphanet.fr` appartient à un tiers
  (expire le 15/06/2027).
- Mail : boîte Zimbra OVH contact@alphanet-group.fr (IMAP/SMTP `ssl0.ovh.net`, 993/465).
- Formulaire : POST `/api/devis` → SMTP OVH → contact@. Mot de passe dans le secret Cloudflare
  `SMTP_PASS` (jamais dans le dépôt). Un changement de secret ne s'applique qu'au déploiement
  suivant. Sans secret ou en cas d'erreur, le site propose l'e-mail pré-rempli.

## Règles à respecter
- Marque : « Alphanet Group ». Raison sociale (mentions légales seulement) : ALPHANET PROPRETE ET
  SERVICES, SAS, RCS 801 134 065 Montpellier. Téléphone : 07 58 34 04 07.
- Zone : accueil « Occitanie » ; ailleurs « principalement dans l'Hérault (34), partout en
  Occitanie et dans le Sud de la France » ; pied de page « Occitanie et Sud de la France ».
- 6 services : Bureaux et Hôtellerie mis en avant, puis Copropriétés, Commerces, Vitrerie,
  Remise en état (inclut l'après sinistre).
- Aucune section partenaires, aucun nom de partenaire. Ne jamais inventer chiffres,
  certifications, clients ou avis.
- Aucun service tiers (polices, images, statistiques, cartes) : tout est hébergé sur le site,
  CSP stricte avec Trusted Types (pas de `innerHTML`, pas de script ni style en ligne).
  Ajouter un tiers impose de modifier la CSP (`csp.html` + `_headers`) et les mentions légales.
- Style voulu : professionnel, sobre, vivant mais pas « IA » (pas de dégradés ni d'étincelles,
  mail de devis en noir et blanc). Logo : « A » coupé d'un trait de raclette, bleu marine
  `#0b1f3a` + bleu `#1f5ad6` (`outils/logo/final.py`).
- S'inspirer de sites concurrents sans jamais copier textes, images, code ou logos.
- Ne jamais ajouter de secret (mot de passe, clé) au dépôt : il est public.
