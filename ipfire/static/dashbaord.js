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
        {
            label: 'Add To Firewall',
            action: (row) => {
                const cells = Array.from(row.children);
                alert(cells[2].textContent)

            }
        },
    ];

    menuItems.forEach(item => {
        const menuItem = document.createElement('div');
        menuItem.textContent = item.label;
        menuItem.style.padding = '5px 10px';
        menuItem.style.cursor = 'pointer';
        menuItem.style.borderBottom = '1px solid #f0f0f0';
        menuItem.addEventListener('click', () => {
            if (contextMenu.targetRow) {
                item.action(contextMenu.targetRow); // Pass the row to the action
            }
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
        event.preventDefault(); // 기본 우클릭 메뉴 방지

        const row = event.target.closest('tr'); // 클릭한 셀의 부모 행
        if (row) {
            contextMenu.targetRow = row; // 현재 행을 contextMenu에 저장

            // 마우스 위치에 따라 메뉴 위치 설정 (스크롤 고려)
            contextMenu.style.top = `${event.pageY}px`;
            contextMenu.style.left = `${event.pageX}px`;
            contextMenu.style.display = 'block';
        }
    });

    // 메뉴 외부를 클릭했을 때 메뉴 숨기기
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
