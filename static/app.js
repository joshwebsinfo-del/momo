document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.querySelector('.menu-toggle');
  const primaryNav = document.getElementById('primary-nav');

  if (menuToggle && primaryNav) {
    menuToggle.addEventListener('click', () => {
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!expanded));
      primaryNav.classList.toggle('open', !expanded);
    });
  }

  const themeToggle = document.querySelector('.theme-toggle');
  const root = document.documentElement;
  const storedTheme = localStorage.getItem('love-journey-theme') || 'light';
  document.body.setAttribute('data-theme', storedTheme);
  root.setAttribute('data-theme', storedTheme);
  if (themeToggle) {
    themeToggle.textContent = storedTheme === 'dark' ? '🌙' : '☀️';
    themeToggle.addEventListener('click', () => {
      const nextTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', nextTheme);
      root.setAttribute('data-theme', nextTheme);
      localStorage.setItem('love-journey-theme', nextTheme);
      themeToggle.textContent = nextTheme === 'dark' ? '🌙' : '☀️';
    });
  }

  const cards = document.querySelectorAll('.card, .feature-card, .hero-card, .stat-card');
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 90}ms`;
    card.classList.add('is-visible');
  });
});
