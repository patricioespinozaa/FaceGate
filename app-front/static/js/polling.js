document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video-stream');
    const rutInput = document.getElementById('rut');
    const pollingInterval = 3000; // cada 3 segundos
    let fotoEnviada = false;

    async function poll() {
        try {
            // Pedir el último RUT pendiente:
            const response = await fetch('https://grupo3.juan.cl/facegate/app-ia/get_last_rut');
            const result = await response.json();
            const rut = result.rut;

            if (!rut) {
                console.log("⏳ No hay RUT pendiente. Polling continúa...");
                fotoEnviada = false;
                return;
            }

            rutInput.value = rut;

            // Si ya envió foto para este RUT, no la vuelva a enviar:
            if (fotoEnviada) return;

            // Verificar cámara lista:
            if (!video || video.readyState < 2) {
                console.warn("⚠️ Cámara no lista todavía.");
                return;
            }

            // Capturar foto:
            const blob = await capturarFoto(video);
            if (!blob) return;

            // Enviar a /predict:
            const formData = new FormData();
            formData.append('rut', rut);
            formData.append('imagen', blob, 'captura.jpeg');

            fetch('https://grupo3.juan.cl/facegate/app-ia/predict', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    console.log('✅ Respuesta /predict:', data);
                    fotoEnviada = true;

                    updateDecision(
                        data.status === 'success',
                        data.data?.nombre ?? '',
                        data.images.db_url,   // pasa URL completa
                        data.message
                    );

                    fotoEnviada = true;

                    // Limpia input del Guardia después de unos segundos
                    setTimeout(() => {
                        rutInput.value = "";
                        fotoEnviada = false;
                    }, 5000);
                })
                .catch(error => {
                    console.error('❌ Error en /predict:', error);
                });

        } catch (error) {
            console.error('❌ Error en polling Guardia:', error);
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
