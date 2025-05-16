document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const messageDiv = document.getElementById('rut-message');

    if (rutInput) {
        rutInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                const rutValue = event.target.value;
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
                        messageDiv.style.display = 'block';

                        setTimeout(() => {
                            messageDiv.style.display = 'none';
                            messageDiv.textContent = '';
                        }, 5000);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        messageDiv.textContent = 'Error al enviar';
                        messageDiv.style.display = 'block';

                        setTimeout(() => {
                            messageDiv.style.display = 'none';
                            messageDiv.textContent = '';
                        }, 5000);
                    });
            }
        });
    }
});
