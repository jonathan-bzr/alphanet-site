/* Exécuté avant l'affichage de la page :
   1. thème clair / sombre (le site s'ouvre en clair ; le choix du visiteur est mémorisé
      dans son navigateur uniquement), pour éviter un flash au chargement ;
   2. ouverture en haut de page quand on recharge le site ;
   3. protection contre l'affichage du site dans le cadre d'un autre site (clickjacking),
      car GitHub Pages ne permet pas d'envoyer l'en-tête prévu pour cela. */
(function () {
  var root = document.documentElement;
  var theme = null;
  root.classList.add('js');
  try { theme = window.localStorage.getItem('alphanet-theme'); } catch (e) { /* stockage indisponible */ }
  root.setAttribute('data-theme', theme === 'dark' ? 'dark' : 'light');

  // Un rechargement ne ramène pas au milieu de la page : on repart du haut (sauf lien avec #ancre).
  try {
    var entry = window.performance && performance.getEntriesByType('navigation')[0];
    if (entry && entry.type === 'reload' && !window.location.hash && 'scrollRestoration' in history) {
      history.scrollRestoration = 'manual';
      window.addEventListener('load', function () {
        window.scrollTo({ top: 0, behavior: 'instant' });
        window.setTimeout(function () { history.scrollRestoration = 'auto'; }, 300);
      });
    }
  } catch (e) { /* sans importance */ }

  // Anti-clickjacking : si la page est affichée dans un cadre, on la masque et on sort du cadre.
  if (window.top !== window.self) {
    root.style.display = 'none';
    try { window.top.location.href = window.self.location.href; } catch (e) { /* bloqué : la page reste masquée */ }
  }
})();
