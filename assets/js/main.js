/* ==========================================================================
   ALPHANET SOCIÉTÉ SERVICE — Thème, navigation, chiffres clés, formulaire
   --------------------------------------------------------------------------
   Aucun framework ni service extérieur. Les animations sont coupées si le
   visiteur a demandé à réduire les animations dans les réglages de son appareil.
   ========================================================================== */
(() => {
  'use strict';

  /* Configuration --------------------------------------------------------- */
  const CONFIG = {
    phone: '07 58 34 04 07',
    // ⚠️ À COMPLÉTER : adresse qui recevra les demandes de devis, en deux morceaux
    // (avant et après le @) pour que les robots qui collectent les adresses ne la trouvent pas.
    // Exemple : emailUser: 'contact', emailDomain: 'alphanet.fr'
    emailUser: '',
    emailDomain: '',
  };
  const THEME_COLORS = { light: '#e8f3fd', dark: '#0c1a30' };
  const THEME_KEY = 'alphanet-theme';
  const SVG_NS = 'http://www.w3.org/2000/svg';

  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasObserver = 'IntersectionObserver' in window;
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));

  $$('[data-current-year]').forEach((el) => { el.textContent = String(new Date().getFullYear()); });


  /* Mode clair / sombre ---------------------------------------------------- */
  const themeToggles = $$('[data-theme-toggle]');
  const themeMeta = $('[data-theme-color]');
  const savedTheme = () => {
    try { return window.localStorage.getItem(THEME_KEY); } catch (error) { return null; }
  };

  const applyTheme = (theme) => {
    root.setAttribute('data-theme', theme);
    if (themeMeta) themeMeta.setAttribute('content', THEME_COLORS[theme]);
  };
  applyTheme(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

  // Le bouton est dans le pied de page et dans le menu mobile : tous font la même chose.
  themeToggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      try { window.localStorage.setItem(THEME_KEY, next); } catch (error) { /* choix non mémorisé */ }
      if (document.startViewTransition && !reduceMotion) document.startViewTransition(() => applyTheme(next));
      else applyTheme(next);
    });
  });
  // Un choix fait dans un autre onglet du site est repris ici.
  window.addEventListener('storage', (event) => {
    if (event.key === THEME_KEY) applyTheme(event.newValue === 'dark' ? 'dark' : 'light');
  });


  /* Menu sur téléphone et tablette ----------------------------------------- */
  const header = $('[data-header]');
  const navToggle = $('[data-nav-toggle]');
  const menu = $('[data-menu]');
  const isMenuOpen = () => Boolean(menu && menu.classList.contains('is-open'));

  const setMenu = (open) => {
    if (!navToggle || !menu) return;
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    menu.classList.toggle('is-open', open);
    root.classList.toggle('menu-lock', open);
    menu.inert = !open;
    if (header) header.classList.toggle('menu-open', open);
    if (open) {
      const firstLink = $('a', menu);
      if (firstLink) firstLink.focus({ preventScroll: true });
    }
  };

  if (navToggle && menu && header) {
    navToggle.addEventListener('click', () => setMenu(!isMenuOpen()));
    menu.addEventListener('click', (event) => {
      if (event.target.closest('a')) setMenu(false);
    });
    // Un clic en dehors du menu (sur le voile ou la page) le referme.
    document.addEventListener('click', (event) => {
      if (!isMenuOpen()) return;
      if (menu.contains(event.target) || event.target.closest('.header-inner')) return;
      setMenu(false);
    });
    document.addEventListener('keydown', (event) => {
      if (!isMenuOpen()) return;
      if (event.key === 'Escape') {
        setMenu(false);
        navToggle.focus();
        return;
      }
      // Garde le focus clavier dans l'en-tête tant que le menu est ouvert.
      if (event.key !== 'Tab') return;
      const focusables = $$('a[href], button', header).filter((el) => !el.hidden && el.getClientRects().length > 0);
      const index = focusables.indexOf(document.activeElement);
      if (event.shiftKey && index <= 0) {
        event.preventDefault();
        focusables[focusables.length - 1].focus();
      } else if (!event.shiftKey && index === focusables.length - 1) {
        event.preventDefault();
        focusables[0].focus();
      }
    });
    window.matchMedia('(min-width: 1080px)').addEventListener('change', (event) => {
      if (event.matches) setMenu(false);
    });
    // Retour arrière : la page peut revenir de la mémoire du navigateur avec le menu resté ouvert.
    window.addEventListener('pageshow', (event) => {
      if (event.persisted) setMenu(false);
    });
  }


  /* Apparition douce des blocs au défilement ------------------------------ */
  const revealTargets = $$('.reveal');
  if (hasObserver && !reduceMotion) {
    const revealer = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealTargets.forEach((el) => revealer.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add('is-visible'));
  }


  /* Chiffres clés : comptent jusqu'à leur valeur quand ils apparaissent ----- */
  // Le chiffre des années d'expérience est recalculé à partir de la date de création.
  const yearsSince = (isoDate) => {
    const [y, m, d] = isoDate.split('-').map(Number);
    const now = new Date();
    let years = now.getFullYear() - y;
    if (now < new Date(now.getFullYear(), m - 1, d)) years -= 1;
    return years;
  };
  const counters = $$('[data-count]');
  counters.forEach((el) => {
    const since = el.getAttribute('data-count-since');
    const target = since ? yearsSince(since) : Number(el.getAttribute('data-count'));
    if (!Number.isFinite(target)) return;
    el.textContent = String(target);
    if (!hasObserver || reduceMotion || target < 2) return;
    el.textContent = '0';
    const counter = new IntersectionObserver((entries, observer) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      observer.disconnect();
      const duration = 1100;
      const start = performance.now();
      const tick = (now) => {
        const progress = Math.min(1, (now - start) / duration);
        el.textContent = String(Math.round(target * (1 - Math.pow(1 - progress, 3))));
        if (progress < 1) window.requestAnimationFrame(tick);
      };
      window.requestAnimationFrame(tick);
    }, { threshold: 0.6 });
    counter.observe(el);
  });


  /* En-tête et barre d'action mobile au défilement ------------------------ */
  const mobileBar = $('[data-mobile-bar]');
  const heroActions = $('[data-hero-actions]');
  let ticking = false;

  const onScroll = () => {
    ticking = false;
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);

    if (mobileBar) {
      // Visible une fois les boutons de l'accueil dépassés (ou un peu plus bas sur les autres pages).
      const viewport = window.innerHeight;
      const pastTop = heroActions ? heroActions.getBoundingClientRect().bottom < 0 : window.scrollY > viewport * 0.6;
      const shown = pastTop && !isMenuOpen();
      mobileBar.classList.toggle('is-visible', shown);
      mobileBar.inert = !shown;
    }
  };

  onScroll();
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(onScroll);
  }, { passive: true });
  window.addEventListener('resize', onScroll);


  /* Formulaire de devis ----------------------------------------------------- */
  // Rien n'est envoyé ni enregistré par le site : le formulaire prépare un e-mail
  // dans la messagerie du visiteur, qui choisit de l'envoyer ou non.
  const form = $('[data-quote-form]');
  const typeSelect = $('#f-type');
  const email = CONFIG.emailUser && CONFIG.emailDomain ? `${CONFIG.emailUser}@${CONFIG.emailDomain}` : '';

  const errorMessage = (control) => {
    const { validity } = control;
    if (validity.valid) return '';
    if (validity.valueMissing) return control.tagName === 'SELECT' ? 'Choisissez une prestation.' : 'Ce champ est obligatoire.';
    if (validity.typeMismatch && control.type === 'email') return 'Indiquez une adresse e-mail valide (ex. nom@entreprise.fr).';
    if (validity.patternMismatch && control.type === 'tel') return 'Indiquez un numéro de téléphone valide (ex. 06 12 34 56 78).';
    return control.validationMessage;
  };

  // Affiche (ou retire) le message d'erreur sous le champ ; renvoie true si le champ est valide.
  const checkField = (control) => {
    const field = control.closest('.field');
    if (!field) return control.validity.valid;
    const message = errorMessage(control);
    const slot = $('.field-error', field);
    field.classList.toggle('is-invalid', Boolean(message));
    if (message) control.setAttribute('aria-invalid', 'true');
    else control.removeAttribute('aria-invalid');
    if (slot) slot.textContent = message;
    return !message;
  };

  // Les pages de services renvoient ici avec ?prestation=... : la prestation est alors pré-remplie.
  const PRESTATIONS = {
    'bureaux': 'Bureaux / locaux professionnels',
    'coproprietes': 'Copropriété / parties communes',
    'commerces': 'Commerce / lieu recevant du public',
    'vitrerie': 'Vitrerie',
    'remise-en-etat': 'Remise en état / fin de chantier',
    'apres-sinistre': 'Intervention après sinistre',
  };
  if (typeSelect) {
    const wanted = new URLSearchParams(window.location.search).get('prestation');
    if (wanted && Object.prototype.hasOwnProperty.call(PRESTATIONS, wanted)) typeSelect.value = PRESTATIONS[wanted];
  }

  if (form) {
    const status = $('[data-form-status]', form);

    const showStatus = (message, icon) => {
      if (!status) return;
      const svg = document.createElementNS(SVG_NS, 'svg');
      svg.setAttribute('class', 'ico');
      svg.setAttribute('aria-hidden', 'true');
      const use = document.createElementNS(SVG_NS, 'use');
      use.setAttribute('href', `#i-${icon}`);
      svg.append(use);
      const text = document.createElement('span');
      text.textContent = message;
      status.replaceChildren(svg, text);
      status.hidden = false;
    };

    const recheck = (event) => {
      if (event.target.closest('.field.is-invalid')) checkField(event.target);
    };
    form.addEventListener('input', recheck);
    form.addEventListener('change', recheck);

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const controls = $$('input, select, textarea', form).filter((control) => control.willValidate);
      const invalid = controls.filter((control) => !checkField(control));
      if (invalid.length) {
        invalid[0].focus();
        return;
      }

      if (!email) {
        showStatus(`L’envoi en ligne n’est pas encore activé. Merci de nous appeler au ${CONFIG.phone}.`, 'phone');
        return;
      }

      const data = new FormData(form);
      // Retire les caractères de contrôle (dont les retours à la ligne, sauf dans le message) : rien ne peut être glissé dans l'objet de l'e-mail.
      const field = (name) => String(data.get(name) || '')
        .replace(name === 'message' ? /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g : /[\u0000-\u001F\u007F]/g, ' ')
        .trim();
      const optional = (label, name) => (field(name) ? `${label} : ${field(name)}` : null);

      const subject = ['Demande de devis', field('type'), field('societe') || field('nom')]
        .filter(Boolean)
        .join(' — ');
      const body = [
        'Bonjour,',
        '',
        'Je souhaite obtenir un devis.',
        '',
        `Nom : ${field('nom')}`,
        optional('Société / organisme', 'societe'),
        `Téléphone : ${field('telephone')}`,
        `E-mail : ${field('email')}`,
        `Prestation : ${field('type')}`,
        '',
        field('message'),
        '',
        'Cordialement,',
        field('nom'),
      ].filter((line) => line !== null).join('\r\n');

      window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      showStatus(`Votre messagerie s’ouvre avec votre demande pré-remplie : il ne reste plus qu’à l’envoyer. Si rien ne s’ouvre, appelez-nous au ${CONFIG.phone}.`, 'check');
    });
  }
})();
