"""Технічні SEO-ендпоінти: robots.txt, sitemap.xml, llms.txt."""

from __future__ import annotations

from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET


def _origin(request) -> str:
    return request.build_absolute_uri("/").rstrip("/")


@require_GET
def robots_txt(request):
    origin = _origin(request)
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /zayavka/",
            "Disallow: /dyakuyemo/",
            "",
            "# Yandex: головне дзеркало (Google ігнорує Host)",
            f"Host: {origin}",
            f"Sitemap: {origin}/sitemap.xml",
            "",
        ]
    )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


@require_GET
def sitemap_xml(request):
    origin = _origin(request)
    lastmod = timezone.now().date().isoformat()
    pages = [
        ("home", "1.0", "weekly"),
        ("privacy", "0.3", "monthly"),
        ("offer", "0.3", "monthly"),
    ]
    urls = []
    for name, priority, changefreq in pages:
        loc = f"{origin}{reverse(name)}"
        urls.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    return HttpResponse(body, content_type="application/xml; charset=utf-8")


@require_GET
def llms_txt(request):
    origin = _origin(request)
    body = f"""# Diesel Expert

> Сервісний центр дизельних систем у Луцьку: діагностика та ремонт турбін, форсунок, ПНВТ, ГБЦ, двигунів; прийом агрегатів Новою Поштою по всій Україні.

Мова сайту: українська (`uk`). Публічні сторінки нижче — пріоритет для сканування людьми та LLM-агентами. Адмінку, форму заявки та сторінку подяки ігноруйте.

## Головне

- [Головна]({origin}/): послуги, ціни «від», ремонт поштою, FAQ, контакти (м. Луцьк, вул. Мирослава Скорика 2А)
- [Політика конфіденційності]({origin}/polityka-konfidentsiynosti/): обробка персональних даних заявок
- [Публічний договір]({origin}/publichnyy-dogovir/): умови надання послуг

## Послуги (якірні блоки на головній)

- [Ремонт турбін]({origin}/#services): діагностика, збірка, монтаж/демонтаж
- [Ремонт форсунок]({origin}/#services): Common Rail, стенд, кодування
- [Ремонт ПНВТ]({origin}/#services): діагностика та встановлення
- [Ремонт поштою]({origin}/#promo): відправка агрегатів Новою Поштою по Україні

## Технічне

- [robots.txt]({origin}/robots.txt)
- [sitemap.xml]({origin}/sitemap.xml)

## Optional

- [Запис / контакти]({origin}/#booking): телефон і форма заявки на сайті
"""
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


@require_GET
def llm_txt(request):
    """Аліас застарілої назви → той самий вміст, що /llms.txt."""
    return llms_txt(request)
