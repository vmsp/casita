(() => {
  function toEl(html) {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstChild;
  }

  window.addEventListener('DOMContentLoaded', () => {
    for (const el of document.querySelectorAll('*[data-cable-click]')) {
      el.addEventListener('click', async () => {
        const compEl = el.closest('*[data-cable-url]');
        const fun = el.dataset.cableClick;
        const url = compEl.dataset.cableUrl;

        const resp = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ fun, state: {} }),
        });
        const newComp = resp.json();

        //compEl.replaceWith();
      });
    }
  });
})();
