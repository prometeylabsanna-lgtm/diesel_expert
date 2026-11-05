import json
import logging
import urllib.request

from django.core.mail import send_mail

log = logging.getLogger(__name__)


def notify_lead(lead, site):
    text = (
        "Нова заявка Diesel Expert\n"
        f"Ім’я: {lead.name}\n"
        f"Телефон: {lead.phone}\n"
        f"Послуга: {lead.service_title}"
    )
    if site.notify_email:
        send_mail(
            "Нова заявка Diesel Expert",
            text,
            None,
            [site.notify_email],
            fail_silently=True,
        )
    token = (site.telegram_bot_token or "").strip()
    chat = (site.telegram_chat_id or "").strip()
    if not token or not chat:
        return
    payload = json.dumps({"chat_id": chat, "text": text}).encode()
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=4) as response:
            response.read()
    except Exception:
        log.warning("Не вдалося надіслати заявку в Telegram")
