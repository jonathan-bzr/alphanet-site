# Alphanet Group — site vitrine

Site vitrine d'**Alphanet Group**, entreprise de nettoyage professionnel à Montpellier
depuis 2014 : entretien de bureaux, copropriétés et commerces, vitrerie, remise en état
et après sinistre, principalement dans l'Hérault (34), en Occitanie et dans le Sud.

[![Site en ligne](https://img.shields.io/badge/site-en%20ligne-1f5ad6?style=for-the-badge)](https://alphanet-group.fr/)
[![Hébergé sur Cloudflare Pages](https://img.shields.io/badge/h%C3%A9berg%C3%A9%20sur-Cloudflare%20Pages-0c1a2e?style=for-the-badge&logo=cloudflare)](https://alphanet-group.fr/)

## Liens

| | |
|---|---|
| **Site en ligne** | https://alphanet-group.fr/ |
| **Demande de devis** | https://alphanet-group.fr/#contact |
| **Mentions légales et données personnelles** | https://alphanet-group.fr/mentions-legales.html |
| **Dépôt GitHub** | https://github.com/jonathan-bzr/alphanet-site |
| **Historique des mises en ligne** | https://github.com/jonathan-bzr/alphanet-site/deployments |

## L'entreprise

| | |
|---|---|
| Nom commercial | Alphanet Group |
| Raison sociale | ALPHANET PROPRETE ET SERVICES (APS), SAS |
| Activité | Nettoyage courant des bâtiments (APE 81.21Z) |
| Siège | Montpellier (34070) |
| Téléphone | [07 58 34 04 07](tel:+33758340407) |
| Secteur | Principalement l'Hérault (34), mais aussi toute l'Occitanie et le Sud de la France |

## Le site en bref

Cinq pages, un menu en haut de chaque page (sur téléphone : bouton « menu » et barre « Appeler / Devis ») :

| Page | Contenu |
|---|---|
| **Accueil** (`index.html`) | Titre, devis et téléphone en un clic, chiffres clés, mission et valeurs, aperçu des six services et des engagements |
| **Entreprise** (`entreprise.html`) | Histoire, mission, valeurs, méthode de travail, zone d'intervention |
| **Services** (`services.html`) | Les six prestations en détail : bureaux, hôtellerie (mis en avant), copropriétés, commerces, vitrerie, remise en état et après sinistre |
| **Engagements** (`engagements.html`) | Service suivi, équipes stables, environnement, confidentialité |
| **Contact** (`contact.html`) | Téléphone, étapes après la demande, formulaire de devis (la prestation se pré-remplit depuis la page Services) |

Et aussi : **mode clair / sombre** (bouton rond lune / soleil en bas à droite de l'écran, toujours visible ; le site s'ouvre en clair) et la page
**mentions légales et données personnelles**.

## Sécurité et données personnelles

- **Aucun service tiers** : la police et les images sont hébergées sur le site. Aucun cookie,
  aucune mesure d'audience, aucune publicité : pas de bandeau de consentement à afficher.
- **Règle de sécurité dans chaque page** (`Content-Security-Policy`) : le navigateur refuse tout
  script, style ou fichier qui ne vient pas du site lui-même, et bloque l'envoi du formulaire vers
  un autre site.
- **Formulaire sans stockage** : la demande est envoyée par une petite fonction Cloudflare
  (`functions/api/devis.js`) directement à la boîte contact@, en e-mail mis en forme. Rien n'est
  enregistré sur le site. Protections : champs vérifiés côté serveur, champ piège et délai minimum
  contre les robots, envoi accepté uniquement depuis le site. Si l'envoi échoue, le visiteur peut
  passer par sa propre messagerie.
- **Règle renforcée** : la même règle impose aussi un contrôle strict de tout code injecté
  (`require-trusted-types-for`). Aucun script ni style n'est écrit « en ligne » dans les pages.
- **Protection contre l'affichage dans un cadre** : si un autre site essaie d'afficher le vôtre
  dans un cadre (technique du « clickjacking »), la page se masque et sort du cadre
  (voir `assets/js/theme.js`).
- **Formulaire assaini** : les caractères de contrôle (retours à la ligne cachés, etc.) sont retirés
  des champs avant de préparer l'e-mail, et le pré-remplissage par lien n'accepte qu'une liste fixe de valeurs.
- Connexion chiffrée (HTTPS) assurée par Cloudflare.
- **En-têtes de sécurité** : le fichier `_headers` envoie la politique de sécurité, l'anti-cadre,
  `Permissions-Policy`, HSTS, etc. sur chaque page servie par Cloudflare Pages.
- **Référencement** : titres et descriptions propres à chaque page, données structurées
  (entreprise locale, services, fil d'Ariane), `sitemap.xml` et `robots.txt`.
- Voir aussi `SECURITY.md` (comment signaler un problème).
- Le point le plus important de votre côté : activer la **double authentification** sur le
  compte GitHub, sur le compte Cloudflare et sur le compte OVHcloud. Dans les réglages du dépôt, protéger la branche `main` contre les suppressions et les
  réécritures forcées (Settings > Branches).

## Structure du dépôt

| Fichier | Rôle |
|---|---|
| `index.html`, `entreprise.html`, `services.html`, `engagements.html`, `contact.html` | Les cinq pages |
| `mentions-legales.html` | Mentions légales, données personnelles, cookies |
| `sitemap.xml` | Liste des pages pour les moteurs de recherche |
| `assets/css/styles.css` | Couleurs (clair et sombre), formes, mise en page |
| `assets/js/theme.js` | Applique le mode clair / sombre avant l'affichage |
| `assets/js/main.js` | Mode sombre, menu, chiffres clés, formulaire |
| `assets/fonts/` | Police Plus Jakarta Sans (licence libre OFL) |
| `assets/img/fond/` | Fonds d'image (version claire et sombre, ordinateur et téléphone) |
| `assets/img/logo/` | Logo « A » au trait de raclette : couleur, blanc (fonds foncés), noir (une couleur), pictogramme, SVG et PNG |
| `assets/img/og-image.jpg` | Image affichée quand on partage le lien (WhatsApp, LinkedIn…) |
| `functions/api/devis.js` | Envoi du formulaire de devis vers contact@ (Cloudflare) |
| `outils/` | Générateur des pages, tests et logo (mode d'emploi dans `outils/README.md`) |
| `CLAUDE.md` | Consignes du projet pour Claude |
| `.nojekyll` | Publie les fichiers tels quels (ancienne adresse GitHub Pages) |

Site statique en HTML, CSS et JavaScript, sans dépendance ni outil de compilation.
Le menu et le pied de page sont écrits dans chaque page : pour les changer, modifier les six fichiers `.html`.

## Modifier le site

- **Textes** : directement dans les fichiers `.html` (un titre = une balise `<h2>` ou `<h3>`).
- **Chiffres de l'accueil** : bloc « Alphanet en bref » (accueil et page Entreprise). Le chiffre des
  années d'expérience se met à jour tout seul chaque année (date de création : 10 avril 2014). Ne mettre
  que des chiffres exacts.
- **Zone d'intervention** : textes des pages Entreprise et Contact (« principalement dans l'Hérault (34), mais aussi partout en Occitanie et dans les autres régions du Sud »).
- **Adresse e-mail du formulaire** : dans `assets/js/main.js`, `emailUser` (avant le @) et
  `emailDomain` (après le @), à reporter aussi dans `mentions-legales.html` et `functions/api/devis.js`.
  Le mot de passe de la boîte contact@ n'est **jamais** dans le code : il est rangé dans Cloudflare
  (Workers & Pages > alphanet-site > Paramètres > Variables et secrets, secret `SMTP_PASS`). Si le mot de
  passe de la boîte change, il faut le changer aussi à cet endroit, sinon le formulaire repasse en
  mode « messagerie du visiteur ».
- **Couleurs** : en haut de `assets/css/styles.css` (section « 2. Couleurs ») : `--primary` pour le
  bleu, `--accent` pour la touche turquoise ; la deuxième liste concerne le mode sombre.
- **Formes** : `.chip-drop` (pastille en forme de goutte) et `.bulle` (cadre au coin pointu, avec une étincelle)
  dans `assets/css/styles.css`. À utiliser avec modération.
- **Après chaque modification du CSS ou du JS** : augmenter le numéro `?v=` dans les six pages
  HTML, pour que les navigateurs prennent la nouvelle version.

## Mise en ligne

Le site est hébergé gratuitement sur **Cloudflare Pages** (projet `alphanet-site`), à partir de la branche `main`,
avec le nom de domaine **alphanet-group.fr** (acheté chez OVHcloud, DNS gérés par Cloudflare).
Chaque modification envoyée sur `main` met le site en ligne à jour automatiquement,
en une à deux minutes. Les en-têtes de sécurité sont dans `_headers`.

## À compléter

- [x] Adresse e-mail de contact : contact@alphanet-group.fr (formulaire et mentions légales, boîte Zimbra chez OVHcloud)
- [x] Nom de domaine : alphanet-group.fr
- [ ] Déclarer le site dans Google Search Console
- [ ] Relire les textes des pages (histoire, valeurs, détail des services, engagements) et corriger ce qui ne correspond pas à la réalité
- [ ] Certifications éventuelles (ISO 9001, Qualipropre, FEP...), à afficher avec leur logo officiel
- [ ] Chiffres supplémentaires exacts (sites entretenus, agents, clients) et photos réelles des interventions
- [ ] Médiateur de la consommation (obligatoire pour les clients particuliers ; le formulaire propose « Particulier (domicile) »)
- [ ] Vérifier que la raison sociale et le SIREN des mentions légales sont toujours à jour

## Crédits

- Logo et illustrations : réalisés pour Alphanet Group. Le texte du logo est dessiné avec la police Archivo (licence libre SIL Open Font License), transformée en formes : aucune police à charger.
- Police de caractères : [Plus Jakarta Sans](https://github.com/tokotype/PlusJakartaSans) (SIL Open Font License).

© Alphanet Group — tous droits réservés.
