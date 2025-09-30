import random
import uuid

names = [
    'Шапкарин Денис Сергеевич',
    'Деракова Анастасия Маратовна',
    'Капустин Максим Сергеевич',
    'Гуляев Егор Михайлович',
    'Шапкарин Иван Сергеевич',
    'Дераков Арсений Маратович',
    'Васильев Никита Олегвочи',
    'Горелов Илья Алексеевич',
    'Есина Злата Денисовна',
    'Шапкарин Сергей Александрович', 
    'Дераков Марат Николаевич',
]

categories = [
    'Одежда',
    'Обувь',
    'Аксессуары',
]

products_clothes = [
    'Футболка',
    'Шорты',
    'Брюки',
    'Куртка',
    'Джинсы',
]

products_shoes = [
    'Кроссовки',
    'Ботинки',
    'Сандали',
    'Тапочки',
    'Кеды',
]

products_accessories = [
    'Кепка',
    'Сумка',
    'Чехол для телефона',
    'Чехол для ноутбука',
    'Чехол для планшета',
]

addresses = [
    'Москва, ул. Ленина, 1',
    'Санкт-Петербург, ул. Пушкина, 10',
    'Екатеринбург, ул. Гагарина, 5',
    'Новосибирск, ул. Кирова, 15',
    'Красноярск, ул. Мира, 20',
]

def gen_uuid():
    return uuid.uuid4()

def gen_people():
    return random.choice(names)

def gen_category_name():
    return random.choice(categories)

def gen_product_name():
    category_dict = {
        'Одежда': products_clothes,
        'Обувь': products_shoes,
        'Аксессуары': products_accessories,
    }
    return list(category_dict.items())

def gen_price():
    return random.randint(100, 10000)

def gen_address():
    return random.choice(addresses)

def gen_random_email():
    names = ['denis', 'anastasia', 'ilya', 'marat', 'ivan', 'maxim', 'arsenyi']
    surnames = ['shapkarin', 'derakov', 'gorelov', 'vasiliev', 'ghulayev', 'esina']
    separators = ['', '.', '_']

    username = (
        random.choice(names) + 
        random.choice(separators) + 
        random.choice(surnames) + 
        str(random.randint(1, 99))
    )

    domains = ['gmail.com', 'mtuci.ru', 'mail.ru', 'yandex.ru']
    return f"{username}@{random.choice(domains)}"



    