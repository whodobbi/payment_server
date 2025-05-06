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

В процессе реализации и настройки `DEBUG=False` выявлен **конфликт**, связанный с тем, что:

* обе админки используют общую `admin`-статику (CSS/JS);
* Unfold требует быть **в начале** `INSTALLED_APPS`, чтобы переопределить шаблоны;
* но это приводит к тому, что классическая админка начинает ломаться (ошибка `toggle_sidebar`, 500 и несовместимые шаблоны).

Вывод: **одновременная работа двух стилистически отличающихся админок невозможна**, так как Unfold заменяет базовые шаблоны `admin` на свои.

Можно выбрать:

1. Оставить **две одинаковые по стилю админки** — и отказаться от визуального преимущества Unfold;
2. Или использовать **только Unfold** — но тогда `/admin/` становится неработоспособным.

В данной реализации я **осознанно выбрала Unfold**, как более современный и подходящий под задачу вариант (в том числе с Dashboard), отказавшись от `/admin/` в пользу `/dashboard/`.

* `/admin/` — стандартная Django admin
* `/dashboard/` — кастомная Unfold



## Краткое соответствие заданию

* [x] Модели и статусы реализованы
* [x] `save()` с логикой обработки попыток оплаты
* [x] Celery-задача по просроченным счетам
* [x] Панель Unfold + Dashboard
* [x] Поддержка `DEBUG=False`, раздача статики через Whitenoise
* [x] Документация по запуску
* [x] Структура и нюансы указаны
