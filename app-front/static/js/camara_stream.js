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