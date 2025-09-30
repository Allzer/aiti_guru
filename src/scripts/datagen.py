from datetime import datetime, timedelta
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
    {
        'Футболка': [
            'Футболка 1',
            'Футболка 2',
            'Футболка 3',
        ]
    },
    {
        'Шорты': [
            'Шорты 1',
            'Шорты 2',
            'Шорты 3',
        ],
    },
    {
        'Брюки': [
            'Брюки 1',
            'Брюки 2',
            'Брюки 3',
        ],
    }
]

products_shoes = [
    {
        'Кроссовки': [
            'Кроссовки 1',
            'Кроссовки 2',
            'Кроссовки 3',
        ]
    },
    {
        'Ботинки': [
            'Ботинки 1',
            'Ботинки 2',
            'Ботинки 3',
        ]
    },
]

products_accessories = [
    {
        'Кепка': [
            'Кепка 1',
            'Кепка 2',
            'Кепка 3',
        ]
    },
    {
        'Сумка': [
            'Сумка 1',
            'Сумка 2',
            'Сумка 3',
        ]
    },
    {
        'Чехол для телефона': [
            'Чехол для телефона 1',
            'Чехол для телефона 2',
            'Чехол для телефона 3',
        ]
    },
    {
        'Чехол для ноутбука': [
            'Чехол для ноутбука 1',
            'Чехол для ноутбука 2',
            'Чехол для ноутбука 3',
        ]
    },
    {
        'Чехол для планшета': [
            'Чехол для планшета 1',
            'Чехол для планшета 2',
            'Чехол для планшета 3',
        ]
    },
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


def gen_order_created_at():
    """
    Возвращает datetime для created_at с распределением:
      - 50% — случайная дата в предыдущем календарном месяце,
      - 30% — случайная дата в текущем месяце,
      - 20% — дата старее, чем предыдущий месяц (60..180 дней назад).
    Используется UTC (datetime.utcnow()).
    """
    now = datetime.utcnow()
    r = random.random()
    if r < 0.5:
        # предыдущий календарный месяц
        first_of_this_month = datetime(now.year, now.month, 1)
        last_month_end = first_of_this_month - timedelta(days=1)
        first_of_last_month = datetime(last_month_end.year, last_month_end.month, 1)
        days_in_last_month = (last_month_end - first_of_last_month).days
        d = first_of_last_month + timedelta(days=random.randint(0, days_in_last_month))
        return d + timedelta(hours=random.randint(0,23), minutes=random.randint(0,59))
    elif r < 0.8:
        # текущий месяц, от 1 числа до now
        first_of_this_month = datetime(now.year, now.month, 1)
        max_day_offset = max(0, (now - first_of_this_month).days)
        d = first_of_this_month + timedelta(days=random.randint(0, max_day_offset))
        return d + timedelta(hours=random.randint(0,23), minutes=random.randint(0,59))
    else:
        # старее предыдущего месяца: 60..180 дней назад
        delta_days = random.randint(60, 180)
        d = now - timedelta(days=delta_days)
        return d.replace(hour=random.randint(0,23), minute=random.randint(0,59), second=0, microsecond=0)