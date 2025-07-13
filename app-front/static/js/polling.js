document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video-stream');
    const rutInput = document.getElementById('rut');
    const pollingInterval = 3000; // cada 3 segundos
    const timeout = 20000;
    let fotoEnviada = false;

    async function poll() {
        try {
            const resetResponse = await fetch('https://grupo3.juan.cl/facegate/app-ia/should_reset_guard');
            const resetData = await resetResponse.json();

            if (resetData.reset) {
                console.log('🔄 Reiniciando interfaz del guardia...');

                //reset rut 
                rutInput.value = '';
                fotoEnviada = false;

                //reset stream
                if (video) {
                    const capturedPhoto = document.getElementById('captured-photo');
                    if (capturedPhoto) {
                        capturedPhoto.src = '';
                        capturedPhoto.style.display = 'none';
                    }
                    video.style.display = 'block';
                }
                //reset overlay 
                const cameraContainer = document.getElementById('camera-body-camara');
                const faceGuide = document.createElement('div');
                const videoElement = cameraContainer.querySelector('#video-stream');
                faceGuide.className = 'face-guide-overlay';
                cameraContainer.insertBefore(faceGuide, videoElement);

                //reset spinner
                const ucampusContainer = document.getElementById('camera-body-ucampus');
                if (ucampusContainer) {
                    ucampusContainer.innerHTML = '<div class="spinner" id="camera-spinner"></div>';
                }

                //reset mensaje decision
                const accessLabel = document.getElementById('access-label');
                const decisionBox = document.getElementById('decision-box');
                const decisionMessage = document.getElementById('decision-message');

                if (accessLabel) accessLabel.textContent = "Espera la respuesta";
                if (decisionBox) decisionBox.classList.remove('success', 'error');
                if (decisionMessage) {
                    decisionMessage.textContent = "";
                    decisionMessage.classList.remove('success', 'error');
                }

                return; 
            }

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
            fotoEnviada = true;

            // Verificar cámara lista:
            if (!video || video.readyState < 2) {
                console.warn("⚠️ Cámara no lista todavía.");
                fotoEnviada = false;
                return;
            }

            // Capturar foto:
            const blob = await capturarFoto(video);
            if (!blob) {
                fotoEnviada = false;
                return;
            }

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

                    const capturedPhoto = document.getElementById('captured-photo');
                    if (capturedPhoto) {
                        capturedPhoto.src = 'https://grupo3.juan.cl' + data.images.uploaded_url;
                        capturedPhoto.style.display = 'block';
                        video.style.display = 'none';
                        document.querySelectorAll('.face-guide-overlay').forEach(el => {
                            el.style.display = 'none';
                        });
                    }

                    if (data.status === 'success') {
                        updateDecision(true, data.data?.nombre ?? "", data.data?.rut ?? "", data.message);
                    } else {
                        updateDecision(false, data.data?.nombre ?? "", data.data?.rut ?? "", data.message);
                    }

                    // Limpia input del Guardia después de unos segundos
                    //setTimeout(() => {
                    //    rutInput.value = "";
                    //    fotoEnviada = false;
                        
                        // Limpiar contenedor de la foto de la DB
                    //    const ucampusContainer = document.getElementById('camera-body-ucampus');
                    //    if (ucampusContainer) {
                    //        ucampusContainer.innerHTML = '';
                    //    }
                    //    if (capturedPhoto) {
                    //        capturedPhoto.src = "";
                    //        capturedPhoto.style.display = 'none';
                    //        video.style.display = 'block';
                    //    }

                        // Restaurar mensaje default
                    //    const accessLabel = document.getElementById('access-label');
                    //    const decisionBox = document.getElementById('decision-box');
                    //    const decisionMessage = document.getElementById('decision-message');

                    //    if (accessLabel) accessLabel.textContent = "Acércate a la cámara";
                    //    if (decisionBox) decisionBox.classList.remove('success', 'error');
                    //    if (decisionMessage) {
                    //        decisionMessage.textContent = "";
                    //        decisionMessage.classList.remove('success', 'error');
                    //    }
                    //}, timeout);
                })
                .catch(error => {
                    console.error('❌ Error en /predict:', error);
                    fotoEnviada = false;
                });

        } catch (error) {
            console.error('❌ Error en polling Guardia:', error);
            fotoEnviada = false;
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
