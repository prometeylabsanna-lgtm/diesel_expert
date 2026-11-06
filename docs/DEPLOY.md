# Деплой Diesel Expert

## Тест (Vercel) — зараз

- **БД:** SQLite у `/tmp` (ефемерна: cold start може скинути дані)
- **Media:** `/tmp/diesel-expert-media`
- **Env на Vercel:** не потрібні (платформа сама ставить `VERCEL=1`)
- **Адмінка демо:** `admin` / `admin`
- **Static:** WhiteNoise після `collectstatic` на білді

Імпорт з GitHub → Deploy. Root Directory = корінь репо.

Після деплою: відкрити `https://….vercel.app/`, перевірити `/admin/`.

> Preview на Vercel — лише демо. Не зберігати продакшен-контент у цій БД.

## Прод (DigitalOcean) — пізніше

1. App Platform / Droplet + gunicorn (див. типовий `deploy/entrypoint.sh`).
2. PostgreSQL замість SQLite.
3. Постійний `MEDIA` (Spaces / диск).
4. Обов’язкові env: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL`.
5. Прибрати / вимкнути `bootstrap_vercel` у `config/wsgi.py`.
