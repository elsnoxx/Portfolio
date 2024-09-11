document.getElementById('myForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Zabraňuje odeslání formuláře tradiční metodou

    // Resetování výsledků a zobrazení spinnerů
    document.getElementById('spinner-api1').classList.remove('d-none');
    document.getElementById('spinner-api2').classList.remove('d-none');
    document.getElementById('spinner-api3').classList.remove('d-none');
    
    const resultApi1 = document.getElementById('result-api1');
    const resultApi2 = document.getElementById('result-api2');
    const resultApi3 = document.getElementById('result-api3');
    
    resultApi1.innerHTML = '';
    resultApi2.innerHTML = '';
    resultApi3.innerHTML = '';

    // Získání hodnoty tickeru
    const tickerSymbol = document.getElementById('ticker_symbol').value;
    const formData = new FormData();
    
    const api1Url = `/basicData/${tickerSymbol}`;
    const api2Url = `/graph/${tickerSymbol}`;
    const api3Url = `/technicalanalysis/${tickerSymbol}`;

    // Volání jednotlivých API funkcí
    loadBasicData(api1Url, formData);
    loadGraph(api2Url, formData);
    loadTechnicalAnalysis(api3Url, formData);
});

async function loadBasicData(apiUrl, formData) {
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData
        });
        
        const resultApi1 = document.getElementById('result-api1');
        const spinnerApi1 = document.getElementById('spinner-api1');

        if (response.ok) {
            const data = await response.json();
            spinnerApi1.classList.add('d-none');
            resultApi1.innerHTML = data.html;
        } else {
            throw new Error(`Failed to load data: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Chyba při volání API 1:', error);
        document.getElementById('spinner-api1').classList.add('d-none');
        document.getElementById('result-api1').innerHTML = `<p>Chyba při načítání dat: ${error.message}</p>`;
    }
}

async function loadGraph(apiUrl, formData) {
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData
        });

        const resultApi2 = document.getElementById('result-api2');
        const spinnerApi2 = document.getElementById('spinner-api2');

        if (response.ok) {
            const data = await response.json();
            spinnerApi2.classList.add('d-none');
            resultApi2.innerHTML = data.html;
        } else {
            throw new Error(`Failed to load graph: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Chyba při volání API 2:', error);
        document.getElementById('spinner-api2').classList.add('d-none');
        document.getElementById('result-api2').innerHTML = `<p>Chyba při načítání grafu: ${error.message}</p>`;
    }
}

async function loadTechnicalAnalysis(apiUrl, formData) {
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData
        });

        const resultApi3 = document.getElementById('result-api3');
        const spinnerApi3 = document.getElementById('spinner-api3');

        if (response.ok) {
            const data = await response.json();
            spinnerApi3.classList.add('d-none');
            resultApi3.innerHTML = data.html;
        } else {
            throw new Error(`Failed to load technical analysis: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Chyba při volání API 3:', error);
        document.getElementById('spinner-api3').classList.add('d-none');
        document.getElementById('result-api3').innerHTML = `<p>Chyba při načítání technické analýzy: ${error.message}</p>`;
    }
}
