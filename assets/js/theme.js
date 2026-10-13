/* Thème clair / sombre, appliqué avant l'affichage de la page (évite un flash).
   Choix du visiteur mémorisé dans son navigateur uniquement ; sinon, réglage de l'appareil. */
(function () {
  var root = document.documentElement;
  var theme = null;
  root.classList.add('js');
  try { theme = window.localStorage.getItem('alphanet-theme'); } catch (e) { /* stockage indisponible */ }
  if (theme !== 'light' && theme !== 'dark') {
    theme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  root.setAttribute('data-theme', theme);
})();
