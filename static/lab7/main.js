function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (response) {
        return response.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for (let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');
            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;
            tdTitle.innerHTML = films[i].title 
                ? `<em>(${films[i].title})</em>` 
                : '';
            tdYear.innerText = films[i].year;

            // Кнопка редактирования
            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function(){
                editFilm(i); 
            };

            // Кнопка удаления
            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function(){
                deleteFilm(i, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);
            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);
            tbody.append(tr);
        }
    });
}



function deleteFilm(id, title){
    if (! confirm(`Вы точно хотите удалить фильм?"${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method:'DELETE'})
    .then(function(){
        fillFilmList();
    });
}
function showModal(){
    document.querySelector('div.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
}
function hideModal(){
    document.querySelector('div.modal').style.display = 'none';
}
function addFilm(){
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal()
    
}
function cancel(){
    hideModal()
}

function sendFilm() {
    const id = document.getElementById('id').value.trim();
    const title = document.getElementById('title').value.trim();
    const title_ru = document.getElementById('title_ru').value.trim();
    const year = document.getElementById('year').value.trim();
    const description = document.getElementById('description').value.trim();

    if (title_ru === '') {
        alert('Название фильма на русском обязательно!');
        return;
    }

    if (year === '' || isNaN(year)) {
        alert('Год выпуска обязателен и должен быть числом!');
        return;
    }

    const film = {
        title: title === '' ? title_ru : title, // Заполняем оригинальное название, если оно пустое
        title_ru: title_ru,
        year: parseInt(year), 
        description: description
    };

    // Определяем метод и URL
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    // Отправляем запрос
    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if (resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if (errors.error) {
            alert(errors.error);
        }
    })
    .catch(function(err) {
        console.error('Ошибка запроса:', err);
        alert('Произошла ошибка при отправке данных.');
    });
}
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Фильм не найден');
        }
        return response.json();
    })
    .then(function (film) {
        // Заполняем форму данными из ответа сервера
        document.getElementById('id').value = id; 
        document.getElementById('title').value = film.title || '';
        document.getElementById('title_ru').value = film.title_ru || '';
        document.getElementById('year').value = film.year || '';
        document.getElementById('description').value = film.description || '';

        showModal();
    })
    .catch(function (error) {
        console.error('Ошибка при редактировании:', error);
        alert('Не удалось загрузить данные фильма для редактирования.');
    });
}
