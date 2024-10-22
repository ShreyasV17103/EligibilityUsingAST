document.getElementById('ruleForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const rule = document.getElementById('rule').value;
    const testData = {
        data: {
            age: 35,
            department: 'Sales',
            salary: 60000,
            experience: 5
        }
    };

    // Send rule and test data to backend for evaluation using Fetch API
    fetch('/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule: rule, data: testData.data })
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('response');
        resultsDiv.innerHTML = '';  // Clear previous results

        if (data.status === 'success') {
            // Display the result
            const div = document.createElement('div');
            div.innerHTML = `<strong>Result:</strong> ${data.result}`;
            resultsDiv.appendChild(div);
        } else {
            // Display error message
            resultsDiv.innerHTML = `<p class="error">${data.message}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerHTML = `<p class="error">An error occurred while processing the rule.</p>`;
    });
});
