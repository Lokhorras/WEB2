// Обработчик отправки формы входа
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries()); // Преобразуем FormData в объект

    fetch('/rgz2/rest-api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Указываем, что отправляем JSON
        },
        body: JSON.stringify(data) // Сериализуем данные в JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            sessionStorage.setItem('login', data.login);
            window.location.href = '/rgz2/'; // Перенаправляем на главную страницу
        } else {
            alert(data.error); // Показываем ошибку
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during login');
    });
});

// Функция для выхода
function logout() {
    fetch('/rgz/rest-api/logout', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/rgz/login';
        }
    });
}

// Функция для получения данных пользователя
function fetchUser() {
    fetch('/rgz/rest-api/user')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                window.location.href = '/rgz/login';
            } else {
                displayUser(data);
            }
        });
}

// Функция для отображения данных пользователя
function displayUser(user) {
    document.getElementById('full_name').innerText = user.full_name;
    document.getElementById('phone').innerText = user.phone;
    document.getElementById('account_number').innerText = user.account_number;
    document.getElementById('balance').innerText = user.balance + ' руб.';
}

// Функция для получения истории транзакций
function fetchTransfers() {
    fetch('/rgz/rest-api/transfers')
        .then(response => response.json())
        .then(transactions => {
            displayTransfers(transactions);
        });
}

// Функция для отображения истории транзакций
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

// Загрузка данных при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fetchUser();
    fetchTransfers();
});