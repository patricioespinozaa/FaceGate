document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const confirmationMessage = document.getElementById('confirmation-message');
    const capturedPhoto = document.getElementById('captured-photo');

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
                    })
                    .catch(error => {
                        console.error('❌ Error al enviar RUT:', error);
                        confirmationMessage.textContent = 'Ocurrió un error al enviar tu RUT. Inténtalo de nuevo.';
                    });
            }
        });
    }

    // Polling para mostrar la última foto capturada por el guardia
    setInterval(() => {
        fetch('https://grupo3.juan.cl/facegate/app-ia/get_last_image')
            .then(res => res.json())
            .then(data => {
                if (data.image_url) {
                    capturedPhoto.src = data.image_url + '?' + new Date().getTime(); // evita cache
                    capturedPhoto.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('❌ Error obteniendo imagen:', error);
            });
    }, 3000); // cada 3 segundos
});
