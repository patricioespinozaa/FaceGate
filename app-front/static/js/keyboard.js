document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('rut');
    const rutErrorMessage = document.getElementById('rut-error-message');
  
    // addDigit
    window.addDigit = function (char) {
      input.value += char;
      rutErrorMessage.textContent = '';
      rutErrorMessage.classList.remove('error');
      rutErrorMessage.style.visibility = 'hidden';
    };
  
    // remove
    window.removeDigit = function () {
      input.value = input.value.slice(0, -1);
    };
  
    // dejar igual el inputt
    document.addEventListener('keydown', (event) => {
      let tecla = event.key.toUpperCase();
      if (tecla === 'BACKSPACE') {
        simulateClick('borrar');
        removeDigit();
      } else if (/^[0-9K\-]$/.test(tecla)) {
        simulateClick(tecla);
        addDigit(tecla);
      }
    });
  });
  