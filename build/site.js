// Disclosure behaviour for the presentational components: any button with aria-controls toggles its target's `hidden`.
// Escape or a click outside closes what is open; focus returns to the button.
const open = new Set();

function setOpen(button, target, state) {
  button.setAttribute('aria-expanded', String(state));
  target.hidden = !state;
  state ? open.add(button) : open.delete(button);
  if (state && target.getAttribute('role') === 'dialog') target.querySelector('button, a')?.focus();
}

document.addEventListener('click', (event) => {
  const button = event.target.closest('button[aria-controls]');
  const close = event.target.closest('[data-close]');
  if (close) {
    for (const b of open) if (document.getElementById(b.getAttribute('aria-controls'))?.contains(close)) { setOpen(b, document.getElementById(b.getAttribute('aria-controls')), false); b.focus(); }
    return;
  }
  if (button) {
    const target = document.getElementById(button.getAttribute('aria-controls'));
    if (target && target.hasAttribute('hidden') !== undefined) {
      for (const b of [...open]) if (b !== button) setOpen(b, document.getElementById(b.getAttribute('aria-controls')), false);
      setOpen(button, target, button.getAttribute('aria-expanded') !== 'true');
      return;
    }
  }
  for (const b of [...open]) {
    const target = document.getElementById(b.getAttribute('aria-controls'));
    if (!target.contains(event.target)) setOpen(b, target, false);
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  for (const b of [...open]) { setOpen(b, document.getElementById(b.getAttribute('aria-controls')), false); b.focus(); }
});
