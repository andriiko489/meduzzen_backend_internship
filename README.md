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
# Як запустити з докером
Запустити термінал в директорії проекту і виконати наступні команди:
```
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```
Сайт буде запущений за адресою http://127.0.0.1/