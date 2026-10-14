/* Thème clair / sombre, appliqué avant l'affichage de la page (évite un flash).
   Le site s'ouvre en clair ; le choix du visiteur (bouton lune / soleil) est mémorisé
   dans son navigateur uniquement. */
(function () {
  var root = document.documentElement;
  var theme = null;
  root.classList.add('js');
  try { theme = window.localStorage.getItem('alphanet-theme'); } catch (e) { /* stockage indisponible */ }
  root.setAttribute('data-theme', theme === 'dark' ? 'dark' : 'light');
})();
