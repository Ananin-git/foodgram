#  Социальная сеть для обмена рецептами приготовления еды Foodgram

Адрес сайта: https://yp-foodgram.zapto.org/

## Описание проекта

Данный проект представляет собой социальную сеть, которая позволяет пользователям: 
- публиковать свои рецепты 
- добавлять чужие рецепты в избранное 
- подписываться на публикации других авторов 
- зарегистрированным пользователям доступен сервис «Список покупок». 

## Использованные технологии
- Python — разработка backend, версия 3.9
- Django — веб-фреймворк, версия 5.1.1
- Django REST Framework — создание API, версия 3.15.2
- React — фреймворк для frontend
- npm — управление пакетами frontend
- Nginx — веб-сервер и обратный прокси
- Docker — контейнеризация и деплой
- PostgreSQL — база данных
- GitHub Actions — автоматизация CI/CD



## Как развернуть проект локально

### 1. Клонируйте репозиторий на компьютер
```bash
git clone git clone <https or SSH URL>
```

### 2. Заполните переменные окружения
Для работы проекта необходимо заполнить переменные окружения. Создаnm файл `.env` в 
корневой директории проекта и добавьте переменные:

```env
- SECRET_KEY=your_django_secret_key
- DEBUG=True
- ALLOWED_HOSTS=your_domain.com,localhost,127.0.0.1
- DB_ENGINE=sqlite
- DB_NAME=your_db_name
- POSTGRES_USER=your_db_user
- POSTGRES_PASSWORD=your_db_password
- DB_HOST=db
- DB_PORT=5432
```
### 3. Установите зависимости и выполните миграции
В терминале перейдите в директорию backend и выполните следующие команды:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py load_data --data_type=ingredients
python manage.py load_data --data_type=tags

```

### 4. Запустите frontend-проект
```bash
npm run start
```
### 5. Запустите backend-проект
```bash
python manage.py runserver
```
### 6. Откройте в браузере адрес http://localhost:3000


## Доступы и документация
### Доступ к сайту
https://fogramopa.ddns.net/


### Доступ к админке
https://fogramopa.ddns.net/admin/


## Документация
```  
http://fogramopa.ddns.net/api/docs  
```


## Автор  
[Ананьин Михаил] https://github.com/gor134
