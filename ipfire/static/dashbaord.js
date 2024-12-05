const baseURL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
document.addEventListener('DOMContentLoaded', () => {
    const table = document.getElementById('logTable');
    const contextMenu = createContextMenu();

    // Context Menu Initialization
    initializeContextMenu(contextMenu, table);

    // Fetch Logs
    fetchLogs();
    setInterval(fetchLogs, 5000);
});

/**
 * Creates and returns the context menu element.
 */
function createContextMenu() {
    const contextMenu = document.createElement('div');
    contextMenu.id = 'contextMenu';
    document.body.appendChild(contextMenu);

    const menuItems = [
        { label: 'Add Firewall', action: () => alert('Viewing details...') },
    ];

    menuItems.forEach(item => {
        const menuItem = document.createElement('div');
        menuItem.textContent = item.label;
        menuItem.addEventListener('click', () => {
            item.action();
            hideContextMenu(contextMenu);
        });
        contextMenu.appendChild(menuItem);
    });

    return contextMenu;
}

/**
 * Hides the context menu.
 */
function hideContextMenu(contextMenu) {
    contextMenu.style.display = 'none';
}

/**
 * Initializes the context menu functionality.
 */
function initializeContextMenu(contextMenu, table) {
    table.addEventListener('contextmenu', event => {
        event.preventDefault();
        const row = event.target.closest('tr');
        if (row) {
            contextMenu.style.top = `${event.clientY}px`;
            contextMenu.style.left = `${event.clientX}px`;
            contextMenu.style.display = 'block';
        }
    });

    document.addEventListener('click', () => hideContextMenu(contextMenu));
}

/**
 * Fetches logs from the server and updates the log table.
 */
async function fetchLogs() {
    try {
        console.log(`${baseURL}`)
        const response = await fetch(`${baseURL}/api/logs/`);
        const logs = await response.json();
        // console.log(logs)
        const table = document.getElementById('logTable');
        table.innerHTML = '';

        logs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${log.input_id}</td>
                <td>${log.input_passwd}</td>
                <td>${log.source_addr}</td>
                <td>${log.result}</td>
                <td>${new Date(log.time).toLocaleString()}</td>
            `;
            if (log.result) row.classList.add('attack-log');
            table.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching logs:', error);
    }
}
