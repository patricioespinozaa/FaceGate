document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
    const decisionMessage = document.getElementById('decision-message');
    const capturedPhoto = document.getElementById('captured-photo');
    const cameraContainer = document.getElementById('camera-body-student');
    const takePicBtn = document.getElementById('take-pic');
    const videoStream = document.getElementById('video-stream-student');
    const rutErrorMessage = document.getElementById('rut-error-message');

    let takingPhoto = false;

    decisionBox.classList.remove('success', 'error');
    decisionMessage.classList.remove('success', 'error');

    function resetUI() {
        videoStream.style.display = 'block';
        cameraContainer.appendChild(videoStream)

        fetch('https://grupo3.juan.cl/facegate/app-ia/reset_guard_view', {
            method: 'POST'
        });

        rutInput.disabled = false;
        rutInput.value = '';
        decisionBox.classList.remove('success', 'error');
        decisionMessage.classList.remove('success', 'error');
        decisionMessage.textContent = '';
        accessLabel.textContent = 'Acércate a la cámara';

        if (capturedPhoto) capturedPhoto.style.display = 'none';

        rutErrorMessage.textContent = '';
        rutErrorMessage.classList.remove('error');
        rutErrorMessage.style.visibility = 'hidden';

        if (!videoStream.srcObject) {
            console.log("entro al if")
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    videoStream.srcObject = stream;
                    videoStream.style.display = 'block';
                })
                .catch(err => console.error('Error al acceder a la cámara:', err));
        }

        takePicBtn.querySelector('#take-pic-label').textContent = 'Tomar foto';
        takingPhoto = false;
    }

    function captureAndSend() {
        let rut = rutInput.value.replace(/[^0-9kK]/g, '');
        const cuerpo = rut.slice(0, -1);
        const dv = rut.slice(-1).toLowerCase();
        const rutValue = `${cuerpo}-${dv}`;
        if (!rutValue) return;

        const canvas = document.createElement('canvas');
        canvas.width = videoStream.videoWidth;
        canvas.height = videoStream.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoStream, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('rut', rutValue);
            formData.append('image', blob, `captura_${rutValue}.jpg`);

            fetch('https://grupo3.juan.cl/facegate/app-ia/store_rut', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    console.log('✅ RUT guardado:', data);
                    rutInput.disabled = true;

                    if (cameraContainer) {
                        cameraContainer.innerHTML = '<div class="spinner" id="camera-spinner"></div>';
                    }

                    decisionBox.classList.remove('success', 'error');
                    decisionMessage.classList.remove('success', 'error');
                    accessLabel.textContent = 'RUT enviado. Verificando...';
                })
                .catch(error => {
                    console.error('❌ Error al enviar RUT:', error);
                    decisionBox.classList.add('error');
                    accessLabel.textContent = 'Error al enviar tu RUT. Intenta de nuevo.';
                });
        }, 'image/jpeg');
    }

    takePicBtn.addEventListener('click', function () {
        if (!takingPhoto) {
            const rawRut = rutInput.value.trim();
            if (!rawRut) {
                rutErrorMessage.textContent = "Ingresa tu RUT antes de tomarte la foto";
                rutErrorMessage.classList.add('error');
                rutErrorMessage.style.visibility = 'visible';
                return;
            }
            rutErrorMessage.textContent = '';
            rutErrorMessage.classList.remove('error');
            captureAndSend();
        } else {
            resetUI();
        }
    });

    rutInput.addEventListener('input', () => {
        rutErrorMessage.textContent = '';
        rutErrorMessage.classList.remove('error');
        rutErrorMessage.style.visibility = 'hidden';
    });

    rutInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && !takingPhoto) {
            takePicBtn.click();
        }
    });

    document.addEventListener('verificacion-finalizada', () => {
        takePicBtn.querySelector('#take-pic-label').textContent = 'Retomar foto';
        takingPhoto = true;
    });
});
