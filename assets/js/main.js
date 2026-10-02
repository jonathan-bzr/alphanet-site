/* ==========================================================================
   ALPHANET PROPRETÉ ET SERVICES (APS) — Navigation et formulaire
   --------------------------------------------------------------------------
   Aucun framework : ce fichier fonctionne tel quel dans les navigateurs
   récents. Les effets de mouvement sont coupés si le visiteur a demandé
   à réduire les animations dans les réglages de son appareil.
   ========================================================================== */
(() => {
  'use strict';

  /* Configuration --------------------------------------------------------- */
  const CONFIG = {
    // ⚠️ À REMPLACER : adresse qui recevra les demandes de devis du formulaire.
    email: 'contact@example.com',
    phone: '06 21 63 40 86',
    foundedOn: '2014-04-10', // date de création de la société (registre du commerce)
  };

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasObserver = 'IntersectionObserver' in window;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));


  /* Années d'expérience et année courante (toujours à jour) --------------- */
  const yearsSince = (isoDate) => {
    const start = new Date(`${isoDate}T00:00:00`);
    const now = new Date();
    let years = now.getFullYear() - start.getFullYear();
    const beforeAnniversary = now.getMonth() < start.getMonth()
      || (now.getMonth() === start.getMonth() && now.getDate() < start.getDate());
    if (beforeAnniversary) years -= 1;
    return years;
  };

  $$('[data-years]').forEach((el) => { el.textContent = String(yearsSince(CONFIG.foundedOn)); });
  $$('[data-current-year]').forEach((el) => { el.textContent = String(new Date().getFullYear()); });


  /* Menu mobile plein écran ------------------------------------------------ */
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
    document.body.classList.toggle('nav-open', open);
    if (header) {
      header.classList.toggle('menu-open', open);
      header.classList.remove('is-hidden');
    }
    if (open) {
      const firstLink = $('a', menu);
      if (firstLink) firstLink.focus({ preventScroll: true });
    }
  };

  if (navToggle && menu) {
    navToggle.addEventListener('click', () => setMenu(!isMenuOpen()));
    menu.addEventListener('click', (event) => {
      if (event.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', (event) => {
      if (!isMenuOpen()) return;
      if (event.key === 'Escape') {
        setMenu(false);
        navToggle.focus();
        return;
      }
      // Garde le focus clavier dans le menu ouvert.
      if (event.key !== 'Tab') return;
      const focusables = [navToggle, ...$$('a, button', menu)];
      const index = focusables.indexOf(document.activeElement);
      if (event.shiftKey && index <= 0) {
        event.preventDefault();
        focusables[focusables.length - 1].focus();
      } else if (!event.shiftKey && index === focusables.length - 1) {
        event.preventDefault();
        focusables[0].focus();
      }
    });
    window.matchMedia('(min-width: 1080px)').addEventListener('change', () => setMenu(false));
  }


  /* Lien actif dans les menus selon la section affichée -------------------- */
  const navLinks = $$('.nav-list a[href^="#"], .menu-links a[href^="#"]');
  if (navLinks.length && hasObserver) {
    const ids = ['top', ...new Set(navLinks.map((link) => link.hash.slice(1)))];
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((link) => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    ids.map((id) => document.getElementById(id)).filter(Boolean).forEach((section) => spy.observe(section));
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
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.1 });
    revealTargets.forEach((el) => revealer.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add('is-visible'));
  }


  /* En-tête, progression, barre mobile et « retour en haut » --------------- */
  const hero = $('.hero');
  const mobileBar = $('[data-mobile-bar]');
  const toTop = $('[data-to-top]');
  const heroActions = $('[data-hero-actions]');
  const contactSection = $('#contact');
  let lastY = window.scrollY;
  let ticking = false;

  const setShown = (el, shown) => {
    el.classList.toggle('is-visible', shown);
    el.inert = !shown;
  };

  const onScroll = () => {
    ticking = false;
    const y = window.scrollY;
    const viewport = window.innerHeight;

    if (header) {
      // Transparent sur la grande photo, blanc une fois celle-ci dépassée.
      const solidAt = hero ? Math.max(hero.offsetHeight - header.offsetHeight - 40, 40) : 8;
      header.classList.toggle('is-solid', y > solidAt);
      header.classList.toggle('is-scrolled', y > 8);

      // Se range quand on descend, revient dès que l'on remonte.
      const delta = y - lastY;
      if (Math.abs(delta) > 6) {
        const keyboardInside = Boolean(header.querySelector(':focus-visible'));
        const hide = delta > 0 && y > Math.max(solidAt, 320) && !isMenuOpen() && !keyboardInside;
        header.classList.toggle('is-hidden', hide);
        lastY = y;
      }

      const scrollable = document.documentElement.scrollHeight - viewport;
      header.style.setProperty('--progress', scrollable > 0 ? Math.min(1, y / scrollable).toFixed(4) : '0');
    }

    if (mobileBar) {
      // Visible une fois les boutons du haut dépassés, masquée en arrivant au formulaire.
      const pastHero = heroActions ? heroActions.getBoundingClientRect().bottom < 0 : y > viewport;
      const beforeContact = contactSection ? contactSection.getBoundingClientRect().top > viewport * 0.85 : true;
      const shown = pastHero && beforeContact;
      setShown(mobileBar, shown);
      document.body.classList.toggle('mobile-bar-visible', shown);
    }

    if (toTop) {
      const shown = y > viewport * 1.2;
      toTop.classList.toggle('is-visible', shown);
      toTop.tabIndex = shown ? 0 : -1;
    }
  };

  onScroll();
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(onScroll);
  }, { passive: true });
  window.addEventListener('resize', onScroll);
  if (header) header.addEventListener('focusin', () => header.classList.remove('is-hidden'));

  if (toTop) {
    toTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      const brand = $('.site-header .brand');
      if (brand) brand.focus({ preventScroll: true });
    });
  }


  /* Formulaire de devis ----------------------------------------------------- */
  const form = $('[data-quote-form]');
  const typeSelect = $('#f-type');

  const errorMessage = (control) => {
    const { validity } = control;
    if (validity.valid) return '';
    if (validity.valueMissing) return control.tagName === 'SELECT' ? 'Choisissez une option.' : 'Ce champ est obligatoire.';
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

  // Les cartes de services pré-remplissent le type de prestation.
  $$('[data-service]').forEach((link) => {
    link.addEventListener('click', () => {
      if (!typeSelect) return;
      typeSelect.value = link.dataset.service;
      if (typeSelect.closest('.field.is-invalid')) checkField(typeSelect);
    });
  });

  if (form) {
    const status = $('[data-form-status]', form);
    // Tant que l'adresse ci-dessus est l'adresse d'exemple, aucune demande n'est envoyée.
    const emailReady = !/@example\.(com|fr)$/i.test(CONFIG.email);

    const showStatus = (message, tone) => {
      if (!status) return;
      status.hidden = false;
      status.classList.toggle('form-status--info', tone === 'info');
      status.innerHTML = `<svg class="ico" aria-hidden="true"><use href="#i-${tone === 'info' ? 'phone' : 'check'}"/></svg><span></span>`;
      status.lastElementChild.textContent = message;
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

      if (!emailReady) {
        showStatus(`L’envoi en ligne n’est pas encore activé. Merci de nous appeler au ${CONFIG.phone}.`, 'info');
        return;
      }

      const data = new FormData(form);
      const field = (name) => String(data.get(name) || '').trim();
      const optional = (label, name, suffix = '') => (field(name) ? `${label} : ${field(name)}${suffix}` : null);

      const subject = ['Demande de devis', field('type'), field('societe') || field('nom')]
        .filter(Boolean)
        .join(' — ');
      const body = [
        'Bonjour,',
        '',
        'Je souhaite obtenir un devis pour une prestation de nettoyage.',
        '',
        `Nom : ${field('nom')}`,
        optional('Société / organisme', 'societe'),
        `Téléphone : ${field('telephone')}`,
        `E-mail : ${field('email')}`,
        `Type de prestation : ${field('type')}`,
        optional('Fréquence souhaitée', 'frequence'),
        optional('Surface approximative', 'surface', ' m²'),
        optional('Commune', 'ville'),
        '',
        field('message'),
        '',
        'Cordialement,',
        field('nom'),
      ].filter((line) => line !== null).join('\r\n');

      window.location.href = `mailto:${CONFIG.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      showStatus(`Votre messagerie s’ouvre avec la demande pré-remplie : il ne reste plus qu’à l’envoyer. Si rien ne se passe, appelez-nous au ${CONFIG.phone}.`, 'success');
    });
  }
})();
