document.addEventListener('DOMContentLoaded', () => {
    function updateCpuUsage(percentage) {
        const numberElement = document.getElementById('cpu-number');
        const ringElement = document.getElementById('cpu-ring');

        // Ensure percentage is between 0 and 100
        const clampedPercentage = Math.max(0, Math.min(100, percentage));

        // Update the number displayed
        numberElement.innerHTML = Math.round(clampedPercentage);

        // Calculate angle for the pointer (0% -> -90°, 100% -> +90°)
        const angle = (clampedPercentage * 180 / 100) - 90;

        // Convert angle to radians for trigonometric functions
        const radians = angle * (Math.PI / 180);

        // Calculate pointer position (assume radius is half of the gauge's size)
        const radius = 50; // Adjust if needed based on gauge size
        const pointerLeft = Math.round(50 + (radius * Math.cos(radians))) + '%'; // Horizontal position
        const pointerTop = Math.round(50 - (radius * Math.sin(radians))) + '%'; // Vertical position (inverted)

        // Apply CSS variables for pointer positioning
        ringElement.style.setProperty('--pointerdeg', `${angle}deg`);
        ringElement.style.setProperty('--pointerleft', pointerLeft);
        ringElement.style.setProperty('--pointertop', pointerTop);

        // Debugging - Log values
        // console.log('CPU Usage:', clampedPercentage, '%');
        // console.log('Pointer Angle:', angle, 'degrees');
        // console.log('Pointer Position - Left:', pointerLeft, 'Top:', pointerTop);
    }

    function updateRamUsage(percentage) {
        const numberElement = document.getElementById('ram-number');
        const ringElement = document.getElementById('ram-ring');

        // Ensure percentage is between 0 and 100
        const clampedPercentage = Math.max(0, Math.min(100, percentage));

        // Update the number displayed
        numberElement.innerHTML = Math.round(clampedPercentage);

        // Calculate angle for the pointer (0% -> -90°, 100% -> +90°)
        const angle = (clampedPercentage * 180 / 100) - 90;

        // Convert angle to radians for trigonometric functions
        const radians = angle * (Math.PI / 180);

        // Calculate pointer position (assume radius is half of the gauge's size)
        const radius = 50; // Adjust if needed based on gauge size
        const pointerLeft = Math.round(50 + (radius * Math.cos(radians))) + '%'; // Horizontal position
        const pointerTop = Math.round(50 - (radius * Math.sin(radians))) + '%'; // Vertical position (inverted)

        // Apply CSS variables for pointer positioning
        ringElement.style.setProperty('--pointerdeg', `${angle}deg`);
        ringElement.style.setProperty('--pointerleft', pointerLeft);
        ringElement.style.setProperty('--pointertop', pointerTop);

        // Debugging - Log values
        // console.log('RAM Usage:', clampedPercentage, '%');
        // console.log('Pointer Angle:', angle, 'degrees');
        // console.log('Pointer Position - Left:', pointerLeft, 'Top:', pointerTop);
    }

    function fetchCpuUsage() {
        fetch('/api/cpu-usage', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                updateCpuUsage(data.cpu_usage);
            })
            .catch(error => {
                console.error('Error fetching CPU usage:', error);
            });
    }

    function fetchRamUsage() {
        fetch('/api/ram-usage', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                updateRamUsage(data.ram_usage);
            })
            .catch(error => {
                console.error('Error fetching RAM usage:', error);
            });
    }

    // Načíst log soubor pomocí fetch API
    async function loadDeleteLogs() {
        try {
            const response = await fetch('/api/deletelogs', {
                method: 'GET',
                headers: {
                    'Content-Type': 'text/html'
                }
            });
    
            if (response.ok) {
                const htmlContent = await response.text(); // Získání celého HTML obsahu jako textu
                const logContainer = document.getElementById('deletelog-container');
                
                // Vložit HTML obsah do určeného elementu
                logContainer.innerHTML = htmlContent;
            } else {
                console.error("Failed to load logs:", response.status);
            }
        } catch (error) {
            console.error("Error loading logs:", error);
        }
    }

    // Načíst log soubor pomocí fetch API
    async function loadHttprequestLogs() {
        try {
            const response = await fetch('/api/httprequesteslogs', {
                method: 'GET',
                headers: {
                    'Content-Type': 'text/html'
                }
            });
    
            if (response.ok) {
                const htmlContent = await response.text(); // Získání celého HTML obsahu jako textu
                const logContainer = document.getElementById('httprequesteslogs-container');
                
                // Vložit HTML obsah do určeného elementu
                logContainer.innerHTML = htmlContent;
            } else {
                console.error("Failed to load logs:", response.status);
            }
        } catch (error) {
            console.error("Error loading logs:", error);
        }
    }

    async function loadRootTree() {
        try {
            const response = await fetch('/api/filesTree', {
                method: 'GET',
                headers: {
                    'Content-Type': 'text/html'
                }
            });
    
            if (response.ok) {
                const htmlContent = await response.text(); // Získání celého HTML obsahu jako textu
                const logContainer = document.getElementById('filesTree-container');
                
                // Vložit HTML obsah do určeného elementu
                logContainer.innerHTML = htmlContent;
            } else {
                console.error("Failed to load logs:", response.status);
            }
        } catch (error) {
            console.error("Error loading logs:", error);
        }
    }

    // Update every 5 seconds
    setInterval(fetchCpuUsage, 5000);
    fetchCpuUsage(); // Initial fetch

    setInterval(fetchRamUsage, 5000);
    fetchRamUsage(); // Initial fetch
    loadDeleteLogs();
    loadHttprequestLogs();
    loadRootTree();
});
