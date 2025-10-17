document.addEventListener('DOMContentLoaded', function () {
    const statusElement = document.getElementById('status');

    fetch('http://localhost:5000/status')
        .then(response => response.json())
        .then(data => {
            if (statusElement) {
                statusElement.textContent = `Status: ${data.status} - Service: ${data.service}`;
            }
        })
        .catch(error => {
            if (statusElement) {
                statusElement.textContent = 'Backend connection failed';
            }
            console.error('Fetch error:', error);
        });
});
