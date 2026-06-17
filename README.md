# NOVOGRANKOR Landing Page

Односторінковий сайт для компанії **NOVOGRANKOR**, яка займається виготовленням та встановленням пам’ятників з натурального граніту.

Основна ціль сайту — швидко показати приклади робіт, надати базову інформацію про компанію та привести користувача до контакту: **дзвінка або переходу в Telegram, Viber чи WhatsApp**.

Сайт не використовує онлайн-замовлення, форми заявок або email-нотифікації. Основний бізнес-сценарій — користувач переглядає інформацію та телефонує або переходить у месенджер.

---

## Основна бізнес-логіка

Сайт не є інтернет-магазином або системою онлайн-заявок.

Основний сценарій користувача:

```text
Користувач заходить на сайт
↓
Швидко бачить, чим займається компанія
↓
Переглядає приклади робіт і відео процесу
↓
Телефонує або переходить у месенджер
```

Головна бізнес-ціль:

```text
Приклади робіт → довіра → дзвінок / месенджер
```

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
* Відео галерея робочого процесу
* Блок послуг
* Фінальний контактний CTA
* Контакти та CTA керуються через Django Admin
* Активний / неактивний статус для контенту
* Healthcheck endpoint
* Базові automated tests
* Адаптивна верстка для desktop та mobile

---

## Чого немає в проєкті

У проєкті свідомо не реалізовано:

* онлайн-замовлення;
* форму заявки;
* POST-обробку заявки;
* email-нотифікації;
* spam protection для форми;
* модель `ContactRequest`.

Основна дія користувача — **подзвонити або перейти в месенджер**.

---

## Стек

* Python
* Django
* SQLite для локальної розробки
* PostgreSQL через `DATABASE_URL` для продакшену за потреби
* HTML
* CSS
* Bootstrap
* WhiteNoise
* Gunicorn
* python-decouple
* dj-database-url

---

## Структура проєкту

```text
novogrankor/
├── config/                     # Налаштування Django-проєкту
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/                       # Основний Django app
│   ├── admin.py
│   ├── context_processors.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/                  # HTML-шаблони
│   ├── base.html
│   └── home.html
├── static/                     # Статичні файли
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── logo.png
├── media/                      # Локальні завантаження через адмінку
├── staticfiles/                # Результат collectstatic, не додається в git
├── .env.example                # Приклад env-змінних
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## Основні моделі

У проєкті використовуються такі моделі:

### `Category`

Категорії пам’ятників.

Поля:

* `name`
* `order`
* `is_active`
* `created_at`
* `updated_at`

### `Monument`

Приклади робіт / пам’ятники.

Поля:

* `category`
* `title`
* `image`
* `alt_text`
* `description`
* `order`
* `is_active`
* `created_at`
* `updated_at`

### `Gallery`

Відео галерея робочого процесу.

Поля:

* `title`
* `video`
* `poster`
* `description`
* `order`
* `is_active`
* `created_at`
* `updated_at`

### `SiteSettings`

Singleton-модель для керування основними налаштуваннями сайту.

Поля:

* `phone`
* `phone_display`
* `telegram`
* `viber`
* `whatsapp`
* `logo`
* `hero_title`
* `hero_subtitle`
* `cta_title`
* `cta_subtitle`

У базі має бути лише один запис `SiteSettings`.

---

## Env-змінні

Проєкт використовує `.env`.

Приклад є у файлі:

```text
.env.example
```

Локально потрібно створити файл:

```text
.env
```

Приклад:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=
```

Для генерації `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Локальний запуск

### 1. Клонувати репозиторій

```bash
git clone <repository-url>
cd novogrankor
```

### 2. Створити віртуальне середовище

```bash
python3 -m venv .venv
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
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Створити `.env`

```bash
cp .env.example .env
```

Після цього заповнити `SECRET_KEY`.

### 6. Застосувати міграції

```bash
python manage.py migrate
```

### 7. Створити суперкористувача

```bash
python manage.py createsuperuser
```

### 8. Запустити сервер

```bash
python manage.py runserver
```

Сайт:

```text
http://127.0.0.1:8000/
```

Адмінка:

```text
http://127.0.0.1:8000/admin/
```

Healthcheck:

```text
http://127.0.0.1:8000/healthcheck/
```

---

## Робота з адмінкою

Через Django Admin можна:

1. Керувати категоріями пам’ятників:

   * назва;
   * порядок;
   * активність.

2. Додавати пам’ятники:

   * назва;
   * опис;
   * фото;
   * alt-текст;
   * категорія;
   * порядок;
   * активність.

3. Додавати відео робочого процесу:

   * назва;
   * відеофайл;
   * poster / обкладинка;
   * опис;
   * порядок;
   * активність.

4. Оновлювати налаштування сайту:

   * телефон для посилання;
   * телефон для відображення;
   * Telegram;
   * Viber;
   * WhatsApp;
   * логотип;
   * hero title;
   * hero subtitle;
   * CTA title;
   * CTA subtitle.

---

## Контакти на сайті

Контакти не захардкоджені в шаблонах. Вони керуються через `SiteSettings` в Django Admin.

Телефон для посилання:

```text
+380671234567
```

Телефон для відображення:

```text
+38 (067) 123-45-67
```

У шаблоні телефон використовується так:

```django
{% if site_settings and site_settings.phone %}
    <a href="tel:{{ site_settings.phone }}">
        {{ site_settings.phone_display|default:site_settings.phone }}
    </a>
{% endif %}
```

Telegram, Viber і WhatsApp також задаються в адмінці як повні посилання.

---

## Робота зі статикою

CSS-файл:

```text
static/css/style.css
```

Локальні статичні файли:

```text
static/
```

Продакшен-збірка статичних файлів:

```bash
python manage.py collectstatic --noinput
```

Після виконання команди файли збираються в:

```text
staticfiles/
```

Папка `staticfiles/` не додається в git.

---

## Робота з media-файлами

Фото пам’ятників, логотип, poster-зображення та відео завантажуються через Django Admin і зберігаються в папці:

```text
media/
```

Папка `media/` не додається в git.

Для локального відображення media-файлів у `config/urls.py` має бути підключення через:

```python
from django.conf import settings
from django.conf.urls.static import static
```

та:

```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Тести

У проєкті є базові automated tests для:

* моделей;
* singleton-логіки `SiteSettings`;
* головної сторінки;
* фільтрації active / inactive контенту;
* CTA-контактів;
* відсутності онлайн-форми заявки;
* healthcheck endpoint;
* базової конфігурації Django Admin.

Запуск тестів:

```bash
python manage.py test
```

Очікуваний результат:

```text
OK
```

---

## Production readiness

Проєкт підготовлений до продакшену частково:

* конфіг винесено в `.env`;
* `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` читаються з env;
* `DATABASE_URL` підтримується через `dj-database-url`;
* додано `WhiteNoise`;
* додано `Gunicorn`;
* налаштовано `STATIC_ROOT`;
* додано healthcheck endpoint;
* додано production security settings для `DEBUG=False`.

---

## Gunicorn

Приклад локальної перевірки Gunicorn:

```bash
gunicorn config.wsgi:application
```

Або з явним bind:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## Production check

Для перевірки production-налаштувань потрібно встановити:

```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
SECRET_KEY=your-production-secret-key
```

Після цього запустити:

```bash
python manage.py check --deploy
```

Деякі попередження можуть залежати від конкретного хостингу, HTTPS, reverse proxy та налаштувань домену.

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

---

## Поточний статус

Готовий MVP landing page з call-first бізнес-логікою:

* сайт запускається локально;
* головна сторінка зверстана;
* онлайн-заявки видалені;
* контакти керуються через адмінку;
* CTA ведуть на дзвінок або месенджери;
* каталог наповнюється через адмінку;
* фото пам’ятників виводяться по категоріях;
* відео робочого процесу виводяться з Gallery;
* є floating call button;
* є healthcheck endpoint;
* є automated tests;
* конфіг підготовлений до production-середовища.

---

## Подальші покращення

* Додати favicon
* Додати SEO meta title та description
* Додати Open Graph meta tags
* Додати sitemap.xml
* Додати robots.txt
* Оптимізувати зображення
* Оптимізувати відео для web
* Перевірити mobile UX на реальних пристроях
* Перевірити реальні посилання на Telegram, Viber, WhatsApp
* Перейти з SQLite на PostgreSQL для продакшену за потреби
* Налаштувати деплой
