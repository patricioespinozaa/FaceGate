document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
    const decisionMessage = document.getElementById('decision-message');
    const capturedPhoto = document.getElementById('captured-photo');
    const cameraContainer = document.getElementById('camera-body-student');

    decisionBox.classList.remove('success', 'error');
    decisionMessage.classList.remove('success', 'error');

    // Lógica para enviar el RUT y la imagen
    if (rutInput) {
        rutInput.addEventListener('keydown', async function (event) {
            if (event.key === 'Enter') {
                let rut = rutInput.value.replace(/[^0-9kK]/g, '');
                const cuerpo = rut.slice(0, -1);
                const dv = rut.slice(-1).toLowerCase();
                const rutValue = `${cuerpo}-${dv}`;
                if (!rutValue) return;

                const formData = new FormData();
                formData.append('rut', rutValue);

                // Estado inicial
                rutInput.disabled = true;
                decisionBox.classList.remove('success', 'error');
                decisionMessage.classList.remove('success', 'error');
                accessLabel.textContent = 'RUT enviado. Verificando...';
                if (cameraContainer) {
                    cameraContainer.innerHTML = '<div class="spinner" id="camera-spinner"></div>';
                }

                try {
                    const storeResponse = await fetch('https://grupo3.juan.cl/facegate/app-ia/store_rut', {
                        method: 'POST',
                        body: formData
                    });

                    const storeData = await storeResponse.json();
                    console.log('✅ RUT guardado:', storeData);

                    const video = document.getElementById('video-stream-student');
                    if (!video || !video.srcObject || video.videoWidth === 0 || video.videoHeight === 0) {
                        console.warn("⚠️ Cámara no disponible o no lista.");
                        return;
                    }

                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                    canvas.toBlob((blob) => {
                        if (!blob) return;

                        const formDataImg = new FormData();
                        formDataImg.append('rut', rutValue);
                        formDataImg.append('image', blob, `captura_${rutValue}.jpg`);

                        fetch('https://grupo3.juan.cl/facegate/app-ia/predict', {
                            method: 'POST',
                            body: formDataImg
                        })
                            .then(() => {
                                console.log('📡 Imagen enviada a /predict');
                            })
                            .catch(err => {
                                console.error('❌ Error al enviar imagen:', err);
                            });
                    }, 'image/jpeg');
                } catch (error) {
                    console.error('❌ Error al enviar RUT:', error);
                    decisionBox.classList.add('error');
                    accessLabel.textContent = 'Error al enviar tu RUT. Intenta de nuevo.';
                }
            }
        });
    }
});
