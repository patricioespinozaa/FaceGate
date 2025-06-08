document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');

    if (rutInput) {
        rutInput.addEventListener('keydown', async function (event) {
            if (event.key === 'Enter') {
                const rutValue = rutInput.value.trim();
                if (!rutValue) return;

                const video = document.getElementById('video-stream');
                if (!video || video.readyState < 2) {
                    console.warn("La cámara no está lista.");
                    return;
                }

                const blob = await capturarFoto(video);
                if (!blob) return;

                mostrarImagen(blob);

                const formData = new FormData();
                formData.append('rut', rutValue);
                formData.append('imagen', blob, 'captura.jpeg');

                enviarFormulario(formData);
            }
        });
    }

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
                    console.error("No se pudo crear el blob de la imagen");
                    resolve(null);
                } else {
                    resolve(blob);
                }
            }, 'image/jpeg');
        });
    }

    function mostrarImagen(blob) {
        const cameraBody = document.getElementById('camera-body-camara');
        cameraBody.innerHTML = '';

        const img = document.createElement('img');
        img.src = URL.createObjectURL(blob);
        img.id = 'captured-image';
        img.style.maxWidth = '100%';
        img.style.maxHeight = '100%';
        img.style.objectFit = 'contain';
        img.style.display = 'block';

        cameraBody.appendChild(img);
    }

    function enviarFormulario(formData) {
        fetch('https://grupo3.juan.cl/facegate/app-ia/predict', {
            method: 'POST',
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                console.log('✅ Backend response:', data);
                const rut = data.data.rut;
                updateDecision(data.status === 'success', data.data.nombre, rut, data.message);
            })
            .catch(error => {
                console.error('❌ Error al enviar al backend:', error);
            });
    }
});