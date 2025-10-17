import { updateStatus, fetchStatus } from '../main.js';

// Import the actual function from main.js
import { toggleSwitch } from '../main.js';

// Mock fetch globally
global.fetch = jest.fn();

// Setup DOM environment
const DOM = new JSDOM('<!DOCTYPE html><div id="status"></div>');
global.document = DOM.window.document;

describe('Frontend main.js', () => {
  let statusElement;

  beforeEach(() => {
    document.body.innerHTML = `
      <div id="app"></div>
      <div id="switch" class="off"></div>
      <p id="status">Status: Checking...</p>
    `;
    statusElement = document.getElementById('status');
    fetch.mockClear();
  });

  test('updateStatus updates the DOM element correctly', () => {
    updateStatus('Active');
    expect(statusElement.textContent).toBe('Active');
    expect(statusElement.style.color).toBe('green');

    updateStatus('Error', true);
    expect(statusElement.textContent).toBe('Error');
    expect(statusElement.style.color).toBe('red');
  });

  test('fetchStatus calls fetch and updates status on success', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ status: 'Online', timestamp: '2025-10-17T23:00:00Z' }),
    });

    await fetchStatus();

    expect(fetch).toHaveBeenCalledWith('http://localhost:5000/status');
    expect(statusElement.textContent).toMatch(/AI Status: Online/);
  });

  test('fetchStatus handles network error and updates status', async () => {
    fetch.mockRejectedValueOnce(new Error('Network failed'));

    await fetchStatus();

    expect(statusElement.textContent).toBe('Failed to connect to backend. Is it running?');
    expect(statusElement.style.color).toBe('red');
  });
});
