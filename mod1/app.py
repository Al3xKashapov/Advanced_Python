import datetime
import os
import random
from random import choice


from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/test')
def test_function():
    now = datetime.datetime.now().utcnow()
    return f'Это тестовая страничка, ответ сгенерирован в {now}'

@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lexus']
@app.route('/cars')
def cars():
    return ", ".join(cars_list)

cat_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчки']
@app.route('/cats')
def cats():
    return choice(cat_list)

@app.route('/get_time/now')
def get_time():
    now = datetime.datetime.now().utcnow()
    return 'Точное время: {current_time}'.format(current_time=now)

@app.route('/get_time/future')
def get_time_future():
    delta = datetime.timedelta(hours=1)
    now = datetime.datetime.now().utcnow()
    return 'Точное время через час будет {current_time_after_hour}'.format(current_time_after_hour=now + delta)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
@app.route('/get_random_word')
def get_random_word():
    with open(BOOK_FILE, "r", encoding='utf8') as book:
        content = book.read()
    words = content.replace(',', '.').split()
    random_word = random.choice(words)
    return random_word

visit = 0
@app.route('/counter')
def counter():
    global visit
    visit += 1
    return f'Страница открыта {visit} раз(a)'