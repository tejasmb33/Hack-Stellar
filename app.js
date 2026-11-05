'use strict';
const search = document.querySelector('#search');
const domain = document.querySelector('#domain');
const source = document.querySelector('#source');
const cards = [...document.querySelectorAll('.problem-card')];
function normalize(value) { return value.toLowerCase().normalize('NFKD').replace(/[–—−]/g, '-').replace(/\s+/g, ' ').trim(); }
function filterProblems() {
  const query = normalize(search.value);
  let count = 0;
  for (const card of cards) {
    const match = normalize(card.dataset.search).includes(query) && (!domain.value || card.dataset.domains.split('|').includes(domain.value)) && (!source?.value || card.dataset.source === source.value);
    card.hidden = !match;
    if (match) count++;
  }
  document.querySelector('#result-count').textContent = `Showing ${count} of ${cards.length} problem statements`;
  document.querySelector('#empty').hidden = count !== 0;
}
function resetFilters() { search.value = ''; domain.value = ''; if (source) source.value = ''; filterProblems(); search.focus(); }
if (search) {
  const showAll = () => {search.value = ''; domain.value = ''; if (source) source.value = ''; filterProblems();};
  showAll();
  addEventListener('pageshow', showAll);
  search.addEventListener('input', filterProblems);
  domain.addEventListener('change', filterProblems);
  source?.addEventListener('change', filterProblems);
  document.querySelector('.filter-toolbar').addEventListener('submit', event => event.preventDefault());
  document.querySelector('#reset').addEventListener('click', event => {event.preventDefault(); resetFilters();});
  document.querySelector('#empty-reset').addEventListener('click', resetFilters);
}
const floating = document.querySelector('.floating-register');
const heroRegister = document.querySelector('#hero-register');
let passed = false, atRegistration = false;
function updateFloating() {
  passed = heroRegister.getBoundingClientRect().bottom < 0;
  const registrationRect = document.querySelector('#registration').getBoundingClientRect();
  atRegistration = registrationRect.top < innerHeight && registrationRect.bottom > 0;
  const style = getComputedStyle(floating);
  const right = parseFloat(style.right) || 16;
  const bottom = parseFloat(style.bottom) || 16;
  const width = floating.offsetWidth || (innerWidth < 600 ? 176 : 194);
  const height = floating.offsetHeight || 52;
  const candidate = {left: innerWidth - right - width - 8, right: innerWidth - right + 8, top: innerHeight - bottom - height - 8, bottom: innerHeight - bottom + 8};
  const blocked = [...document.querySelectorAll('.logo-safe, .judge-body, .preview-row, .faq-list summary')].some(node => {
    const rect = node.getBoundingClientRect();
    return rect.width > 0 && rect.left < candidate.right && rect.right > candidate.left && rect.top < candidate.bottom && rect.bottom > candidate.top;
  });
  floating.hidden = !passed || atRegistration || blocked;
}
if (heroRegister) {
  let floatingFrame = false;
  addEventListener('scroll', () => {
    if (!floatingFrame) {floatingFrame = true; requestAnimationFrame(() => {floatingFrame = false; updateFloating();});}
  }, {passive: true});
  addEventListener('resize', updateFloating);
  new IntersectionObserver(([entry]) => { passed = !entry.isIntersecting && entry.boundingClientRect.bottom < 0; updateFloating(); }).observe(heroRegister);
  new IntersectionObserver(([entry]) => { atRegistration = entry.isIntersecting; updateFloating(); }).observe(document.querySelector('#registration'));
}
const signal = document.querySelector('#signal');
signal?.addEventListener('click', () => {
  const expanded = signal.getAttribute('aria-expanded') === 'true';
  signal.setAttribute('aria-expanded', String(!expanded));
  document.querySelector('#signal-message').textContent = expanded ? 'SIGNAL / AWAITING CONTACT' : 'SOS / EVEN LIGHT NEEDS A LITTLE HELP.';
});
const timeNote = document.querySelector('#time-note');
timeNote?.addEventListener('click', () => {
  const expanded = timeNote.getAttribute('aria-expanded') === 'true';
  timeNote.setAttribute('aria-expanded', String(!expanded));
  document.querySelector('#time-message').textContent = expanded ? 'A matter of perspective.' : 'Proper time and coordinate time need not agree.';
});
