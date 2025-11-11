# 8. Django REST Framework #

Система управления обучением (LMS) с интеграцией платежной системы Stripe для продажи курсов.

## Технологии
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)  
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)  
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)  
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
- **Stripe API** для платежей  
- **drf-yasg** для документации API   


## Использование
Открыть проект в  
![Pycharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)

## Структура проекта

### Приложение `materials`
- **Модели**: `Course`, `Lesson`, `Payment`, `Subscription`
- **API эндпоинты** для управления курсами и уроками
- **Интеграция с Stripe** для обработки платежей
- **Автоматическое переключение** между реальным и мок-сервисом Stripe
- **Система подписок** на обновления курсов
- **Асинхронные уведомления** через Celery

### Приложение `users`
- **Кастомная модель пользователя** `User` (email вместо username)
- **JWT аутентификация**
- **Расширенная админка** с русской локализацией
- **Периодические задачи** для блокировки неактивных пользователей

### Основные функции
- **Управление курсами и уроками** - CRUD операции через REST API
- **Система платежей** - интеграция с Stripe для оплаты курсов
- **Документация API** - Swagger UI и ReDoc
- **Управление пользователями** - кастомная аутентификация
- **Безопасность** - JWT токены, права доступа
- **Уведомления** - асинхронная рассылка email при обновлении материалов
- **Периодические задачи** - автоматическая блокировка неактивных пользователей
- **Система подписок** - уведомления об обновлениях курсов

## API Эндпоинты

### Материалы
- `GET/POST /api/materials/courses/` - список/создание курсов
- `GET/PUT/DELETE /api/materials/courses/{id}/` - управление курсом
- `GET/POST /api/materials/lessons/` - управление уроками
- `GET/POST /api/materials/payments/` - платежи
- `GET/POST /api/materials/subscriptions/` - управление подписками

### Пользователи
- `GET /api/` - корневой эндпоинт
- `POST /api/users/token/` - получение JWT токена
- `POST /api/users/register/` - регистрация
- `GET/PUT /api/users/profile/` - профиль текущего пользователя
- `GET /api/users/users/{id}/` - просмотр профиля пользователя

### Документация
- `GET /swagger/` - Swagger UI
- `GET /redoc/` - ReDoc документация

## Запуск Celery

Для работы асинхронных задач необходимо запустить:

```bash
# Worker для обработки задач
celery -A config worker --loglevel=info
```

```bash
# Beat для периодических задач
celery -A config beat --loglevel=info
```

### Периодические задачи

Ежедневно в полночь: Блокировка пользователей, не заходивших более месяца  

При обновлении курса: Рассылка уведомлений подписанным пользователям  

При обновлении урока: Рассылка уведомлений (с проверкой времени)  

------------
В проекте присутствует файл
### requirements.txt
Файл с зависимостями pip для проекта. Для
установки зависимостей следует в терминале
(возможно в терминале PyCharm) ввести команду:
```bash
pip install -r requirements.txt
```

Запуск сервера
```bash
python manage.py runserver
```

### Требования
Для установки и запуска проекта, необходимы:  
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
https://www.python.org/  
![Pycharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)
https://www.jetbrains.com/pycharm/  
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
https://www.djangoproject.com/  
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
https://www.jwt.io/  
[Stripe API]
https://stripe.com/docs/api  
[drf-yasg]
https://drf-yasg.readthedocs.io/en/stable/


## Команда проекта
[Roman Z](roman-z@inbox.ru)
