document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('instructions-container');
    const button = document.getElementById('toggle-button');

    button.addEventListener('click', () => {
        const isCollapsed = container.classList.toggle('collapsed');
        button.textContent = isCollapsed ? '▼' : '▲';
    });
});
