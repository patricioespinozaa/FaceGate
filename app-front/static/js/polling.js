document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video-stream');
    const rutInput = document.getElementById('rut');
    const pollingInterval = 3000; // cada 3 segundos
    let fotoEnviada = false;
    async function poll() {
        try {
            // Obtener el último RUT desde el backend
            const response = await fetch('https://grupo3.juan.cl/facegate/app-ia/get_result');
            const result = await response.json();
            const rut = result.rut;

            if (!rut) {
                console.log("⏳ No hay RUT pendiente. Polling continúa...");
                fotoEnviada = false; // Reset flag si no hay RUT
                return;
            }

            // Mostrar RUT en el input del guardia
            rutInput.value = rut;

            // Si ya enviaste foto en este intento, espera solo resultado
            if (fotoEnviada) {
                console.log("⏳ Foto ya enviada, esperando resultado...");

                // Si detecta fin del ciclo, resetea flag para permitir nuevo intento
                if (result.predict_result !== 'pending') {

                    setTimeout(() => {
                        rutInput.value = ""; // Limpia input visible del guardia

                        const decisionBox = document.getElementById('decision-box');
                        const accessLabel = document.getElementById('access-label');
                        const decisionMessage = document.getElementById('decision-message');

                        decisionBox.classList.remove('success', 'error');
                        accessLabel.textContent = "Acércate a la cámara";
                        decisionMessage.textContent = "";
                        decisionMessage.classList.remove('success', 'error');

                    }, 5000);

                    fotoEnviada = false;
                    console.log("🔄 Ciclo finalizado, listo para nuevo RUT.");
                }
                return;
            }

            // Si no es pending, reset flag
            if (result.predict_result !== 'pending') {
                console.log("✅ Intento finalizado, sin envío de foto.");
                fotoEnviada = false;
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

                    if (data.status === 'success') {
                        updateDecision(true, data.data?.nombre ?? "", data.data?.rut ?? "", data.message);
                    } else {
                        updateDecision(false, "", "", data.message);
                    }

                    // Marca como enviada
                    fotoEnviada = true;

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

    // Iniciar polling loop
    setInterval(poll, pollingInterval);
});
