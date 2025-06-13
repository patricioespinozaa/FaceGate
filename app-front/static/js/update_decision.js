
function updateDecision(isVerified, studentName = '', studentPhoto = '', dataMessage = '', imageUrl = '') {
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
    const decisionMessage = document.getElementById('decision-message');
    const ucampusContainer = document.getElementById('camera-body-ucampus');

    decisionBox.classList.remove('success', 'error');
    decisionMessage.classList.remove('success', 'error');

    if (isVerified && dataMessage === "Acceso permitido") {
        decisionBox.classList.add('success');
        accessLabel.textContent = "ACCESO PERMITIDO";
        decisionMessage.textContent = studentName;
        decisionMessage.classList.add('success');
    } else if (!isVerified && dataMessage === "Acceso denegado") {
        decisionBox.classList.add('error');
        accessLabel.textContent = "ACCESO DENEGADO";
        decisionMessage.textContent = "Verificación fallida";
        decisionMessage.classList.add('error');
    } else if (!isVerified && dataMessage === "Rut no encontrado") {
        decisionBox.classList.add('error');
        accessLabel.textContent = "ACCESO DENEGADO";
        decisionMessage.textContent = "Rut no encontrado";
        decisionMessage.classList.add('error');
    } else {
        decisionBox.classList.add('error');
        accessLabel.textContent = "ACCESO DENEGADO";
        decisionMessage.textContent = "Verificación Fallida";
        decisionMessage.classList.add('error');
    }

    // Mostrar imagen solo si existe contenedor
    if (ucampusContainer && imageUrl) {
        ucampusContainer.innerHTML = '';
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = "Foto del estudiante";
        ucampusContainer.appendChild(img);
    }
}
