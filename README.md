# Залежності
Python 3.10
# Як скопіювати на свій комп'ютер
Запустити термінал в директорії в яку скопіюється проект і виконати наступні команди:
`git clone https://github.com/andriiko489/meduzzen_backend_internship`
# Як запустити без докера
Запустити термінал в директорії проекту і виконати наступні команди:
```
pip install -r requirements.txt
python app/main.py
```
Сайт буде запущений за адресою http://127.0.0.1:8000/

Щоб запустити тести потрібно написати наступну команду
`pytest`
# Як запустити з докером
Запустити термінал в директорії проекту і виконати наступні команди:
```
docker build -t app .
docker-compose up
```
Сайт буде запущений за адресою http://127.0.0.1:8000/
# Як відкрити термінал контейнера
Щоб відкрити термінал потрібно написати наступну команду:
`docker ps`
Ця команда відображає всі запущені контейнери, нам потрібний ID контейнера до якого треба підключитися.
Щоб відкрити термінал контейнера потрібно написати наступну команду:
`docker exec -it [CONTEINER ID] bash`
# Як запустити тести
В терміналі контейнера `app` виконати наступну команду
`python -m pytest`
# Як створити міграції
В терміналі контейнера `app` виконати наступну команду
`alembic -n main_db revision --autogenerate -m "init"`
# Як виконати міграції
В терміналі контейнера `app` виконати наступні команди
```
alembic -n main_db upgrade head
alembic -n test_db upgrade head
```

