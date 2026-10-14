# Alphanet Société Service — site vitrine

Site vitrine d'**Alphanet Société Service**, entreprise de nettoyage professionnel à Montpellier
depuis 2014 : entretien de bureaux, copropriétés et commerces, vitrerie, remise en état
et interventions après sinistre, à Montpellier et dans tout l'Hérault.

[![Site en ligne](https://img.shields.io/badge/site-en%20ligne-1f5ad6?style=for-the-badge)](https://jonathan-bzr.github.io/alphanet-site/)
[![Hébergé sur GitHub Pages](https://img.shields.io/badge/h%C3%A9berg%C3%A9%20sur-GitHub%20Pages-0c1a2e?style=for-the-badge&logo=github)](https://github.com/jonathan-bzr/alphanet-site/deployments)

## Liens

| | |
|---|---|
| **Site en ligne** | https://jonathan-bzr.github.io/alphanet-site/ |
| **Demande de devis** | https://jonathan-bzr.github.io/alphanet-site/#contact |
| **Mentions légales et données personnelles** | https://jonathan-bzr.github.io/alphanet-site/mentions-legales.html |
| **Dépôt GitHub** | https://github.com/jonathan-bzr/alphanet-site |
| **Historique des mises en ligne** | https://github.com/jonathan-bzr/alphanet-site/deployments |

## L'entreprise

| | |
|---|---|
| Nom commercial | Alphanet Société Service |
| Raison sociale | ALPHANET PROPRETE ET SERVICES (APS), SAS |
| Activité | Nettoyage courant des bâtiments (APE 81.21Z) |
| Siège | Montpellier (34070) |
| Téléphone | [07 58 34 04 07](tel:+33758340407) |
| Secteur | Montpellier, sa métropole et tout l'Hérault (34) |

## Le site en bref

Cinq pages, un menu en haut de chaque page (sur téléphone : bouton « menu » et barre « Appeler / Devis ») :

| Page | Contenu |
|---|---|
| **Accueil** (`index.html`) | Titre, devis et téléphone en un clic, chiffres clés, mission et valeurs, aperçu des six services et des engagements |
| **Entreprise** (`entreprise.html`) | Histoire, mission, valeurs, méthode de travail, zone d'intervention |
| **Services** (`services.html`) | Les six prestations en détail : bureaux, copropriétés, commerces, vitrerie, remise en état, après sinistre |
| **Engagements** (`engagements.html`) | Service suivi, équipes stables, environnement, confidentialité |
| **Contact** (`contact.html`) | Téléphone, étapes après la demande, formulaire de devis (la prestation se pré-remplit depuis la page Services) |

Et aussi : **mode clair / sombre** (bouton lune / soleil en haut ; le site s'ouvre en clair) et la page
**mentions légales et données personnelles**.

## Sécurité et données personnelles

- **Aucun service tiers** : la police et les images sont hébergées sur le site. Aucun cookie,
  aucune mesure d'audience, aucune publicité : pas de bandeau de consentement à afficher.
- **Règle de sécurité dans chaque page** (`Content-Security-Policy`) : le navigateur refuse tout
  script, style ou fichier qui ne vient pas du site lui-même, et bloque l'envoi du formulaire vers
  un autre site.
- **Formulaire sans stockage** : il prépare un e-mail dans la messagerie du visiteur, rien n'est
  enregistré sur le site. L'adresse de réception est écrite en deux morceaux dans le code pour
  échapper aux robots qui collectent les adresses.
- Connexion chiffrée (HTTPS) assurée par GitHub Pages.
- Le point le plus important de votre côté : activer la **double authentification** sur le
  compte GitHub qui publie le site.

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
| `assets/img/logo/` | Logo : couleur, blanc (fonds foncés), pictogramme, PNG |
| `assets/img/og-image.jpg` | Image affichée quand on partage le lien (WhatsApp, LinkedIn…) |
| `.nojekyll` | Publie les fichiers tels quels sur GitHub Pages |

Site statique en HTML, CSS et JavaScript, sans dépendance ni outil de compilation.
Le menu et le pied de page sont écrits dans chaque page : pour les changer, modifier les six fichiers `.html`.

## Modifier le site

- **Textes** : directement dans les fichiers `.html` (un titre = une balise `<h2>` ou `<h3>`).
- **Chiffres de l'accueil** : bloc « Alphanet en bref » (accueil et page Entreprise). Le chiffre des
  années d'expérience se met à jour tout seul chaque année (date de création : 10 avril 2014). Ne mettre
  que des chiffres exacts.
- **Communes de la zone d'intervention** : pages Entreprise et Contact, une ligne `<li>` par commune.
- **Adresse e-mail du formulaire** : dans `assets/js/main.js`, remplir `emailUser` (avant le @) et
  `emailDomain` (après le @), puis la reporter dans `mentions-legales.html`. Tant qu'elle est vide,
  le formulaire invite le visiteur à appeler.
- **Couleurs** : en haut de `assets/css/styles.css` (section « 2. Couleurs ») : `--primary` pour le
  bleu, `--accent` pour la touche turquoise ; la deuxième liste concerne le mode sombre.
- **Formes** : `.chip-drop` (pastille en forme de goutte) et `.bulle` (cadre au coin pointu, avec une étincelle)
  dans `assets/css/styles.css`. À utiliser avec modération.
- **Après chaque modification du CSS ou du JS** : augmenter le numéro `?v=` dans les six pages
  HTML, pour que les navigateurs prennent la nouvelle version.

## Mise en ligne

Le site est hébergé gratuitement sur **GitHub Pages**, à partir de la branche `main`.
Chaque modification envoyée sur `main` met le site en ligne à jour automatiquement,
en une à deux minutes.

## À compléter

- [ ] Adresse e-mail de contact (formulaire de devis et mentions légales)
- [ ] Relire les textes des pages (histoire, valeurs, détail des services, engagements) et corriger ce qui ne correspond pas à la réalité
- [ ] Certifications éventuelles (ISO 9001, Qualipropre, FEP...), à afficher avec leur logo officiel
- [ ] Chiffres supplémentaires exacts (sites entretenus, agents, clients) et photos réelles des interventions
- [ ] Médiateur de la consommation (obligatoire pour les clients particuliers)
- [ ] Vérifier que la raison sociale et le SIREN des mentions légales sont toujours à jour

## Crédits

- Logo et illustrations : réalisés pour Alphanet Société Service.
- Police de caractères : [Plus Jakarta Sans](https://github.com/tokotype/PlusJakartaSans) (SIL Open Font License).

© Alphanet Société Service — tous droits réservés.
