async function searchArticles() {
    const query = document.getElementById('query').value;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = "<p>actually searching...</p>";

    try {
        const response = await fetch('http://127.0.0.1:5000/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        if (response.ok) {
            const results = await response.json();
            resultsDiv.innerHTML = ""; 
            if (results.length === 0) {
                resultsDiv.innerHTML = "<p>no results found.</p>";
            } else {
                results.forEach(result => {
                    const div = document.createElement('div');
                    div.className = 'result';
                    div.innerHTML = `
                        <p><strong>${result.text}</strong></p>
                        <p><a href="${result.url}" target="_blank">Read more</a></p>
                    `;
                    resultsDiv.appendChild(div);
                });
            }
        } else {
            const error = await response.json();
            resultsDiv.innerHTML = `<p>error: ${error.error}</p>`;
        }
    } catch (error) {
        console.error("error fetching:", error);
        resultsDiv.innerHTML = "<p>failed to fetch results.</p>";
    }
}
