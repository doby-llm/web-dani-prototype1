(() => {
  const root = document.documentElement;
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  const navLinks = [...document.querySelectorAll('.site-nav a[href^="#"]')];
  const sections = [...document.querySelectorAll('main section[id]')];
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const closeMenu = () => {
    document.body.classList.remove('menu-open');
    menuToggle?.setAttribute('aria-expanded', 'false');
    menuToggle?.setAttribute('aria-label', 'Abrir menú');
  };

  menuToggle?.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });

  navLinks.forEach((link) => {
    link.addEventListener('click', () => closeMenu());
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });

  const mobileBar = document.querySelector('.mobile-contact-bar');
  const updateMobileBar = () => mobileBar?.classList.toggle('is-visible', window.scrollY > 260);
  updateMobileBar();
  window.addEventListener('scroll', updateMobileBar, { passive: true });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 860) closeMenu();
  });

  if (!prefersReducedMotion && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    document.querySelectorAll('[data-reveal]').forEach((element) => revealObserver.observe(element));
  } else {
    document.querySelectorAll('[data-reveal]').forEach((element) => element.classList.add('is-visible'));
  }

  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = `#${entry.target.id}`;
        navLinks.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === id));
      });
    }, { rootMargin: '-32% 0px -58% 0px', threshold: 0 });
    sections.forEach((section) => sectionObserver.observe(section));
  }

  const form = document.querySelector('[data-contact-form]');
  const status = document.querySelector('[data-form-status]');
  const requiredFields = [
    { input: form?.elements.name, message: 'Escribe tu nombre.' },
    { input: form?.elements.email, message: 'Introduce un email válido.' },
  ];

  const setFieldError = (input, message) => {
    if (!input) return;
    const row = input.closest('.form-row');
    const error = document.querySelector(`[data-error-for="${input.name}"]`);
    row?.classList.toggle('invalid', Boolean(message));
    if (error) error.textContent = message || '';
  };

  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    let valid = true;
    requiredFields.forEach(({ input, message }) => {
      const isEmail = input?.type === 'email';
      const invalid = !input?.value.trim() || (isEmail && !input.validity.valid);
      setFieldError(input, invalid ? message : '');
      if (invalid) valid = false;
    });
    if (!valid) {
      status.textContent = 'Revisa los campos marcados antes de continuar.';
      status.className = 'form-status form-status-error';
      return;
    }
    status.textContent = 'Gracias. Este prototipo no envía ni almacena mensajes todavía.';
    status.className = 'form-status form-status-success';
    form.reset();
  });

  form?.querySelectorAll('input, select, textarea').forEach((input) => {
    input.addEventListener('input', () => {
      if (input.required && input.value.trim()) setFieldError(input, '');
    });
  });

  const year = document.querySelector('[data-current-year]');
  if (year) year.textContent = String(new Date().getFullYear());

  // These links intentionally return to the contact section until Daniel's real channels are configured.
  document.querySelectorAll('[data-contact-action]').forEach((link) => {
    link.addEventListener('click', () => {
      window.setTimeout(() => document.querySelector('#name')?.focus({ preventScroll: true }), prefersReducedMotion ? 0 : 450);
    });
  });
})();
