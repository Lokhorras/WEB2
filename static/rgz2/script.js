const API_URL = '/api';

// Функция для входа
async function login() {
    const login = document.getElementById('login').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!login || !password) {
        alert('Заполните все поля.');
        return;
    }

    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password }),
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById('username').innerText = data.login;
        loadAccount();
        document.getElementById('auth-section').style.display = 'none';
        document.getElementById('main-section').style.display = 'block';
    } else {
        const error = await response.json();
        alert(error.error || 'Ошибка входа.');
    }
}

// Функция для выхода
async function logout() {
    const response = await fetch(`${API_URL}/logout`, {
        method: 'POST',
    });

    if (response.ok) {
        alert('Вы успешно вышли.');
        document.getElementById('auth-section').style.display = 'block';
        document.getElementById('main-section').style.display = 'none';
    } else {
        alert('Ошибка при выходе.');
    }
}

// Загрузка данных аккаунта
async function loadAccount() {
    const response = await fetch(`${API_URL}/account`);
    if (response.ok) {
        const data = await response.json();
        document.getElementById('balance').innerText = `${data.account.balance} ₽`;
        loadHistory();
    } else {
        alert('Ошибка загрузки данных аккаунта.');
    }
}

// Функция перевода
async function transfer() {
    const receiver = document.getElementById('receiver').value.trim();
    const amount = parseFloat(document.getElementById('amount').value.trim());

    if (!receiver || !amount || amount <= 0) {
        alert('Введите корректные данные.');
        return;
    }

    const response = await fetch(`${API_URL}/transfer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receiver_account_number: receiver, amount }),
    });

    if (response.ok) {
        alert('Перевод выполнен.');
        loadAccount();
    } else {
        const error = await response.json();
        alert(error.error || 'Ошибка при переводе.');
    }
}

// Загрузка истории операций
async function loadHistory() {
    const response = await fetch(`${API_URL}/history`);
    if (response.ok) {
        const data = await response.json();
        const historyList = document.getElementById('history');
        historyList.innerHTML = '';
        data.transactions.forEach((transaction) => {
            const li = document.createElement('li');
            li.textContent = `${transaction.timestamp}: ${transaction.sender_login} отправил ${transaction.amount} ₽ ${transaction.receiver_login}`;
            historyList.appendChild(li);
        });
    } else {
        alert('Ошибка загрузки истории операций.');
    }
}
