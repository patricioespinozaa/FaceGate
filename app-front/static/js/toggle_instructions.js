document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('instructions-container');
    const button = document.getElementById('toggle-button');
    const box = document.getElementById('instructions-box');

    button.addEventListener('click', () => {
        const willCollapse = container.classList.contains('expanded');

        if (willCollapse) {
            // Paso 1: cerrar el contenido
            container.classList.remove('expanded');

            // Paso 2: reducir el ancho después de la animación de altura
            setTimeout(() => {
                box.classList.add('collapsed');
            }, 400);
        } else {
            // Paso 1: expandir el ancho
            box.classList.remove('collapsed');

            // Paso 2: mostrar contenido después de que crezca el ancho
            setTimeout(() => {
                container.classList.add('expanded');
            }, 400);
        }

        // flechita
        button.textContent = willCollapse ? '▼' : '▲';
    });
});
