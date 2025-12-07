# Habit Tracker

Сервис для отслеживания привычек с интеграцией Telegram‑бота.

## Описание

**Habit Tracker** — веб‑приложение на Django для:
- ведения списка личных привычек;
- контроля регулярности выполнения;
- получения напоминаний через Telegram;
- аналитики прогресса.

## Технологии

- **Backend**: Django, DRF (Django REST Framework)
- **База данных**: PostgreSQL
- **Асинхронные задачи**: Celery + Redis
- **Интеграция**: Telegram Bot API
- **Деплой**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Структура проекта

```
Final_Homework_9/
├──.github/
│   └──workflows
│       └──deploy.yml
├──.venv/
├── habit_tracker/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── habits/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
├── ngnix/
│   └── ngnix.conf
├── telegram_integration/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_user_username_user_telegram_id_and_more.py
│   │   ├── 0003_alter_user_managers.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env
├── .env.example
├── .flake8
├── .gitignore
├── celerybeat-schedule
├── celerybeat-schedule-shm
├── celerybeat-schedule-wal
├── docker-compose.yml
├── Dockerfile
├── dump.rdb
├── manage.py
├── README.md
└── requirements.txt
```

## Запуск локально

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/black-sun-spb/Course_work_8.git
cd Course_work_8
```

### 2. Создайте виртуальное окружение
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate  # Windows
```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

### 4. Настройте окружение
```bash
cp .env.example .env
```

Заполните \`.env\` актуальными значениями (см. \`.env.example\`).

### 5. Запустите сервисы через Docker Compose
```bash
docker-compose up -d
```

### 6. Примените миграции
```bash
docker-compose exec web python manage.py migrate
```

### 7. Создайте суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```

### 8. Проверьте работу
- API: \`http://localhost:8000/api/habits/\`
- Админка: \`http://localhost:8000/admin/\`
- Здоровье: \`http://localhost:8000/health/\`

## Настройка сервера (Yandex Cloud)

### 1. Создайте ВМ
- ОС: Ubuntu 22.04 LTS
- Открытые порты: 22 (SSH), 80, 443, 8000

### 2. Установите Docker и Docker Compose
```bash
sudo apt update
sudo apt install docker.io docker-compose-plugin -y
sudo systemctl enable --now docker
sudo usermod -aG docker \$USER
```

### 3. Разверните проект
```bash
git clone https://github.com/black-sun-spb/Course_work_8.git -b develop
cd Course_work_8
cp .env.example .env  # Заполните параметры
docker-compose up -d
```

### 4. Примените миграции
```bash
docker-compose exec web python manage.py migrate
```

## CI/CD (GitHub Actions)

### Этапы workflow
1. **Линтинг и тесты**: проверка кода через \`flake8\` и \`pytest\`.
2. **Сборка Docker‑образа**: упаковка в контейнер.
3. **Деплой на сервер**: автоматическое обновление при пуше в \`develop\`.

### Необходимые секреты GitHub
В \`Settings → Secrets and variables → Actions\`:
- \`DOCKER_HUB_USERNAME\`
- \`DOCKER_HUB_PASSWORD\`
- \`SERVER_HOST\` (IP сервера)
- \`SERVER_USER\` (пользователь SSH)
- \`SERVER_SSH_KEY\` (приватный ключ)


## Эндопоинты API


### Пользователи (\`/api/users/\`)
- \`GET /users/\` — список пользователей
- \`POST /users/\` — регистрация
- \`GET /users/{id}/\` — профиль


### Привычки (\`/api/habits/\`)
- \`GET /habits/\` — список привычек
- \`POST /habits/\` — создание
- \`PUT /habits/{id}/\` — редактирование
- \`DELETE /habits/{id}/\` — удаление


### Telegram (\`/api/telegram/\`)
- \`POST /webhook/\` — обработка сообщений бота
- \`GET /start/\` — инициализация бота


## Тестирование


```bash
python manage.py test
```
Или для конкретного приложения:
```bash
python manage.py test habits
```

## Документация API


Доступна через Swagger:  
\`http://localhost:8000/api-docs/\`

## Важные файлы

- \`.env.example\` — шаблон переменных окружения
- \`docker-compose.yml\` — конфигурация контейнеров
- \`.github/workflows/deploy.yml\` — CI/CD‑пайплайн
