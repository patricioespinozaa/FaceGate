document.addEventListener('DOMContentLoaded', function () {
    const videoStream = document.getElementById('video-stream');
    if(navigator.mediaDevices.getUserMedia){
        navigator.mediaDevices.getUserMedia({video: true})
        .then(function (stream) {
            videoStream.srcObject = stream;
        })
        .catch (function (error) {
            console.log("Error ");
        })
    } else{
        console.log("no se dio el permiso");
    }
});

//Boton de captura
document.getElementById('captura').addEventListener('click', function () {
    var canvas = document.createElement('canvas');
    var video = document.getElementById('video-stream');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

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