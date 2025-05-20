document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const messageDiv = document.getElementById('rut-message');

    if (rutInput) {
        rutInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                const rutValue = rutInput.value.trim();
                if (!rutValue) return;

                const formData = new FormData();
                formData.append('rut', rutValue);

                // Buscar input de imagen
                const fileInput = document.getElementById('image-upload');
                const uploadedFile = fileInput?.files[0];

                if (uploadedFile && uploadedFile.type.startsWith('image/')) {
                    // Imagen subida por el usuario
                    formData.append('imagen', uploadedFile);
                    enviarFormulario(formData);
                } else {
                    // Imagen por defecto
                    fetch('/static/img/facegate.png')
                        .then(response => response.blob())
                        .then(blob => {
                            formData.append('imagen', blob, 'facegate.png');
                            enviarFormulario(formData);
                        })
                        .catch(error => {
                            console.error('❌ Error al cargar imagen por defecto:', error);
                            mostrarError('No se pudo cargar la imagen por defecto');
                        });
                }
            }
        });
    }

    function enviarFormulario(formData) {
        const data = fetch('http://localhost:8902/facegate/app-ia/predict', {
            method: 'POST',
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                console.log('✅ Backend response:', data);
                const status = data.status;
                const nombre = data.data.nombre;
                const isVerified = (status === 'success');
                updateDecision(isVerified, nombre);
                messageDiv.textContent = data.message;
                messageDiv.classList.remove('error');
                messageDiv.classList.add('visible', 'success');
                setTimeout(() => {
                    messageDiv.classList.remove('visible', 'success');
                }, 5000);
            })
          /*  .catch(error => {
                console.error('❌ Error:', error);
                mostrarError('Error al enviar');
            });*/
    }

    function mostrarError(msg) {
        messageDiv.textContent = msg;
        messageDiv.classList.remove('success');
        messageDiv.classList.add('visible', 'error');
        setTimeout(() => {
            messageDiv.classList.remove('visible', 'error');
        }, 5000);
    }
});
