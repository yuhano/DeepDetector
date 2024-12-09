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
    // alert(cells[2].textContent);

    const menuItems = [
        {
            label: 'Add To Firewall',
            action: (row) => {
                const cells = Array.from(row.children);
                host_ip = window.location.hostname;
                src_addr = cells[3].textContent;
                ruleremark = "sample";
                sendFirewallRule(host_ip, src_addr, ruleremark);

                // alert(cells[2].textContent);

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


/**
 * 444 ipfire 서버에 데이터 방화벽 규칙 추가 
 */
async function sendFirewallRule(host_ip, src_addr, ruleremark) {
    const data = {
        host_ip: host_ip,       
        src_addr: src_addr,     
        ruleremark: ruleremark  
    };

    // const data = {
    //     host_ip: "192.168.1.1",
    //     src_addr: "10.0.0.1",
    //     ruleremark: "Block suspicious IP"
    // };

    try {
        // Flask 엔드포인트로 POST 요청 보내기
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) // JSON 형식으로 데이터 전송
        });

        // 응답 처리
        if (response.ok) {
            const result = await response.json();
            console.log("Server response:", result);
            alert("Firewall rule sent successfully!");
        } else {
            console.error("Error sending rule:", response.statusText);
            alert("Failed to send firewall rule.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while sending the firewall rule.");
    }
}