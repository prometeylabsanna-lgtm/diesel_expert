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

    def branch(title, icon, children):
        # Unfold вимагає link у батька; клік лише розгортає підменю.
        return {
            "title": title,
            "icon": icon,
            "link": children[0]["link"],
            "items": children,
        }

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
            "collapsible": False,
            "items": [
                branch(
                    "Перший екран",
                    "image",
                    [
                        {
                            "title": "Тексти і фон",
                            "link": change("herosettings"),
                        },
                        {
                            "title": "Картки напрямків",
                            "link": index("herocard"),
                        },
                        {
                            "title": "Плашки",
                            "link": index("herobadge"),
                        },
                    ],
                ),
                branch(
                    "Переваги",
                    "verified",
                    [
                        {
                            "title": "Заголовок",
                            "link": change("advantagessectionsettings"),
                        },
                        {
                            "title": "Картки",
                            "link": index("advantage"),
                        },
                    ],
                ),
                branch(
                    "Послуги",
                    "build",
                    [
                        {
                            "title": "Заголовки",
                            "link": change("servicessectionsettings"),
                        },
                        {
                            "title": "Послуги і ціни",
                            "link": index("service"),
                        },
                    ],
                ),
                {
                    "title": "Нова пошта",
                    "icon": "local_shipping",
                    "link": change("promosectionsettings"),
                },
                branch(
                    "Кроки пошти",
                    "route",
                    [
                        {
                            "title": "Заголовок",
                            "link": change("stepssectionsettings"),
                        },
                        {
                            "title": "Кроки",
                            "link": index("mailstep"),
                        },
                    ],
                ),
                branch(
                    "Відгуки",
                    "reviews",
                    [
                        {
                            "title": "Заголовок",
                            "link": change("reviewssectionsettings"),
                        },
                        {
                            "title": "Список відгуків",
                            "link": index("review"),
                        },
                    ],
                ),
                branch(
                    "Роботи",
                    "photo_library",
                    [
                        {
                            "title": "Заголовок",
                            "link": change("workssectionsettings"),
                        },
                        {
                            "title": "Роботи",
                            "link": index("workphoto"),
                        },
                    ],
                ),
                branch(
                    "Питання",
                    "help",
                    [
                        {
                            "title": "Видимість блоку",
                            "link": change("faqsectionsettings"),
                        },
                        {
                            "title": "Питання",
                            "link": index("faqitem"),
                        },
                    ],
                ),
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
