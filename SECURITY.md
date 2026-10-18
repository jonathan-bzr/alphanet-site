# Sécurité

Ce dépôt contient un site vitrine statique (HTML, CSS, JavaScript) : il ne stocke aucune donnée de
visiteur, n'a pas de base de données ni de compte utilisateur, et n'utilise aucun service tiers.

## Signaler un problème

Si vous pensez avoir trouvé une faille, merci de **ne pas la publier** : écrivez à l'entreprise
(coordonnées sur la page Contact du site) ou ouvrez un signalement privé depuis l'onglet
« Security » du dépôt GitHub. Nous répondons dès que possible.

## Mesures en place

- Aucun cookie, aucun traceur, aucune police ou image chargée depuis un autre site.
- Politique de sécurité du contenu (CSP) dans chaque page, sans script ni style « en ligne ».
- Formulaire sans enregistrement : la demande est envoyée par une fonction Cloudflare à la boîte
  contact@ (champs vérifiés côté serveur, champ piège anti-robots, origine contrôlée). Le mot de passe
  de la boîte est un secret Cloudflare, jamais dans le dépôt.
- Sortie automatique du cadre si la page est affichée dans un autre site.
- Aucun secret (mot de passe, clé) dans le dépôt : à ne jamais en ajouter.

## Hébergement

Le site est servi par Cloudflare Pages. Les en-têtes HTTP de sécurité (`Content-Security-Policy`,
`X-Frame-Options`, `Permissions-Policy`, HSTS…) sont définis dans le fichier `_headers`.
