Пробуем Django!

Учебный образовательный сайт, запустить можно так:
```
git clone git@github.com:avoronov/otus.git
cd otus/LearningCenter
pip install -r requirements.txt
cd learningcenter
python manage.py runserver
```


Для того, что бы через форму обратной связи отсылались письма, нужно:
* установить **redis** - ```sudo apt-get install redis-server```, после установки он сразу запустится
* установить **django-rq** - ```pip install django-rq```
* запустить проект - ```cd otus/LearningCenter/learningcenter; python manage.py runserver```
* запустить обработчик очереди в отдельной консоли - ```cd otus/LearningCenter/learningcenter; python manage.py rqworker```
* открыть в браузере http://127.0.0.1:8000/message, заполнить и засабмитить форму
* тк к проекту подключен бекенд почты **django.core.mail.backends.filebased.EmailBackend**, то все отправленные письма будут добавляться в папку **app-messages** 