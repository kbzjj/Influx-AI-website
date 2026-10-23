/* Ordinary form submissions are local demos. Custom API clients require review. */
document.addEventListener('submit', (event) => {
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  if (!form.reportValidity()) return;
  const wrapper = form.closest('.w-form');
  let feedback = wrapper?.querySelector('.w-form-done');
  if (feedback) {
    const failure = wrapper.querySelector('.w-form-fail');
    if (failure) failure.style.display = 'none';
    form.style.display = 'none';
  } else {
    feedback = form.querySelector('[data-local-preview-feedback]');
    if (!feedback) {
      feedback = document.createElement('p');
      feedback.dataset.localPreviewFeedback = '';
      form.append(feedback);
    }
  }
  feedback.textContent = 'Local preview only. Your message has not been sent.';
  feedback.setAttribute('role', 'status');
  feedback.style.display = 'block';
}, true);
