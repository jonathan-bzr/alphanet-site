# Site vitrine — Alphanet Propreté et Services (APS)

Site statique : HTML, CSS et JavaScript, sans dépendance ni outil de compilation.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `index.html` | Page d'accueil : services, méthode, engagements, secteur, contact |
| `mentions-legales.html` | Mentions légales, données personnelles, crédits |
| `assets/css/styles.css` | Couleurs (blanc, bleu, touche de vert), typographie, mises en page |
| `assets/js/main.js` | Menu mobile, barre d'appel rapide, retour en haut, formulaire de devis |
| `assets/img/favicon.svg` | Icône affichée dans l'onglet du navigateur |

## Voir le site

- En ligne (hébergement gratuit GitHub Pages) : https://jonathan-bzr.github.io/alphanet-site/
- En local : double-cliquez sur `index.html`, il s'ouvre dans votre navigateur.

Chaque envoi de modifications sur la branche `main` du dépôt GitHub met le site
en ligne à jour automatiquement (en une à deux minutes).

## Changer les couleurs

Toutes les couleurs sont regroupées en haut de `assets/css/styles.css`
(section « 1. Tokens ») : `--blue-600` pour le bleu principal,
`--navy` pour le bleu marine, `--green-500` pour le vert, etc.

## Remplacer la photo d'accueil

La photo actuelle provient d'Unsplash (licence gratuite, crédit dans les mentions légales).
Pour mettre la vôtre : copiez-la dans `assets/img/` (par ex. `accueil.jpg`), puis dans
`index.html`, remplacez la balise `<img …>` de la section « Accueil » par :

```html
<img src="assets/img/accueil.jpg" width="1280" height="853" alt="Description de la photo" fetchpriority="high">
```

## À compléter avant la mise en ligne

1. **Adresse e-mail** qui recevra les demandes de devis : dans `assets/js/main.js`,
   remplacer `contact@example.com` (ligne `email: ...`). La reporter aussi dans
   `mentions-legales.html`, champ « E-mail ». Tant que l'adresse d'exemple est en place,
   le formulaire invite simplement le visiteur à appeler.
2. **Médiateur de la consommation**, obligatoire dès que vous travaillez avec des particuliers.
3. **Relire les textes** : prestations, « 20+ salariés », secteur d'intervention, « devis gratuit ».

Les champs à compléter sont surlignés en jaune dans la page des mentions légales.

## Mise en ligne

N'importe quel hébergement de site statique convient (OVH, o2switch, Netlify,
GitHub Pages…) : il suffit d'envoyer le contenu du dossier.
