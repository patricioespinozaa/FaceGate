document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
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
                        rutInput.disabled = true;

                        // Cambia el decision box a estado "En proceso"
                        decisionBox.classList.remove('success', 'error');
                        accessLabel.textContent = 'RUT enviado. Verificando...';

                        // Empieza el polling de imagen SOLO después de enviar
                        startPolling();

                        // ✅ Desbloquear input después de 10 seg para permitir nuevo intento
                        setTimeout(() => {
                            rutInput.disabled = false;
                            rutInput.value = ''; // Limpiar el campo para reusar
                            accessLabel.textContent = 'Acércate a la cámara';
                            decisionBox.classList.remove('success', 'error');
                            clearInterval(pollingIntervalId); // Detener polling anterior
                            pollingIntervalId = null; // Reset flag
                            capturedPhoto.style.display = 'none'; // ocultar imagen anterior
                        }, 10000);

                    })
                    .catch(error => {
                        console.error('❌ Error al enviar RUT:', error);
                        decisionBox.classList.add('error');
                        confirmationMessage.textContent = 'Error al enviar tu RUT. Inténtalo de nuevo.';
                    });
            }
        });
    }
});
