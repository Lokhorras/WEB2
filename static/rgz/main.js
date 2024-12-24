const API_BASE = '/rgz/api';

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

// Fetch Transaction History
async function fetchHistory() {
    const response = await fetch(`${API_BASE}/history`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
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

// Create User (Manager Only)
async function createUser(userDetails) {
    const response = await fetch(`${API_BASE}/create_user`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userDetails)
    });
    return response.json();
}

// Edit User (Manager Only)
async function editUser(login, updatedDetails) {
    const response = await fetch(`${API_BASE}/edit_user/${login}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedDetails)
    });
    return response.json();
}

// Delete User (Manager Only)
async function deleteUser(login) {
    const response = await fetch(`${API_BASE}/delete_user/${login}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
    });
    return response.json();
}

// Manage Users (Manager Only)
async function fetchUsers() {
    const response = await fetch(`${API_BASE}/manage_users`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    return response.json();
}

// Example Usage
(async () => {
    try {
        const loginResponse = await loginUser('johndoe', '123');
        console.log('Login Response:', loginResponse);

        const accountDetails = await fetchAccountDetails();
        console.log('Account Details:', accountDetails);

        const transferResponse = await transferFunds('09876543', 500);
        console.log('Transfer Response:', transferResponse);

        const history = await fetchHistory();
        console.log('Transaction History:', history);

        const logoutResponse = await logoutUser();
        console.log('Logout Response:', logoutResponse);
    } catch (error) {
        console.error('Error:', error);
    }
})();