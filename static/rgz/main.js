function fetchUser() {
    if (sessionStorage.getItem('login')) {
        fetch('/rgz/rest-api/user')  // Используйте маршрут для получения данных пользователя
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    window.location.href = '/rgz/rest-api/login';
                } else {
                    displayUser(data);
                }
            });
    } else {
        window.location.href = '/rgz/rest-api/login';
    }
}

function loginUser(login, password) {
    fetch('/rgz/rest-api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login: login, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            sessionStorage.setItem('login', login);
            window.location.href = '/rgz/account';
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during login');
    });
}

function fetchTransfers() {
    fetch('/rgz/rest-api/transfers')
        .then(response => response.json())
        .then(transactions => {
            displayTransfers(transactions);
        });
}

function transferFunds() {
    const receiverAccount = document.getElementById('receiver_account_number').value;
    const amount = document.getElementById('amount').value;
    fetch('/rgz/rest-api/transfer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({receiver_account_number: receiverAccount, amount: amount})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Transfer successful');
            window.location.href = '/rgz/account';
        }
    });
}

function displayUser(user) {
    document.getElementById('full_name').innerText = user.full_name;
    document.getElementById('phone').innerText = user.phone;
    document.getElementById('account_number').innerText = user.account_number;
    document.getElementById('balance').innerText = user.balance + ' руб.';
}

function displayTransfers(transactions) {
    const tableBody = document.getElementById('transactions-body');
    tableBody.innerHTML = '';
    transactions.forEach(txn => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${txn.sender_login}</td>
            <td>${txn.receiver_login}</td>
            <td>${txn.amount} руб.</td>
            <td>${txn.timestamp}</td>
        `;
        tableBody.appendChild(row);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetchUser();
    fetchTransfers();
});