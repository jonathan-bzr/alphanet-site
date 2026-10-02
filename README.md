# Alphanet Propreté et Services (APS) — site vitrine

Site vitrine d'**Alphanet Propreté et Services (APS)**, entreprise de nettoyage à Montpellier
depuis 2014 : entretien de bureaux, copropriétés et commerces, vitrerie, remise en état
et interventions après sinistre, à Montpellier et dans tout l'Hérault.

[![Site en ligne](https://img.shields.io/badge/site-en%20ligne-1a63d6?style=for-the-badge)](https://jonathan-bzr.github.io/alphanet-site/)
[![Hébergé sur GitHub Pages](https://img.shields.io/badge/h%C3%A9berg%C3%A9%20sur-GitHub%20Pages-0b2545?style=for-the-badge&logo=github)](https://github.com/jonathan-bzr/alphanet-site/deployments)

## Liens

| | |
|---|---|
| **Site en ligne** | https://jonathan-bzr.github.io/alphanet-site/ |
| **Demande de devis** | https://jonathan-bzr.github.io/alphanet-site/#contact |
| **Mentions légales** | https://jonathan-bzr.github.io/alphanet-site/mentions-legales.html |
| **Dépôt GitHub** | https://github.com/jonathan-bzr/alphanet-site |
| **Historique des mises en ligne** | https://github.com/jonathan-bzr/alphanet-site/deployments |

## L'entreprise

| | |
|---|---|
| Raison sociale | ALPHANET PROPRETE ET SERVICES (APS), SAS |
| Activité | Nettoyage courant des bâtiments (APE 81.21Z) |
| Siège | Montpellier (34070) |
| Téléphone | [06 21 63 40 86](tel:+33621634086) |
| Secteur | Montpellier, sa métropole et tout l'Hérault (34) |

## Le site en bref

- **Accueil** : grande photo plein écran, titre court et accès direct au devis.
- **Services** en mosaïque : bureaux, copropriétés, commerces, vitrerie, remise en état,
  après sinistre, plus un encart pour les particuliers. Un clic sur un service ouvre le
  formulaire avec la prestation déjà choisie.
- **Pourquoi nous**, **Méthode** en 4 étapes et **secteur d'intervention**.
- **Formulaire de devis** avec messages d'erreur clairs ; il prépare un e-mail dans la
  messagerie du visiteur (aucune donnée stockée sur le site).
- **Navigation** : en-tête qui se range au défilement, barre de progression de lecture,
  menu mobile plein écran, barre « Appeler / Devis » sur téléphone, bouton retour en haut.
- Adapté aux téléphones, tablettes et ordinateurs ; navigable au clavier ; respecte le
  réglage « réduire les animations » ; aucun cookie de suivi.

## Structure du dépôt

| Fichier | Rôle |
|---|---|
| `index.html` | Page d'accueil |
| `mentions-legales.html` | Mentions légales, données personnelles, crédits |
| `assets/css/styles.css` | Couleurs (blanc, bleu, touche de vert), typographie, mises en page |
| `assets/js/main.js` | Navigation, menu mobile, formulaire de devis |
| `assets/img/favicon.svg` | Icône de l'onglet du navigateur |
| `.nojekyll` | Publie les fichiers tels quels sur GitHub Pages |

Site statique en HTML, CSS et JavaScript, sans dépendance ni outil de compilation.

## Modifier le site

- **Voir le site en local** : double-cliquer sur `index.html`.
- **Couleurs** : toutes regroupées en haut de `assets/css/styles.css` (section « 1. Tokens ») :
  `--blue-600` pour le bleu principal, `--navy` pour le bleu marine, `--green-500` pour le vert.
- **Adresse e-mail du formulaire** : dans `assets/js/main.js`, remplacer `contact@example.com`
  (ligne `email: ...`), puis la reporter dans `mentions-legales.html`. Tant que l'adresse
  d'exemple est en place, le formulaire invite simplement le visiteur à appeler.
- **Photos** : copier vos photos dans `assets/img/` (par ex. `accueil.jpg`) puis, dans
  `index.html`, remplacer la balise `<img …>` concernée en gardant sa classe. Exemple pour
  la grande photo d'accueil :

  ```html
  <img class="hero-bg" src="assets/img/accueil.jpg" width="1920" height="1280" alt="Description de la photo" fetchpriority="high">
  ```

  Pour la grande photo, préférez une image horizontale et lumineuse (au moins 1920 px de
  large) : un voile bleu foncé est ajouté automatiquement à gauche pour garder le titre lisible.

## Mise en ligne

Le site est hébergé gratuitement sur **GitHub Pages**, à partir de la branche `main`.
Chaque modification envoyée sur `main` met le site en ligne à jour automatiquement,
en une à deux minutes.

## À compléter

- [ ] Adresse e-mail de contact (formulaire de devis et mentions légales)
- [ ] Médiateur de la consommation (obligatoire pour les clients particuliers)
- [ ] Relire les textes : prestations, « 20+ salariés », secteur d'intervention, « devis gratuit »

## Crédits

- Photos (licence Unsplash) : hall d'accueil par [Petr](https://unsplash.com/fr/photos/plante-en-pot-verte-sur-carreaux-de-sol-en-ceramique-blanche-HuWm7malJ18),
  nettoyage de bureau par [Towfiqu barbhuiya](https://unsplash.com/fr/photos/mains-qui-nettoient-le-bureau-avec-un-vaporisateur--9gPKrsbGmc),
  entretien des sols par [Toon Lambrechts](https://unsplash.com/fr/photos/personne-passant-la-serpilliere-dans-le-sol-du-couloir-clinique-0FTI9ceTUOc).
- Police de caractères : [Inter](https://rsms.me/inter/) (SIL Open Font License).

© Alphanet Propreté et Services (APS) — tous droits réservés.
