function updateDecision(isVerified, studentName = '') {
    const decisionBox = document.getElementById('decision-box');
    const accessLabel = document.getElementById('access-label');
    const decisionMessage = document.getElementById('decision-message');
    decisionBox.classList.remove('success', 'error');
    decisionMessage.classList.remove('success', 'error');

    if (isVerified) {
        decisionBox.classList.add('success');
        accessLabel.textContent = "ACCESO PERMITIDO";

        decisionMessage.textContent = studentName;
        decisionMessage.classList.add('success');
    } else {
        decisionBox.classList.add('error');
        accessLabel.textContent = "ACCESO DENEGADO";

        decisionMessage.textContent = "Verificación Fallida";
        decisionMessage.classList.add('error');
    }
}
