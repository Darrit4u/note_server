# Python сервер, предоставляющий Rest API интерфейс для добавления и хранения текстовых заметок

## Описание


* Сервер сделан на основе FastApi.
* Присутсвует авторизация, аутентификация и авторизация пользователя. Каждый пользователь имеет доступ только к своим заметкам.
* При добавлении заметки происходит проверка текста с помощью сервиса Яндекс Спеллер. Если в тексте содержаться ошибки, об этом сообщается пользователю и заметка не сохраняется
* Реализован jwt token, но без refresh_token'а
* Пароль хранится в виде хэша
* База данных сделана в виде json файлов. Доступ к бд делается с помощью класса JsonDB, где для инициализации бд необходимы только пути к json-файлам с данными.
* Проверка чистоты кода производилась с помощью pylint (игнорируя missing docstring) и black.


## Основные эндпоинты

* Регистрация пользователя - /register params: username, password
* Авторизация пользователя - /login params: username, password
* Добавление своей заметки (только для авторизованных пользователей) - /note/add params: text
* Просмотр своих заметок (только для авторизованных пользователей) - /user/note
 
## Установка проекта

### С помощью git clone

```sh
git clone https://github.com/Darrit4u/note_server.git
cd note_server
python3.11 -m venv env
source ./env/Scripts/activate
pip install -r requirements.txt
uvicorn src.app:app --reload 
```

### С помощью docker
```sh
docker pull da44it/note_server:ver1.0
docker run -p 80:80 da44it/note_server:ver1.0
```

## Пример запросов
[Коллекция запросов Postman](https://www.postman.com/darrit/workspace/public-workspace/collection/22089641-cb547b4d-2dc6-4bdd-89f7-a33ec7111b1b?action=share&creator=22089641)
