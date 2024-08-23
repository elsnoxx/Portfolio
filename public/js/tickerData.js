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
            document.getElementById('loading-spinner').classList.add('d-none');
            resultDiv.innerHTML = data.html;
        })
        .catch(error => {
            resultDiv.innerHTML = ` Neznami ticker `;
            console.error('Chyba:', error);
        });
});
