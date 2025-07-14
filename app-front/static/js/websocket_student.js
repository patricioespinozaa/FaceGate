document.addEventListener('DOMContentLoaded', function () {
    const socket = io('https://grupo3.juan.cl', {
        path: '/socket.io',
        transports: ['websocket']
    });

    socket.on('connect', () => {
        console.log('✅ WebSocket conectado (estudiante)');
    });

    socket.onAny((event, ...args) => {
        console.log('[WS] Evento recibido:', event, args);
    });

    socket.on('resultado_verificacion', (data) => {
        const rutInput = document.getElementById('rut');
        const decisionBox = document.getElementById('decision-box');
        const accessLabel = document.getElementById('access-label');
        const decisionMessage = document.getElementById('decision-message');
        const cameraContainer = document.getElementById('camera-body-student');
        const video = document.getElementById('video-stream-student');

        const myRut = rutInput.value.replace(/[^0-9kK]/g, '');
        const receivedRut = (data.rut || '').replace(/[^0-9kK]/g, '');
        if (myRut !== receivedRut) return; // Ignora resultados ajenos

        console.log('📨 Resultado para mí:', data);

        decisionBox.classList.remove('success', 'error');
        decisionMessage.classList.remove('success', 'error');


        if (video) {
            video.style.display = 'none';
        }  
         // Eliminar imagen anterior si existe
        const prevImg = cameraContainer.querySelector('img');
        if (prevImg) prevImg.remove();

        if (cameraContainer) {
            
            // Ocultar overlay
            const overlay = cameraContainer.querySelector('.face-guide-overlay');
            if (overlay) overlay.remove();

            // Ocultar o eliminar spinner
            const spinner = document.getElementById('camera-spinner');
            if (spinner) spinner.remove();

            const img = document.createElement('img');
            img.src = 'https://grupo3.juan.cl' + data.uploaded_url;
            cameraContainer.appendChild(img);
        }

        if (data.status === 'success') {
            decisionBox.classList.add('success');
            accessLabel.textContent = 'ACCESO PERMITIDO';
        } else {
            decisionBox.classList.add('error');
            accessLabel.textContent = 'ACCESO DENEGADO';
            decisionMessage.textContent = data.message || 'Verificación fallida';
            decisionMessage.classList.add('error');
        }
        document.dispatchEvent(new Event('verificacion-finalizada'));
    });
});
