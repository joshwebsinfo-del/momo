document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('[data-smooth]');
  buttons.forEach((button) => button.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' })));

  const menuToggle = document.querySelector('.menu-toggle');
  const primaryNav = document.getElementById('primary-nav');

  if (menuToggle && primaryNav) {
    menuToggle.addEventListener('click', () => {
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', String(!expanded));
      primaryNav.classList.toggle('open', !expanded);
    });
  }
});
