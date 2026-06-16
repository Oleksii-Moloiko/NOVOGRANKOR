# NOVOGRANKOR Landing Page

Односторінковий сайт для компанії **NOVOGRANKOR**, яка займається виготовленням та встановленням пам’ятників з натурального граніту.

Основна ціль сайту — швидко показати приклади робіт, надати базову інформацію про компанію та привести користувача до контакту: дзвінка або повідомлення в Telegram, Viber чи WhatsApp.

---

## Функціонал

* Односторінковий Landing Page
* Hero-блок з назвою компанії, слоганом і CTA
* Клікабельний номер телефону
* Кнопки Telegram / Viber / WhatsApp
* Floating call button для швидкого дзвінка
* Блок “Про нас”
* Каталог робіт з категоріями
* Фото пам’ятників через Django Admin
* Блок послуг
* Фінальний контактний CTA
* Адаптивна верстка для desktop та mobile

---

## Стек

* Python
* Django
* SQLite
* HTML
* CSS
* Bootstrap

---

## Структура проєкту

```text
novogrankor/
├── config/              # Налаштування Django-проєкту
├── core/                # Основний Django app
├── templates/           # HTML-шаблони
│   ├── base.html
│   └── home.html
├── static/              # Статичні файли
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── logo.png
├── media/               # Завантажені фото з адмінки
├── db.sqlite3           # Локальна база даних
├── manage.py
├── requirements.txt
└── README.md
```

---

## Основні моделі

У проєкті використовуються такі моделі:

* `Category` — категорії пам’ятників
* `Monument` — приклади робіт / пам’ятники
* `Gallery` — додаткова галерея
* `ContactRequest` — заявки від користувачів
* `SiteSettings` — налаштування сайту: телефон, месенджери, hero-тексти

---

## Локальний запуск

### 1. Клонувати репозиторій

```bash
git clone <repository-url>
cd novogrankor
```

### 2. Створити віртуальне середовище

```bash
python -m venv .venv
```

### 3. Активувати віртуальне середовище

Для macOS / Linux:

```bash
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

### 4. Встановити залежності

```bash
pip install -r requirements.txt
```

### 5. Застосувати міграції

```bash
python manage.py migrate
```

### 6. Створити суперкористувача

```bash
python manage.py createsuperuser
```

### 7. Запустити сервер

```bash
python manage.py runserver
```

Після запуску сайт буде доступний за адресою:

```text
http://127.0.0.1:8000/
```

Адмінка:

```text
http://127.0.0.1:8000/admin/
```

---

## Робота з адмінкою

Через Django Admin можна:

1. Додати категорії пам’ятників:

   * Бюджетні
   * Середні
   * Елітні
   * Військові

2. Додати пам’ятники в кожну категорію:

   * назва
   * опис
   * фото
   * категорія

3. Оновити налаштування сайту:

   * телефон
   * Telegram
   * WhatsApp
   * hero title
   * hero subtitle

---

## Контакти на сайті

Телефон використовується як клікабельне посилання:

```html
<a href="tel:+380959197152">
    +38 (095) 919-71-52
</a>
```

WhatsApp:

```html
https://wa.me/380959197152
```

Viber:

```html
viber://chat?number=%2B380959197152
```

Telegram задається через `SiteSettings` в адмінці.

---

## Робота зі статикою

CSS-файл:

```text
static/css/style.css
```

Логотип:

```text
static/img/logo.png
```

Підключення статичних файлів у шаблоні:

```django
{% load static %}
```

Приклад використання логотипа:

```django
<img src="{% static 'img/logo.png' %}" alt="NOVOGRANKOR">
```

---

## Робота з media-файлами

Фото пам’ятників завантажуються через Django Admin і зберігаються в папці:

```text
media/
```

Для локального відображення media-файлів у `config/urls.py` має бути:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

У `settings.py` має бути:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

## Git ignore

У репозиторій не потрібно додавати:

```text
.venv/
__pycache__/
*.pyc
db.sqlite3
media/
staticfiles/
.env
.DS_Store
__MACOSX/
```

Рекомендований `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc

db.sqlite3
media/
staticfiles/

.env
.DS_Store
__MACOSX/
```

---

## Поточний статус

Готовий MVP landing page:

* сайт запускається локально;
* головна сторінка зверстана;
* контакти клікабельні;
* каталог наповнюється через адмінку;
* фото пам’ятників виводяться по категоріях;
* доданий фоновий watermark-логотип;
* є адаптивні стилі для мобільної версії.

---

## Подальші покращення

* Додати favicon
* Перевірити реальні посилання на Telegram, Viber, WhatsApp
* Додати більше фото в категорії
* Покращити мобільну версію після тестування на реальному телефоні
* Підготувати продакшен-налаштування
* Винести секретні налаштування в `.env`
* Перейти з SQLite на PostgreSQL для продакшену
* Налаштувати деплой
* Додати SEO meta title та description
* Додати sitemap.xml і robots.txt

---

## Основна логіка сайту

Сайт не є інтернет-магазином або складним каталогом.

Основний сценарій користувача:

```text
Користувач заходить на сайт
↓
Швидко бачить, чим займається компанія
↓
Переглядає приклади робіт
↓
Телефонує або пише в месенджер
```

Головна бізнес-ціль:

```text
Фото робіт → довіра → контакт
```
