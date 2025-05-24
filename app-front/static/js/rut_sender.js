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
                    console.error('❌ Error al cargar imagen por defecto.');
                }
            }
        });
    }

    function enviarFormulario(formData) {
        const data = fetch('http://gate.dcc.uchile.cl:8633/facegate/app-ia/predict', {
            method: 'POST',
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                console.log('✅ Backend response:', data);
                const rut = data.data.rut;        
                updateDecision(data.status === 'success', data.data.nombre, rut, data.message)
            })
            .catch(error => {
                console.error('❌ Error:', error);
            });
    }
});
