/* Progressive enhancement: core course information never depends on JavaScript. */
(() => {
  const header = document.querySelector('header');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#nav');
  if (header && toggle && nav) {
    header.classList.add('has-js');
    toggle.hidden = false;
    const setOpen = open => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? '关闭导航菜单' : '展开导航菜单');
      nav.classList.toggle('is-open', open);
    };
    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', event => { if (event.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false); toggle.focus();
      }
    });
    matchMedia('(min-width: 651px)').addEventListener('change', event => { if (event.matches) setOpen(false); });
  }
  const input = document.querySelector('#faq-search');
  if (input) {
    document.querySelector('.filter-tools').hidden = false;
    const items = Array.from(document.querySelectorAll('.faq-item'));
    const groups = Array.from(document.querySelectorAll('.faq-group'));
    const update = () => {
      const query = input.value.trim().toLocaleLowerCase();
      let count = 0;
      items.forEach(item => {
        const match = item.textContent.toLocaleLowerCase().includes(query);
        item.hidden = !match;
        if (match) count++;
      });
      groups.forEach(group => { group.hidden = !group.querySelector('.faq-item:not([hidden])'); });
      document.querySelector('#faq-count').textContent = `显示 ${count} / ${items.length} 个问题`;
      document.querySelector('#faq-empty').hidden = count !== 0;
    };
    input.addEventListener('input', update);
    document.querySelector('#faq-clear').addEventListener('click', () => { input.value = ''; update(); input.focus(); });
    update();
  }
  const filter = document.querySelector('#episode-filter');
  if (filter) {
    document.querySelector('.episode-tools').hidden = false;
    const episodes = Array.from(document.querySelectorAll('.episode'));
    const update = () => {
      let count = 0;
      episodes.forEach(episode => {
        const match = filter.value === 'all' || episode.dataset.type === filter.value;
        episode.hidden = !match; if (match) count++;
      });
      document.querySelector('#episode-count').textContent = `显示 ${count} / ${episodes.length} 期`;
    };
    filter.addEventListener('change', update); update();
  }
  // Expand native disclosures for print, then restore the reader's previous state.
  let printStates = [];
  addEventListener('beforeprint', () => {
    printStates = Array.from(document.querySelectorAll('details')).map(item => [item, item.open]);
    printStates.forEach(([item]) => { item.open = true; });
  });
  addEventListener('afterprint', () => printStates.forEach(([item, open]) => { item.open = open; }));
})();
