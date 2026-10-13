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

Une seule page, en cinq parties, pensée pour que les professionnels trouvent vite l'essentiel :

1. **Accueil** : grand fond lumineux, titre, devis et téléphone en un clic.
2. **Services** : six prestations. Un clic sur une carte ouvre le formulaire avec la prestation déjà choisie.
3. **Méthode** : quatre étapes, du premier rendez-vous au suivi qualité.
4. **Partenaires** : bandeau qui défile en continu (pause au survol ou avec le bouton).
5. **Contact** : téléphone et formulaire de devis.

Et aussi : **mode clair / sombre** (bouton lune / soleil en haut, suit le réglage de l'appareil par
défaut), menu et barre « Appeler / Devis » sur téléphone, page **mentions légales et données personnelles**.

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
| `index.html` | Page d'accueil |
| `mentions-legales.html` | Mentions légales, données personnelles, cookies |
| `assets/css/styles.css` | Couleurs (clair et sombre), mise en page |
| `assets/js/theme.js` | Applique le mode clair / sombre avant l'affichage |
| `assets/js/main.js` | Mode sombre, menu, bandeau des partenaires, formulaire |
| `assets/fonts/` | Police Plus Jakarta Sans (licence libre OFL) |
| `assets/img/fond/` | Fonds d'image (version claire et sombre, ordinateur et téléphone) |
| `assets/img/logo/` | Logo : couleur, blanc (fonds foncés), pictogramme, PNG |
| `assets/img/og-image.jpg` | Image affichée quand on partage le lien (WhatsApp, LinkedIn…) |
| `.nojekyll` | Publie les fichiers tels quels sur GitHub Pages |

Site statique en HTML, CSS et JavaScript, sans dépendance ni outil de compilation.

## Modifier le site

- **Partenaires** : dans `index.html`, section « Partenaires », un `<li class="partner">` par
  partenaire. Les cinq noms après Atout-Box sont **provisoires**. Pour mettre un vrai logo, copier
  le fichier dans `assets/img/partenaires/` puis écrire :

  ```html
  <li class="partner"><img src="assets/img/partenaires/nom.svg" alt="Nom du partenaire" height="40"></li>
  ```

- **Adresse e-mail du formulaire** : dans `assets/js/main.js`, remplir `emailUser` (avant le @) et
  `emailDomain` (après le @), puis la reporter dans `mentions-legales.html`. Tant qu'elle est vide,
  le formulaire invite le visiteur à appeler.
- **Couleurs** : en haut de `assets/css/styles.css` (section « 2. Couleurs ») : `--primary` pour le
  bleu, `--accent` pour la touche turquoise ; la deuxième liste concerne le mode sombre.
- **Après chaque modification du CSS ou du JS** : augmenter le numéro `?v=` dans les deux pages
  HTML, pour que les navigateurs prennent la nouvelle version.

## Mise en ligne

Le site est hébergé gratuitement sur **GitHub Pages**, à partir de la branche `main`.
Chaque modification envoyée sur `main` met le site en ligne à jour automatiquement,
en une à deux minutes.

## À compléter

- [ ] Adresse e-mail de contact (formulaire de devis et mentions légales)
- [ ] Vrais partenaires (noms et logos) à la place des noms provisoires
- [ ] Médiateur de la consommation (obligatoire pour les clients particuliers)
- [ ] Vérifier que la raison sociale et le SIREN des mentions légales sont toujours à jour

## Crédits

- Logo et illustrations : réalisés pour Alphanet Société Service.
- Police de caractères : [Plus Jakarta Sans](https://github.com/tokotype/PlusJakartaSans) (SIL Open Font License).

© Alphanet Société Service — tous droits réservés.
