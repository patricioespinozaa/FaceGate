document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
    const capturedPhoto = document.getElementById('captured-photo');

    // Ocultar foto al inicio
    capturedPhoto.style.display = 'none';

    // Lógica: después de enviar RUT, espera y consulta /get_result
    async function checkResult(rut) {
        // Esperar 5 s para dar tiempo a capturar foto y verificar
        await new Promise(resolve => setTimeout(resolve, 5000));

        fetch(`https://grupo3.juan.cl/facegate/app-ia/get_result?rut=${rut}`)
            .then(res => res.json())
            .then(data => {
                console.log('🔄 Resultado:', data);

                if (data.status === 'pending') {
                    accessLabel.textContent = 'Aún procesando...';
                    return;
                }

                // Mostrar la foto capturada
                capturedPhoto.src = 'https://grupo3.juan.cl' + data.uploaded_image_url;
                capturedPhoto.style.display = 'block';

                // Cambiar decisionBox según resultado real
                if (data.status === 'success') {
                    decisionBox.classList.add('success');
                    decisionBox.classList.remove('error');
                    accessLabel.textContent = 'Acceso autorizado';
                } else if (data.status === 'error') {
                    decisionBox.classList.add('error');
                    decisionBox.classList.remove('success');
                    accessLabel.textContent = 'Acceso denegado';
                } else {
                    decisionBox.classList.remove('success', 'error');
                    accessLabel.textContent = 'Verificando...';
                }
            })
            .catch(error => {
                console.error('❌ Error al obtener resultado:', error);
            });
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

                        // Después de guardar, consultar resultado UNA VEZ
                        checkResult(rutValue);

                        // Desbloquear input después de 10 seg para nuevo intento
                        setTimeout(() => {
                            rutInput.disabled = false;
                            rutInput.value = '';
                            accessLabel.textContent = 'Acércate a la cámara';
                            decisionBox.classList.remove('success', 'error');
                            capturedPhoto.style.display = 'none';
                        }, 10000);
                    })
                    .catch(error => {
                        console.error('❌ Error al enviar RUT:', error);
                        decisionBox.classList.add('error');
                        accessLabel.textContent = 'Error al enviar tu RUT. Intenta de nuevo.';
                    });
            }
        });
    }
});
