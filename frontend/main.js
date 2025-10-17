// Frontend logic to connect to backend and display status
let statusElement;

// Function to update status display
function updateStatus(message, isError = false) {
  if (statusElement) {
    statusElement.textContent = message;
    statusElement.style.color = isError ? 'red' : 'green';
  }
}

// Function to fetch status from backend
async function fetchStatus() {
  try {
    const response = await fetch('http://localhost:5000/status');
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const data = await response.json();
    updateStatus(`AI Status: ${data.status} (Last checked: ${data.timestamp})`);
  } catch (error) {
    console.error('Failed to fetch status:', error);
    updateStatus('Failed to connect to backend. Is it running?', true);
  }
}

// On DOM load, initialize
document.addEventListener('DOMContentLoaded', () => {
  statusElement = document.getElementById('status');
  if (statusElement) {
    updateStatus('Loading...');
    fetchStatus();
  } else {
    console.warn('Element with id "status" not found');
  }
});

// Export for testing (when using module)
export { updateStatus, fetchStatus };
