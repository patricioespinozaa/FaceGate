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

document.getElementById('captura').addEventListener('click', function () {
    var canvas = document.createElement('canvas');
    var video = document.getElementById('videoStream');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    var dataURL = canvas.toDataURL('image/imagen');
    console.log("Se saca la foto")
});