
function updateDecision(isVerified, studentName = '', studentPhoto = '', dataMessage = '') {
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
    const decisionMessage = document.getElementById('decision-message');
    const ucampusContainer = document.getElementById('camera-body-ucampus');
    ucampusContainer.innerHTML = '';
    decisionBox.classList.remove('success', 'error');
    decisionMessage.classList.remove('success', 'error');   
    const img = document.createElement('img');
    img.style.maxWidth = '100%';
    img.style.maxHeight = '100%';        
    if (isVerified && dataMessage == "Acceso permitido") {
        decisionBox.classList.add('success');
        accessLabel.textContent = "ACCESO PERMITIDO";

        decisionMessage.textContent = studentName;
        decisionMessage.classList.add('success');
        img.src =  "/facegate/app-front/static/img/".concat(studentPhoto).concat(".jpeg");
        img.alt = "Foto del estudiante";
    } else if(!isVerified && dataMessage == "Acceso denegado"){
        decisionBox.classList.add('error');
        accessLabel.textContent = "ACCESO DENEGADO";

        decisionMessage.textContent = "Verificación fallida";
        decisionMessage.classList.add('error');
        img.src =  "/facegate/app-front/static/img/".concat(studentPhoto).concat(".jpeg");
        img.alt = "Foto del estudiante";

    } else if(!isVerified && dataMessage == "Rut no encontrado"){
        decisionBox.classList.add('error');
        accessLabel.textContent = "ACCESO DENEGADO";

        decisionMessage.textContent = "Rut no encontrado";
        decisionMessage.classList.add('error');
        img.src = "/facegate/app-front/static/img/plain.png";
        img.alt = "Imagen de error";

    } else {
        decisionBox.classList.add('error');
        accessLabel.textContent = "ACCESO DENEGADO";

        decisionMessage.textContent = "Verificación Fallida";
        decisionMessage.classList.add('error');
        img.src = "/facegate/app-front/static/img/plain.png";
        img.alt = "Imagen de error";
    }
    ucampusContainer.appendChild(img);
}
