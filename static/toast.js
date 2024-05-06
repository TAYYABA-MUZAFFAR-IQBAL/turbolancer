// Create the toastParent element if it doesn't exist
let toastParent = document.getElementById('toast_parent-TurboLancer');
let activeToasts = [];

function toast(type, text, padding = 0) {
  console.log('triggered...');

  // Create the toastParent if it doesn't exist
  if (!toastParent) {
    toastParent = document.createElement('div');
    toastParent.id = 'toast_parent-TurboLancer';
    document.body.appendChild(toastParent);
  }

  const toastElement = document.createElement('div');
  toastElement.classList.add('toast-TurboLancer');
  toastElement.setAttribute('role', 'alert');
  toastElement.id = type;

  const toastContent = document.createElement('div');
  toastContent.classList.add('toast-contentt');
  toastElement.appendChild(toastContent);

  const toastIcon = document.createElement('div');
  toastIcon.classList.add('toast-icont');
  toastContent.appendChild(toastIcon);

  const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  icon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  icon.setAttribute('width', '16');
  icon.setAttribute('height', '16');
  icon.setAttribute('fill', 'currentColor');
  icon.setAttribute('viewBox', '0 0 16 16');
  toastIcon.appendChild(icon);

  const iconPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  if (type === 's') {
    iconPath.setAttribute('d', 'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z');
  } else if (type === 'd') {
    iconPath.setAttribute('d', 'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z');
  } else if (type === 'w') {
    iconPath.setAttribute('d', 'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z');
  }
  icon.appendChild(iconPath);

  const toastText = document.createElement('div');
  toastText.classList.add('toasttextt');
  toastContent.appendChild(toastText);

  const textNode = document.createElement('p');
  textNode.textContent = text;
  textNode.style.paddingTop = `${padding}px`
  toastText.appendChild(textNode);

  toastParent.appendChild(toastElement);

  const toastTimeout = setTimeout(() => {
    toastElement.classList.add('go');
    setTimeout(() => {
      toastElement.classList.remove('go');
      toastElement.classList.add('none');
      toastParent.removeChild(toastElement);
      activeToasts = activeToasts.filter(t => t.element !== toastElement);

      // Remove the toastParent if it's empty
      if (!toastParent.hasChildNodes()) {
        document.body.removeChild(toastParent);
        toastParent = null;
      }
    }, 400);
  }, 4000); // Display the toast for 4 seconds

  activeToasts.push({ element: toastElement, timeout: toastTimeout });
}