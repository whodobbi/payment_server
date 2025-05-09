# Payment Server

Тестовое задание: реализация Django-приложения для управления платежами и демонстрации административных возможностей, включая Unfold-дизайн, кастомную логику обработки счетов и асинхронную обработку задач через Celery.

## Функционал

* Модели: `Invoice` (Счёт) и `PaymentAttempt` (Попытка оплаты)
* Статусы счёта: ожидает оплату, оплачен, просрочен
* Логика `save()` в `PaymentAttempt`:
  * отказ, если счёт просрочен
  * недостаточно средств, если сумма превышает лимит
  * успешная оплата и перевод счёта в статус "оплачен"
* Celery-задача `mark_invoice_as_expired`, запускаемая по `expires_at`
* Кастомная админка Unfold + Dashboard со статусами
* Использование Whitenoise для корректной раздачи статики в проде

## Технологии

* Python 3.12
* Django 4.2
* Celery 5
* Redis (брокер задач)
* Unfold (альтернатива Django Admin)
* SQLite3 (по умолчанию)
* Whitenoise (обслуживание статики при DEBUG=False)
* uv (управление окружением и зависимостями)

## Запуск проекта (в режиме DEBUG=False)

### 1. Подготовка окружения

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Сборка статики

```bash
python manage.py collectstatic
```

> Статика обслуживается с помощью [Whitenoise](https://whitenoise.readthedocs.io/en/stable/), который подключён через `MIDDLEWARE` и `STATICFILES_STORAGE`

### 3. Миграции

```bash
python manage.py migrate
```

### 4. Запуск Django

```bash
export DJANGO_SETTINGS_MODULE=payment_server.settings
export DEBUG=False
python manage.py runserver
```

### 5. Запуск Celery

```bash
celery -A payment_server worker --loglevel=info
```

## Dashboard (Unfold)

Доступен по адресу: `/dashboard/`

Показывает:

* Кол-во счетов по статусам
* Кол-во попыток оплаты по статусам
* Использует шаблон `templates/unfold/dashboard.html`

## Структура проекта

```
.
├── manage.py
├── db.sqlite3
├── requirements.txt
├── payment_server/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── payments/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── classic_site.py
│   ├── dashboard.py
│   ├── models.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   ├── unfold_admin.py
│   ├── unfold_site.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
├── templates/
│   └── unfold/
│       └── dashboard.html
├── static/
└── staticfiles/
```

## Админки

В проекте предусмотрены две админки:

* `/admin/` — стандартная Django admin
* `/dashboard/` — кастомная Unfold admin

### Как работает

Обе админки реализованы через наследование от UnfoldAdminSite. Это позволяет использовать стили и возможности Unfold в обеих админках.

В итоге:

* `/admin/` — классическая точка входа, но с оформлением Unfold;
* `/dashboard/` — современная Unfold-панель, плюс Dashboard со статистикой.

### Почему не классическая + Unfold?

Unfold переопределяет шаблоны admin — это делает невозможным одновременное отображение двух стилистически разных админок. При попытке разместить Unfold в INSTALLED_APPS ниже — его шаблоны не применяются, а если выше — стандартная админка ломается (ошибки JS и верстки).

Поэтому было принято решение:
* использовать единый стиль Unfold для обеих панелей;
* обеспечить стабильную работу /admin/ без конфликтов;
* применить индивидуальные точки входа для различия интерфейсов.

## Краткое соответствие заданию

* [x] Модели и статусы реализованы
* [x] `save()` с логикой обработки попыток оплаты
* [x] Celery-задача по просроченным счетам
* [x] Панель Unfold + Dashboard
* [x] Поддержка `DEBUG=False`, раздача статики через Whitenoise
* [x] Документация по запуску
* [x] Структура и нюансы указаны
