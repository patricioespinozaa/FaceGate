document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');

    if (rutInput) {
        rutInput.addEventListener('keydown', async function (event) {
            if (event.key === 'Enter') {
                const rutValue = rutInput.value.trim();
                if (!rutValue) return;

                const formData = new FormData();
                formData.append('rut', rutValue);

                fetch('https://grupo3.juan.cl/facegate/app-ia/store_rut', {
                    method: 'POST',
                    body: formData
                })
                    .then(res => res.json())
                    .then(data => {
                        console.log('✅ RUT guardado:', data);
                        // Opcional: mostrar feedback al alumno
                        alert('RUT enviado. Por favor acércate a la cámara.');
                    })
                    .catch(error => {
                        console.error('❌ Error al enviar RUT:', error);
                    });
            }
        });
    }
});
