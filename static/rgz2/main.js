const API_BASE = '/api';

// Login
async function loginUser(login, password) {
    const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password })
    });
    return response.json();
}

// Logout
async function logoutUser() {
    const response = await fetch(`${API_BASE}/logout`, {
        method: 'POST'
    });
    return response.json();
}

// Transfer
async function transferFunds(receiverAccountNumber, amount) {
    const response = await fetch(`${API_BASE}/transfer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receiver_account_number: receiverAccountNumber, amount })
    });
    return response.json();
}

// Fetch Account Details
async function fetchAccountDetails() {
    const response = await fetch(`${API_BASE}/account`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    return response.json();
}

// Example Usage
(async () => {
    try {
        // Example: Login
        const loginResponse = await loginUser('johndoe', '123');
        console.log('Login Response:', loginResponse);

        // Example: Fetch Account Details
        const accountDetails = await fetchAccountDetails();
        console.log('Account Details:', accountDetails);

        // Example: Transfer Funds
        const transferResponse = await transferFunds('09876543', 500);
        console.log('Transfer Response:', transferResponse);

        // Example: Logout
        const logoutResponse = await logoutUser();
        console.log('Logout Response:', logoutResponse);
    } catch (error) {
        console.error('Error:', error);
    }
})();
