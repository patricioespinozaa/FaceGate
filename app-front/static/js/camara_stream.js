document.addEventListener('DOMContentLoaded', function () {
    const videoStream = document.getElementById('video-stream');
    const socket = io();
    const peer = new RTCPeerConnection();

    // 1. Captura de cámara local
    navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then(stream => {
        videoStream.srcObject = stream;

        // 2. Añadir pistas a la conexión WebRTC
        stream.getTracks().forEach(track => peer.addTrack(track, stream));

        // 3. Crear y enviar oferta WebRTC
        return peer.createOffer();
    }).then(offer => {
        return peer.setLocalDescription(offer).then(() => {
            socket.emit('offer', { sdp: offer });
        });
    }).catch(error => {
        console.error("❌ Error al capturar cámara o crear oferta:", error);
    });

    // 4. Responder a 'answer' del estudiante
    const pendingCandidates = [];

    socket.on('answer', async ({ sdp }) => {
        try {
            await peer.setRemoteDescription(new RTCSessionDescription(sdp));

            // Procesar candidatos almacenados
            for (const candidate of pendingCandidates) {
                await peer.addIceCandidate(new RTCIceCandidate(candidate));
            }
            pendingCandidates.length = 0;
        } catch (err) {
            console.error("❌ Error al setear remoteDescription (answer):", err);
        }
    });

    socket.on('ice-candidate', ({ candidate }) => {
        if (peer.remoteDescription && peer.remoteDescription.type === 'answer') {
            peer.addIceCandidate(new RTCIceCandidate(candidate)).catch(e => {
                console.error("❌ ICE candidate inválido:", e);
            });
        } else {
            pendingCandidates.push(candidate);
        }
    });

});

//Boton de captura
/*
document.getElementById('captura').addEventListener('click', function () {
   var video = document.getElementById('video-stream');
   const videoWidth = video.videoWidth;
   const videoHeight = video.videoHeight;
   const squareSize = Math.min(videoWidth, videoHeight);
   const finalWidth = squareSize + 10;
   const finalHeight = squareSize;
   const cropX = (videoWidth - finalWidth) / 2;
   const cropY = (videoHeight - finalHeight) / 2;
   var canvas = document.createElement('canvas');

   canvas.width = finalWidth;
   canvas.height = finalHeight;

   canvas.getContext('2d').drawImage(video, cropX, cropY, finalWidth, finalHeight, 0, 0, finalWidth, finalHeight);
   canvas.toBlob(function (blob) {
       if (blob) {
           window.lastCaptureBlob = blob;  // Guarda global para que otro JS lo use
           console.log("Foto capturada y almacenada en window.lastCaptureBlob");
           //Cambiar stream por la foto
           const cameraBody = document.getElementById('camera-body-camara');
           cameraBody.innerHTML = '';
           const img = document.createElement('img');
           img.src = URL.createObjectURL(window.lastCaptureBlob);
           img.id = 'captured-image';
           img.style.maxWidth = '100%';
           img.style.maxHeight = '100%';
           img.style.objectFit = 'contain';
           cameraBody.appendChild(img);
       } else {
           console.error("No se pudo crear el blob de la imagen");
       }
   }, 'image/jpeg');
});
 */