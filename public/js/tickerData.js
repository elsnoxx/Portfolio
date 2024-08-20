document.getElementById('myForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Zabraňuje odeslání formuláře tradiční metodou
    document.getElementById('loading-spinner').classList.remove('d-none');
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ` `;
    
    const formData = new FormData(this);

    fetch('/submit', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Zobrazení odpovědi
            const resultDiv = document.getElementById('result');
            document.getElementById('loading-spinner').classList.add('d-none');
            resultDiv.innerHTML = `
        <div class="container mt-5">
<h2 class="text-center">Výsledky ${data['Ticker'].toLocaleString()}</h2>

<div class="card my-4">
    <div class="card-body">
        <p class="card-text"><strong>Sum of FCF:</strong> $${data['Sum of FCF'].toLocaleString()}</p>
        <p class="card-text"><strong>Equity Value:</strong> $${data['Equity Value'].toLocaleString()}</p>
        <p class="card-text"><strong>Shares Outstanding:</strong> ${data['Shares Outstanding'].toLocaleString()}</p>
        <p class="card-text"><strong>DCF Price per Share:</strong> $${data['DCF Price per Share'].toLocaleString()}</p>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <p class="card-text"><strong>Cash Equivalents:</strong> $${data['Cash Equivalents'].toLocaleString()}</p>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <h3 class="card-title">Free Cash Flow</h3>
        <ul class="list-group list-group-flush">
            ${data['Free Cash Flow'].map(fcf => `<li class="list-group-item">$${fcf.toLocaleString()}</li>`).join('')}
        </ul>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <p class="card-text"><strong>FCF Growth:</strong> ${data['FCF Growth'].join(', ')}</p>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <p class="card-text"><strong>Growth Average:</strong> $${data['Growth Average'].toLocaleString()}</p>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <h3 class="card-title">Future Free Cash Flow</h3>
        <ul class="list-group list-group-flush">
            ${data['Future FCF'].map(fcf => `<li class="list-group-item">$${fcf.toLocaleString()}</li>`).join('')}
        </ul>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <p class="card-text"><strong>Terminal Value:</strong> $${data['Terminal Value'].toLocaleString()}</p>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <h3 class="card-title">PV of Future FCF</h3>
        <ul class="list-group list-group-flush">
            ${data['PV of Future FCF'].map(pv => `<li class="list-group-item">$${pv.toLocaleString()}</li>`).join('')}
        </ul>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <h3 class="card-title">Financial Ratios</h3>
        <ul class="list-group list-group-flush">
            ${Object.entries(data['Financial Ratios']).map(([ratio, value]) => `<li class="list-group-item"><strong>${ratio}:</strong> ${value}</li>`).join('')}
        </ul>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <p class="card-text"><strong>Revenue Growth:</strong> ${data['Revenue Growth']}%</p>
        <p class="card-text"><strong>Earnings Growth:</strong> ${data['Earnings Growth']}%</p>
    </div>
</div>

<div class="card my-4">
    <div class="card-body">
        <h3 class="card-title">Free Cash Flow (Reversed)</h3>
        <ul class="list-group list-group-flush">
            ${data['Free Cash Flow'].map(fcf => `<li class="list-group-item">$${fcf.toLocaleString()}</li>`).join('')}
        </ul>
    </div>
</div>
</div>
        `;
        })
        .catch(error => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = ` Neznami ticker `;
            console.error('Chyba:', error);
        });
});