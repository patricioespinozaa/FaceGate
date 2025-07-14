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

    function formatRut(rut) {
        rut = rut.replace(/[^0-9kK]/g, '').toUpperCase();
        if (rut.length <= 1) return rut;

        const body = rut.slice(0, -1);
        const dv = rut.slice(-1);
        let formatted = '';

        for (let i = 0; i < body.length; i++) {
            if (i > 0 && (body.length - i) % 3 === 0) {
                formatted += '.';
            }
            formatted += body[i];
        }

        return `${formatted}-${dv}`;
    }


    function resetUI(){
        videoStream.style.display = 'block';
        const faceGuide = document.createElement('div');
        const videoElement = cameraContainer.querySelector('#video-stream')
        faceGuide.className = 'face-guide-overlay';
        cameraContainer.insertBefore(faceGuide,videoElement)

        if (videoStream.paused) {
            videoStream.play().catch(err => console.warn("No se pudo reanudar el stream:", err));
        }

        const img = cameraContainer.querySelector('img');
        if (img) img.remove();
        const spinner = document.getElementById('camera-spinner');
        if (spinner) spinner.remove();

        fetch('https://grupo3.juan.cl/facegate/app-ia/reset_guard_view', {
            method: 'POST'
        });
        //reset de rut
        rutInput.disabled = false;
        rutInput.value = '';
        // y de estilos 
        decisionBox.classList.remove('success', 'error');
        decisionMessage.classList.remove('success', 'error');
        decisionMessage.textContent = '';
        accessLabel.textContent = 'Acércate a la cámara';

        //reset de la foto 
        if (capturedPhoto) {
            capturedPhoto.style.display = 'none';
        }
        rutErrorMessage.textContent = '';
        rutErrorMessage.classList.remove('error');
        rutErrorMessage.style.visibility = 'hidden';

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

                    videoStream.style.display = 'none';

                    const existingImg = cameraContainer.querySelector('img');
                    if (existingImg) existingImg.remove();

                    const existingSpinner = document.getElementById('camera-spinner');
                    if (!existingSpinner) {
                        const spinner = document.createElement('div');
                        spinner.id = 'camera-spinner';
                        spinner.className = 'spinner';
                        cameraContainer.appendChild(spinner);
                    }
                    // Cambia el decision box a estado "En proceso"
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

    rutInput.addEventListener('input', function (e) {
        rutErrorMessage.textContent = '';
        rutErrorMessage.classList.remove('error');
        rutErrorMessage.style.visibility = 'hidden';

        const raw = rutInput.value.replace(/[^0-9kK]/g, '');
        const formatted = formatRut(raw);
        rutInput.value = formatted;
        rutInput.setSelectionRange(formatted.length, formatted.length);
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
