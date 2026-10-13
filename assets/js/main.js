/* ==========================================================================
   ALPHANET SOCIÉTÉ SERVICE — Thème, navigation, partenaires, formulaire
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
  const THEME_COLORS = { light: '#e4eaf2', dark: '#0a111e' };
  const THEME_KEY = 'alphanet-theme';
  const SVG_NS = 'http://www.w3.org/2000/svg';

  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasObserver = 'IntersectionObserver' in window;
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));

  $$('[data-current-year]').forEach((el) => { el.textContent = String(new Date().getFullYear()); });


  /* Mode clair / sombre ---------------------------------------------------- */
  const themeToggle = $('[data-theme-toggle]');
  const themeMeta = $('[data-theme-color]');
  const savedTheme = () => {
    try { return window.localStorage.getItem(THEME_KEY); } catch (error) { return null; }
  };

  const applyTheme = (theme) => {
    root.setAttribute('data-theme', theme);
    if (themeMeta) themeMeta.setAttribute('content', THEME_COLORS[theme]);
    if (themeToggle) {
      themeToggle.setAttribute('aria-label', 'Mode sombre');
      themeToggle.setAttribute('aria-pressed', String(theme === 'dark'));
    }
  };
  applyTheme(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      try { window.localStorage.setItem(THEME_KEY, next); } catch (error) { /* choix non mémorisé */ }
      if (document.startViewTransition && !reduceMotion) document.startViewTransition(() => applyTheme(next));
      else applyTheme(next);
    });
  }

  // Tant que le visiteur n'a rien choisi, le site suit le réglage de son appareil.
  const systemDark = window.matchMedia('(prefers-color-scheme: dark)');
  if (systemDark.addEventListener) {
    systemDark.addEventListener('change', (event) => {
      if (!savedTheme()) applyTheme(event.matches ? 'dark' : 'light');
    });
  }


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
  }


  /* Lien actif dans le menu selon la section affichée ---------------------- */
  const navLinks = $$('.nav-list a[href^="#"]');
  if (navLinks.length && hasObserver) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((link) => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['top', ...navLinks.map((link) => link.hash.slice(1))]
      .map((id) => document.getElementById(id))
      .filter(Boolean)
      .forEach((section) => spy.observe(section));
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


  /* Bandeau défilant des partenaires -------------------------------------- */
  // La liste est écrite une seule fois dans la page ; le script la recopie
  // autant de fois que nécessaire pour un défilement continu, sans à-coup.
  const marquee = $('[data-marquee]');
  const marqueeList = marquee ? $('[data-marquee-list]', marquee) : null;
  const marqueeToggle = $('[data-marquee-toggle]');

  if (marquee && marqueeList && !reduceMotion) {
    const track = document.createElement('div');
    track.className = 'marquee-track';
    marqueeList.before(track);
    track.append(marqueeList);
    marquee.classList.add('is-ready');

    const build = () => {
      $$('[data-marquee-clone]', track).forEach((clone) => clone.remove());
      const width = marqueeList.getBoundingClientRect().width;
      if (!width) return;
      const copies = Math.ceil(marquee.clientWidth / width) + 1;
      for (let i = 0; i < copies; i += 1) {
        const clone = marqueeList.cloneNode(true);
        clone.removeAttribute('data-marquee-list');
        clone.setAttribute('data-marquee-clone', '');
        clone.setAttribute('aria-hidden', 'true');
        clone.inert = true;
        track.append(clone);
      }
      track.style.setProperty('--marquee-shift', `${width}px`);
      track.style.setProperty('--marquee-duration', `${Math.max(20, Math.round(width / 42))}s`);
    };

    build();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
    window.addEventListener('load', build); // logos en image : largeur connue une fois chargés
    let resizeTimer = 0;
    let lastWidth = window.innerWidth;
    window.addEventListener('resize', () => {
      if (window.innerWidth === lastWidth) return; // ignore la barre d'adresse mobile
      lastWidth = window.innerWidth;
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(build, 200);
    });

    if (marqueeToggle) {
      marqueeToggle.hidden = false;
      marqueeToggle.addEventListener('click', () => {
        const paused = marquee.classList.toggle('is-paused');
        marqueeToggle.setAttribute('aria-pressed', String(paused));
      });
    }
  }


  /* En-tête et barre d'action mobile au défilement ------------------------ */
  const mobileBar = $('[data-mobile-bar]');
  const heroActions = $('[data-hero-actions]');
  const contactSection = $('#contact');
  let ticking = false;

  const onScroll = () => {
    ticking = false;
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);

    if (mobileBar) {
      // Visible une fois les boutons de l'accueil dépassés, masquée en arrivant au formulaire.
      const viewport = window.innerHeight;
      const pastHero = heroActions ? heroActions.getBoundingClientRect().bottom < 0 : window.scrollY > viewport;
      const beforeContact = contactSection ? contactSection.getBoundingClientRect().top > viewport * 0.85 : true;
      const shown = pastHero && beforeContact && !isMenuOpen();
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

  // Les cartes de services pré-remplissent la prestation.
  $$('[data-service]').forEach((link) => {
    link.addEventListener('click', () => {
      if (!typeSelect) return;
      typeSelect.value = link.dataset.service;
      if (typeSelect.closest('.field.is-invalid')) checkField(typeSelect);
    });
  });

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
      const field = (name) => String(data.get(name) || '').trim();
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
