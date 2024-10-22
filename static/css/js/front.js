document.getElementById('rule-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const rule = document.getElementById('rule').value;

    // Send rule to backend for evaluation using Fetch API
    fetch('/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Send data as JSON
        },
        body: JSON.stringify({ rule: rule })   // Send rule in JSON format
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';  // Clear previous results

        if (data.status === 'success') {
            // Display the results
            data.results.forEach(item => {
                const div = document.createElement('div');
                div.innerHTML = <strong>Data:</strong> ;{JSON.stringify(item.data)} - <strong>Result:</strong>;{item.result};
                resultsDiv.appendChild(div);
            });
        } else {
            // Display error message
            resultsDiv.innerHTML = <p class="error">${data.message}</p>;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('results').innerHTML = <p class="error">An error occurred while processing the rule.</p>;
    });
});

document.getElementById("rule-form").addEventListener("submit", function(event) {
    event.preventDefault();
    let rule = document.getElementById("rule").value;

    fetch('/api/create_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule: rule })
    })
    .then(response => response.json())
    .then(data => {
        const responseDiv = document.getElementById("response");
        if (data.status === 'success') {
            responseDiv.innerHTML = 'AST: ' + data.ast;
        } else {
            responseDiv.innerHTML = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("response").innerHTML = <p class="error">An error occurred while creating the rule.</p>;
    });
});