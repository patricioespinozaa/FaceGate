document.addEventListener('DOMContentLoaded', function () {
    const socket = io('https://grupo3.juan.cl', {
        path: '/socket.io',
        transports: ['websocket']
    });

    socket.on('connect', () => {
        console.log('✅ WebSocket conectado');
    });

    socket.on('resultado_verificacion', (data) => {
        console.log('📨 Resultado recibido vía WebSocket:', data);

        const isVerified = data.status === 'success';
        const studentName = data.nombre || '';
        const rut = data.rut || '';
        const message = data.message || 'Verificación fallida';

        updateDecision(isVerified, studentName, rut, message);
    });

    socket.on('disconnect', () => {
        console.warn('⚠️ WebSocket desconectado');
    });
});
