document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const confirmationMessage = document.getElementById('confirmation-message');
    const capturedPhoto = document.getElementById('captured-photo');

    // Logica para recibir la imagen tomada
    let pollingIntervalId = null;
    capturedPhoto.style.display = 'none';
    function startPolling() {
        // Solo si no hay uno activo
        if (pollingIntervalId !== null) return;

        pollingIntervalId = setInterval(() => {
            fetch('https://grupo3.juan.cl/facegate/app-ia/get_last_image')
                .then(res => res.json())
                .then(data => {
                    if (data.image_url) {
                        capturedPhoto.src = 'https://grupo3.juan.cl' + data.image_url + '?' + new Date().getTime();
                        capturedPhoto.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('❌ Error obteniendo imagen:', error);
                });
        }, 3000);
    }

    // Lógica para enviar el RUT
    if (rutInput) {
        rutInput.addEventListener('keydown', async function (event) {
            if (event.key === 'Enter') {
                const rutValue = rutInput.value.trim();
                if (!rutValue) return;

                const formData = new FormData();
                formData.append('rut', rutValue);

                fetch('https://grupo3.juan.cl/facegate/app-ia/store_rut', {
                    method: 'POST',
                    body: formData
                })
                    .then(res => res.json())
                    .then(data => {
                        console.log('✅ RUT guardado:', data);
                        confirmationMessage.textContent = 'RUT enviado. Por favor espera mientras se verifica.';
                        rutInput.disabled = true;

                        // Empieza el polling de imagen SOLO después de enviar
                        startPolling();

                        // ✅ Desbloquear input después de 3 seg para permitir nuevo intento
                        setTimeout(() => {
                            rutInput.disabled = false;
                            rutInput.value = ''; // Limpiar el campo para reusar
                            clearInterval(pollingIntervalId); // Detener polling anterior
                            pollingIntervalId = null; // Reset flag
                            capturedPhoto.style.display = 'none'; // ocultar imagen anterior
                        }, 5000);

                    })
                    .catch(error => {
                        console.error('❌ Error al enviar RUT:', error);
                        confirmationMessage.textContent = 'Error al enviar tu RUT. Inténtalo de nuevo.';
                    });
            }
        });
    }
});
