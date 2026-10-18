const shareButton = document.querySelector('#share-button');
const shareStatus = document.querySelector('#share-status');

if (navigator.clipboard && window.isSecureContext) {
  shareButton.hidden = false;
  shareButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(new URL('.', location.href).href);
      shareStatus.textContent = 'Enlace copiado.';
    } catch {
      shareStatus.textContent = 'Copiá el enlace desde la barra de direcciones.';
    }
  });
}

if ('IntersectionObserver' in window) {
  const navLinks = [...document.querySelectorAll('.toc nav a')];
  const observer = new IntersectionObserver(entries => {
    const current = entries.filter(entry => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!current) return;
    navLinks.forEach(link => {
      if (link.hash === `#${current.target.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, {rootMargin: '-8% 0px -45% 0px', threshold: [0, .1, .5]});
  document.querySelectorAll('.guide > section').forEach(section => observer.observe(section));
}
