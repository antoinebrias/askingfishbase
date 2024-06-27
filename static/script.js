async function fetchInfo() {
    const species = document.getElementById('species').value.trim(); // Get species name from input

    try {
        const response = await fetch('/fetch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ species })
        });

        if (!response.ok) {
            const errorData = await response.json(); // Parse error response
            throw new Error(errorData.error); // Throw an error with the error message
        }

        const result = await response.json(); // Parse successful response
        const textSummary = result.summary; // Extract summary text

        // Display summary in a <pre> tag
        document.getElementById('response').innerHTML = `<p>${textSummary}</p>`;
    } catch (error) {
        // Handle errors
        console.error('Error fetching data:', error);
        document.getElementById('response').innerText = 'An error occurred while fetching the data.';
    }
}
