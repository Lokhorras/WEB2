async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (data) options.body = JSON.stringify(data);

    const response = await fetch(url, options);
    const result = await response.json();
    if (!response.ok) {
        throw new Error(result.error || 'Ошибка запроса');
    }
    return result;
}

async function login() {
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    try {
        const result = await apiRequest('rgz/api-rest/login', 'POST', { login, password });
        alert(result.message);
        window.location.href = '/rgz/account';
    } catch (error) {
        alert(error.message);
    }
}

async function transfer() {
    const receiverAccount = document.getElementById('receiver_account_number').value;
    const amount = parseFloat(document.getElementById('amount').value);

    try {
        const result = await apiRequest('rgz/api-rest/transfer', 'POST', { receiver_account_number: receiverAccount, amount });
        alert(result.message);
        window.location.reload();
    } catch (error) {
        alert(error.message);
    }
}

async function loadAccount() {
    try {
        const result = await apiRequest('rgz/api-rest/account');
        document.getElementById('user-info').innerText = JSON.stringify(result.user, null, 2);
    } catch (error) {
        alert(error.message);
    }
}

async function loadHistory() {
    try {
        const result = await apiRequest('rgz/api-rest/history');
        const historyElement = document.getElementById('history');
        historyElement.innerHTML = '';
        result.transactions.forEach(tx => {
            const row = document.createElement('div');
            row.textContent = `${tx.sender_login} -> ${tx.receiver_login}: ${tx.amount}`;
            historyElement.appendChild(row);
        });
    } catch (error) {
        alert(error.message);
    }
}
