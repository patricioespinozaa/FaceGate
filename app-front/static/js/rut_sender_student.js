document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut');
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
    const decisionMessage = document.getElementById('decision-message');
    const capturedPhoto = document.getElementById('captured-photo');
    const cameraContainer = document.getElementById('camera-body-student');
    const takePicBtn = document.getElementById('take-pic');
    const videoStream = document.getElementById('video-stream-student');
    const rutErrorMessage = document.getElementById('rut-error-message');

    const timeout = 20000;
    const delay = 5000;

    let startTime;
    let takingPhoto = false; 

    decisionBox.classList.remove('success', 'error');
    decisionMessage.classList.remove('success', 'error'); 

    function resetUI(){
        videoStream.style.display = 'block';
        if(!videoStream.srcObject){
            navigator.mediaDevices.getUserMedia({video: true})
            .then(stream => videoStream.srcObject = stream)
            .catch(err => console.log("no se pudo acceder a la camara", err));
        }
        //reset de rut 
        rutInput.disabled = false;
        rutInput.value = '';
        // y de estilos 
        decisionBox.classList.remove('success', 'error');
        decisionMessage.classList.remove('success', 'error');
        decisionMessage.textContent = '';
        accessLabel.textContent = 'Acércate a la cámara';

        //reset de la foto 
        if (capturedPhoto) {
            capturedPhoto.style.display = 'none';
        }
        rutErrorMessage.textContent = '';
        rutErrorMessage.classList.remove('error');
        rutErrorMessage.style.visibility = 'hidden';        
        //reset del stream
        if (cameraContainer) {
            cameraContainer.innerHTML = '';
        
            //crear nuevo stream
            const newVideo = document.createElement('video');
            newVideo.setAttribute('autoplay', true);
            newVideo.setAttribute('id', 'video-stream-student');
            newVideo.style.width = '100%';
        
            
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    newVideo.srcObject = stream;
                })
                .catch(err => {
                    console.error('Error al acceder a la cámara:', err);
                });
        
            cameraContainer.appendChild(newVideo);
        }

        //reset boton 
        takePicBtn.querySelector('#take-pic-label').textContent = 'Tomar foto';
        takingPhoto = false;

    }

    // Lógica: después de enviar RUT, espera y consulta /get_result
    async function checkResult(rut,  startTime) { 
        
        decisionBox.classList.remove('success', 'error');
        decisionMessage.classList.remove('success', 'error'); 

        // Esperar 5 s para dar tiempo a capturar foto y verificar
        await new Promise(resolve => setTimeout(resolve, delay));

        fetch(`https://grupo3.juan.cl/facegate/app-ia/get_result?rut=${rut}`)
            .then(res => res.json())
            .then(data => {
                console.log('🔄 Resultado:', data);

                if (data.status === 'pending') {
                    accessLabel.textContent = 'Aún procesando...';
                    return;
                }
                
                
                const endTime = performance.now();
                const elapsed = endTime - startTime;
                console.log(`Tiempo de respuesta total: ${elapsed.toFixed(2)} ms`);
                

                    cameraContainer.innerHTML = ''; // Quita el spinner

                const img = document.createElement('img');
                img.src = 'https://grupo3.juan.cl' + data.uploaded_image_url;

                cameraContainer.appendChild(img);
                
                // Cambiar decisionBox según resultado real
                if (data.status === 'success') {
                    decisionBox.classList.add('success');
                    decisionBox.classList.remove('error');
                    decisionMessage.classList.remove('success', 'error'); 
                    accessLabel.textContent = 'ACCESO PERMITIDO';
                } else if (data.status === 'error') {
                    decisionBox.classList.add('error');
                    decisionBox.classList.remove('success');
                    decisionMessage.classList.remove('success', 'error'); 
                    accessLabel.textContent = 'ACCESO DENEGADO';
                    if (data.notes === 'Rut no encontrado') {
                        decisionMessage.textContent = "Rut no encontrado";
                        decisionMessage.classList.add('error');
                    }
                    else if (data.notes === 'Verificación fallida') {
                        decisionMessage.textContent = "Verificación fallida";
                        decisionMessage.classList.add('error');
                    }
                    else if (data.notes === 'Rostro no detectado') {
                        decisionMessage.textContent = "Rostro no detectado";
                        decisionMessage.classList.add('error');
                    }
                } else {
                    decisionBox.classList.remove('success', 'error');
                    decisionMessage.classList.remove('success', 'error'); 
                    accessLabel.textContent = 'Verificando...';
                }
                //cambiar a retomar foto
                takePicBtn.querySelector('#take-pic-label').textContent = 'Retomar foto';
                takingPhoto = true;
            })
            .catch(error => {
                console.error('❌ Error al obtener resultado:', error);
            });
    }


    function captureAndSend(){
        let rut = rutInput.value.replace(/[^0-9kK]/g, '');
        const cuerpo = rut.slice(0, -1);
        const dv = rut.slice(-1).toLowerCase();
        const rutValue = `${cuerpo}-${dv}`;
        if (!rutValue) return;

        startTime = performance.now();
        
        const canvas = document.createElement('canvas');
        canvas.width = videoStream.videoWidth;
        canvas.height = videoStream.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoStream, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            const formData= new FormData();
            formData.append('rut', rutValue);
            formData.append('photo', blob, 'photo.jpg');
            fetch('https://grupo3.juan.cl/facegate/app-ia/store_rut', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    console.log('✅ RUT guardado:', data);
                    rutInput.disabled = true;
                    
                    // Quitamos ultima foto
                    
                    if (cameraContainer) {
                        cameraContainer.innerHTML = '<div class="spinner" id="camera-spinner"></div>';
                    }
                                    // Cambia el decision box a estado "En proceso"
                    decisionBox.classList.remove('success', 'error');
                    decisionMessage.classList.remove('success', 'error'); 
                    accessLabel.textContent = 'RUT enviado. Verificando...';

                    // Después de guardar, consultar resultado UNA VEZ
                    checkResult(rutValue, startTime);
                })
                .catch(error => {
                    console.error('❌ Error al enviar RUT:', error);
                    decisionBox.classList.add('error');
                    accessLabel.textContent = 'Error al enviar tu RUT. Intenta de nuevo.';
                });
            
        }, 'image/jpeg');            
    }
    takePicBtn.addEventListener('click', function (){
        if(!takingPhoto){
            const rawRut = rutInput.value.trim();
            if (!rawRut) {
                rutErrorMessage.textContent = "Ingresa tu RUT antes de tomarte la foto";
                rutErrorMessage.classList.add('error');
                rutErrorMessage.style.visibility = 'visible';
                return;
            }
            rutErrorMessage.textContent = '';
            rutErrorMessage.classList.remove('error');
            captureAndSend();
        } else{
            resetUI();
        }
    })
    
    rutInput.addEventListener('input', () => {
        rutErrorMessage.textContent = '';
        rutErrorMessage.classList.remove('error');
        rutErrorMessage.style.visibility = 'hidden';
    });
    
});
