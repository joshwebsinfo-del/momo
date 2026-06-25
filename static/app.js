document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.querySelector('.menu-toggle');
  const primaryNav = document.getElementById('primary-nav');

  if (menuToggle && primaryNav) {
    menuToggle.addEventListener('click', () => {
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!expanded));
      primaryNav.classList.toggle('open', !expanded);
    });

    primaryNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        menuToggle.setAttribute('aria-expanded', 'false');
        primaryNav.classList.remove('open');
      });
    });
  }

  const themeToggle = document.querySelector('.theme-toggle');
  const storedTheme = localStorage.getItem('love-journey-theme') || 'light';
  document.body.setAttribute('data-theme', storedTheme);
  document.documentElement.setAttribute('data-theme', storedTheme);

  if (themeToggle) {
    themeToggle.textContent = storedTheme === 'dark' ? '🌙' : '☀️';
    themeToggle.addEventListener('click', () => {
      const nextTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', nextTheme);
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('love-journey-theme', nextTheme);
      themeToggle.textContent = nextTheme === 'dark' ? '🌙' : '☀️';
    });
  }
});
