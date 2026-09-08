(() => {
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  const links = [...document.querySelectorAll('.site-nav a')];
  const current = document.body.dataset.page || 'index.html';
  const servicePages = new Set(['perdida-de-peso.html', 'nutricion-deportiva.html', 'nutricion-clinica.html']);
  const activePage = servicePages.has(current) ? 'servicios.html' : current;
  const normalize = (href) => {
    const clean = href.split('#')[0] || 'index.html';
    return clean.endsWith('/') ? 'index.html' : clean;
  };
  links.forEach((link) => {
    if (normalize(link.getAttribute('href') || '') === activePage && !link.classList.contains('nav-cta')) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });
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
  nav?.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 981) closeMenu();
  });
  const mobileBar = document.querySelector('.mobile-contact-bar');
  const updateMobileBar = () => mobileBar?.classList.toggle('is-visible', window.scrollY > 260);
  updateMobileBar();
  window.addEventListener('scroll', updateMobileBar, { passive: true });
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('[data-reveal]');
  if (!reduced && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  }
  const year = document.querySelector('[data-current-year]');
  if (year) year.textContent = String(new Date().getFullYear());
  const form = document.querySelector('[data-contact-form]');
  const status = document.querySelector('[data-form-status]');
  const setError = (input, message) => {
    const row = input?.closest('.form-row');
    const error = input ? document.querySelector(`[data-error-for="${input.name}"]`) : null;
    row?.classList.toggle('invalid', Boolean(message));
    if (error) error.textContent = message || '';
  };
  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = form.elements.name;
    const email = form.elements.email;
    let valid = true;
    if (!name.value.trim()) { setError(name, 'Escribe tu nombre.'); valid = false; } else setError(name, '');
    if (!email.value.trim() || !email.validity.valid) { setError(email, 'Introduce un email válido.'); valid = false; } else setError(email, '');
    if (!valid) {
      status.textContent = 'Revisa los campos marcados. No se ha enviado nada.';
      return;
    }
    status.textContent = 'Demo validada: este formulario no envía ni almacena mensajes.';
    form.reset();
  });
  form?.querySelectorAll('input, textarea').forEach((field) => {
    field.addEventListener('input', () => { if (field.required && field.value.trim()) setError(field, ''); });
  });
})();
