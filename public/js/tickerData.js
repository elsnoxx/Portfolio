document.getElementById('myForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Zabraňuje odeslání formuláře tradiční metodou

    // Resetování výsledků a zobrazení spinnerů
    document.getElementById('spinner-api1').classList.remove('d-none');
    document.getElementById('spinner-api2').classList.remove('d-none');
    document.getElementById('spinner-api3').classList.remove('d-none');
    const resultApi1 = document.getElementById('result-api1');
    const resultApi2 = document.getElementById('result-api2');
    const resultApi3 = document.getElementById('result-api3');
    resultApi1.innerHTML = ``;
    resultApi2.innerHTML = ``;
    resultApi3.innerHTML = ``;
    

    // Získání hodnoty tickeru
    const tickerSymbol = document.getElementById('ticker_symbol').value;
    console.log(tickerSymbol)
    const formData = new FormData();
    const api1Url = `/basicData/${tickerSymbol}`;

    // Volání prvního API
    fetch(api1Url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('spinner-api1').classList.add('d-none');
        resultApi1.innerHTML = data.html;
        
    }).then(
        fetch('/dcf', {
            method: 'POST',
            body: formData
        })
    
    .then(response => response.json())
    .then(data => {
        document.getElementById('spinner-api2').classList.add('d-none');
        resultApi2.innerHTML = data.html;
        
        // Volání třetího API
        return fetch('/income', {
            method: 'POST',
            body: formData
        });
    }))
    .then(response => response.json())
    .then(data => {
        document.getElementById('spinner-api3').classList.add('d-none');
        resultApi3.innerHTML = data.html;
    })
    .catch(error => {
        console.error('Chyba:', error);
    });
});
