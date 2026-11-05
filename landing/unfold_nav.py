from django.templatetags.static import static
from django.urls import reverse


def admin_style(_request):
    return static("css/admin/unfold.css")


def admin_logo(_request):
    return static("img/logo.webp")


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
                {"title": "Перший екран", "icon": "image", "link": change("herosettings")},
                {
                    "title": "Заголовки секцій",
                    "icon": "title",
                    "link": change("sectionsettings"),
                },
                {
                    "title": "Форма заявки",
                    "icon": "edit_note",
                    "link": change("bookingsettings"),
                },
                {
                    "title": "Політика конфіденційності",
                    "icon": "policy",
                    "link": change("legalsettings"),
                },
            ],
        },
        {
            "title": "Перший екран",
            "separator": True,
            "items": [
                {
                    "title": "Картки напрямків",
                    "icon": "dashboard",
                    "link": index("herocard"),
                },
                {"title": "Плашки", "icon": "sell", "link": index("herobadge")},
            ],
        },
        {
            "title": "Головна",
            "separator": True,
            "items": [
                {"title": "Переваги", "icon": "verified", "link": index("advantage")},
                {"title": "Послуги і ціни", "icon": "build", "link": index("service")},
                {"title": "Кроки пошти", "icon": "local_shipping", "link": index("mailstep")},
                {"title": "Відгуки", "icon": "reviews", "link": index("review")},
                {"title": "Роботи", "icon": "photo_library", "link": index("workphoto")},
                {"title": "Питання", "icon": "help", "link": index("faqitem")},
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
