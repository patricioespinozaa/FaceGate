document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const messageDiv = document.getElementById('rut-message');

    if (rutInput) {
        rutInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                const rutValue = event.target.value.trim();
                console.log('Sending RUT:', rutValue);

                fetch('/Facegate/send_rut', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ rut: rutValue })
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Response from backend:', data);
                        messageDiv.textContent = 'Enviado correctamente';
                        messageDiv.classList.remove('success','error');
                        messageDiv.classList.add('visible', 'success');

                        setTimeout(() => {
                            messageDiv.classList.remove('visible', 'success');
                        }, 5000);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        messageDiv.textContent = 'Error al enviar';
                        messageDiv.classList.remove('success','error');
                        messageDiv.classList.add('visible', 'error');

                        setTimeout(() => {
                            messageDiv.classList.remove('visible', 'error');
                        }, 5000);
                    });
            }
        });
    }
});
