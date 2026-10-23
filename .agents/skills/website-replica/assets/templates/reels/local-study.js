/* Local study adapter. Keep the original layout and Webflow/GSAP interactions.
 * Forms are a front-end demonstration and do not contact the original business.
 */
document.addEventListener('submit', (event) => {
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  if (!form.reportValidity()) return;
  const wrapper = form.closest('.w-form');
  const success = wrapper?.querySelector('.w-form-done');
  if (success) {
    success.textContent = 'Local preview only. Your message has not been sent.';
    success.style.display = 'block';
    success.setAttribute('role', 'status');
    form.style.display = 'none';
  }
}, true);
