document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('rut');
    const rutErrorMessage = document.getElementById('rut-error-message');

    function formatRut(rut) {
        rut = rut.replace(/[^0-9kK]/g, '').toUpperCase();
        if (rut.length <= 1) return rut;

        const body = rut.slice(0, -1);
        const dv = rut.slice(-1);
        let formatted = '';

        for (let i = 0; i < body.length; i++) {
            if (i > 0 && (body.length - i) % 3 === 0) {
                formatted += '.';
            }
            formatted += body[i];
        }

        return `${formatted}-${dv}`;
    }
    // addDigit
    window.addDigit = function (char) {
      input.value += char;
      input.value = formatRut(input.value);
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
      } else if (/^[0-9kK\-]$/.test(tecla)) {
        simulateClick(tecla);
        addDigit(tecla);
      }
    });
  });
  