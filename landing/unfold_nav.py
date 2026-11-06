from django.templatetags.static import static
from django.urls import reverse


def admin_style(_request):
    return static("css/admin/unfold.css")


def admin_logo(_request):
    return static("img/logo.webp")


def admin_favicon_ico(_request):
    return static("img/favicon.ico")


def admin_favicon_32(_request):
    return static("img/favicon-32.png")


def admin_favicon_48(_request):
    return static("img/favicon-48.png")


def admin_apple_touch(_request):
    return static("img/apple-touch-icon.png")


def navigation(_request):
    def change(model_name):
        return reverse(f"admin:landing_{model_name}_change", args=[1])

    def index(model_name):
        return reverse(f"admin:landing_{model_name}_changelist")

    return [
        {
            "title": "Налаштування",
            "separator": True,
            "items": [
                {"title": "Контакти", "icon": "call", "link": change("contactssettings")},
                {
                    "title": "Форма заявки",
                    "icon": "edit_note",
                    "link": change("bookingsettings"),
                },
            ],
        },
        {
            "title": "Головна — блоки",
            "separator": True,
            "items": [
                {
                    "title": "Перший екран",
                    "icon": "image",
                    "link": change("herosettings"),
                },
                {
                    "title": "Картки напрямків",
                    "icon": "dashboard",
                    "link": index("herocard"),
                },
                {"title": "Плашки", "icon": "sell", "link": index("herobadge")},
                {
                    "title": "Переваги (заголовок)",
                    "icon": "title",
                    "link": change("advantagessectionsettings"),
                },
                {
                    "title": "Переваги (картки)",
                    "icon": "verified",
                    "link": index("advantage"),
                },
                {
                    "title": "Послуги (заголовки)",
                    "icon": "title",
                    "link": change("servicessectionsettings"),
                },
                {
                    "title": "Послуги і ціни",
                    "icon": "build",
                    "link": index("service"),
                },
                {
                    "title": "Нова пошта",
                    "icon": "local_shipping",
                    "link": change("promosectionsettings"),
                },
                {
                    "title": "Кроки (заголовок)",
                    "icon": "title",
                    "link": change("stepssectionsettings"),
                },
                {
                    "title": "Кроки пошти",
                    "icon": "route",
                    "link": index("mailstep"),
                },
                {
                    "title": "Відгуки (заголовок)",
                    "icon": "title",
                    "link": change("reviewssectionsettings"),
                },
                {"title": "Відгуки", "icon": "reviews", "link": index("review")},
                {
                    "title": "Роботи (заголовок)",
                    "icon": "title",
                    "link": change("workssectionsettings"),
                },
                {
                    "title": "Роботи",
                    "icon": "photo_library",
                    "link": index("workphoto"),
                },
                {"title": "Питання", "icon": "help", "link": index("faqitem")},
            ],
        },
        {
            "title": "Юридичні сторінки",
            "separator": True,
            "items": [
                {
                    "title": "Політика конфіденційності",
                    "icon": "policy",
                    "link": change("privacysettings"),
                },
                {
                    "title": "Публічний договір",
                    "icon": "gavel",
                    "link": change("offersettings"),
                },
            ],
        },
        {
            "title": "Заявки",
            "separator": True,
            "items": [
                {"title": "Усі заявки", "icon": "inbox", "link": index("lead")},
            ],
        },
        {
            "title": "Система",
            "separator": True,
            "items": [
                {
                    "title": "Недавні дії",
                    "icon": "history",
                    "link": reverse("admin:recent-actions"),
                },
                {
                    "title": "Користувачі",
                    "icon": "person",
                    "link": reverse("admin:auth_user_changelist"),
                },
            ],
        },
    ]
