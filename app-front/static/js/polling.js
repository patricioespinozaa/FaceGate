document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video-stream');
    const rutInput = document.getElementById('rut');
    const pollingInterval = 3000; // cada 3 segundos

    async function poll() {
        try {
            // Obtener el último RUT desde el backend
            const response = await fetch('https://grupo3.juan.cl/facegate/app-ia/get_result');
            const result = await resResult.json();
            const rut = result.rut;

            if (!rut) {
                console.log("⏳ No hay RUT pendiente. Polling continúa...");
                return;
            }

            // Mostrar RUT en el input del guardia
            rutInput.value = rut;

            // Verificar estado: solo enviar foto si está pending
            if (result.predict_result !== 'pending') {
                console.log("✅ Ya verificado, no se envía más foto.");
                return;
            }

            // Verificar que la cámara esté lista
            if (!video || video.readyState < 2) {
                console.warn("⚠️ Cámara no lista todavía.");
                return;
            }

            // Capturar foto
            const blob = await capturarFoto(video);
            if (!blob) return;

            // Enviar foto + RUT a /predict
            const formData = new FormData();
            formData.append('rut', rut);
            formData.append('imagen', blob, 'captura.jpeg');

            fetch('https://grupo3.juan.cl/facegate/app-ia/predict', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    console.log('✅ Respuesta backend:', data);
                    updateDecision(
                        data.status === 'success',
                        data.data.nombre,
                        data.data.rut,
                        data.message
                    );

                    // setTimeout 5 seg para no tener que refrescar la vista
                    setTimeout(() => {
                        rutInput.value = ""; // Limpia input visible del guardia

                        // Reiniciar caja de decisión:
                        const decisionBox = document.getElementById('decision-box');
                        const accessLabel = document.getElementById('access-label');
                        const decisionMessage = document.getElementById('decision-message');

                        decisionBox.classList.remove('success', 'error');
                        accessLabel.textContent = "Acércate a la cámara";
                        decisionMessage.textContent = "";
                        decisionMessage.classList.remove('success', 'error');
                    }, 5000); // espera 5 segundos antes de limpiar

                })
                .catch(error => {
                    console.error('❌ Error en predict:', error);
                });

        } catch (error) {
            console.error('❌ Error en polling:', error);
        }
    }

    // Función para capturar foto de la cámara
    function capturarFoto(video) {
        return new Promise(resolve => {
            const videoWidth = video.videoWidth;
            const videoHeight = video.videoHeight;
            const squareSize = Math.min(videoWidth, videoHeight);
            const finalWidth = squareSize + 10;
            const finalHeight = squareSize;
            const cropX = (videoWidth - finalWidth) / 2;
            const cropY = (videoHeight - finalHeight) / 2;

            const canvas = document.createElement('canvas');
            canvas.width = finalWidth;
            canvas.height = finalHeight;

            canvas.getContext('2d').drawImage(video, cropX, cropY, finalWidth, finalHeight, 0, 0, finalWidth, finalHeight);
            canvas.toBlob(function (blob) {
                if (!blob) {
                    console.error("❌ No se pudo crear el blob de la imagen");
                    resolve(null);
                } else {
                    resolve(blob);
                }
            }, 'image/jpeg');
        });
    }

    // Iniciar el polling
    setInterval(poll, pollingInterval);
});
