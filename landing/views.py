import time
from datetime import timedelta

from django.db import connection, transaction
from django.db.utils import OperationalError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from landing.context import build_context
from landing.forms import LeadForm
from landing.models import Lead, SiteSettings
from landing.notify import notify_lead


def home(request):
    return render(request, "home.html", build_context(request))


def privacy(request):
    return render(request, "pages/privacy.html", build_context(request))


def offer(request):
    ctx = build_context(request)
    ctx["legal"] = ctx.get("offer") or {
        "title": "Публічний договір (оферта)",
        "body": "",
    }
    return render(request, "pages/privacy.html", ctx)


def thanks(request):
    return render(request, "pages/thanks.html", build_context(request))


@require_POST
def lead_create(request):
    if (request.POST.get("company") or "").strip():
        return _accept(request)
    form = LeadForm(request.POST)
    if not form.is_valid():
        return _invalid(request, form)
    stored = _create_fresh_lead(
        form.cleaned_data["name"],
        form.cleaned_data["phone"],
        form.cleaned_data["service"],
    )
    if stored is not None:
        lead, site = stored
        notify_lead(lead, site)
    return _accept(request)


def _create_fresh_lead(name, phone, service):
    """Один Lead на телефон за 2 хв. Другий сабміт — тихий успіх, без гонки вкладок."""
    delays = (0, 0.05, 0.15, 0.3)
    last_error = None
    for delay in delays:
        if delay:
            time.sleep(delay)
        try:
            return _insert_fresh_lead(name, phone, service)
        except OperationalError as exc:
            last_error = exc
            if connection.vendor != "sqlite" or "locked" not in str(exc).lower():
                raise
    raise last_error


def _insert_fresh_lead(name, phone, service):
    fresh = timezone.now() - timedelta(minutes=2)
    with transaction.atomic():
        site = _lock_settings_row()
        if Lead.objects.filter(phone=phone, created_at__gte=fresh).exists():
            return None
        lead = Lead.objects.create(
            name=name,
            phone=phone,
            service_title=service,
        )
        return lead, site


def _lock_settings_row():
    if connection.vendor == "sqlite":
        table = connection.ops.quote_name(SiteSettings._meta.db_table)
        column = connection.ops.quote_name(SiteSettings._meta.pk.column)
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA busy_timeout = 5000")
            cursor.execute(f"UPDATE {table} SET {column} = {column} WHERE {column} = 1")
        return SiteSettings.objects.get(pk=1)
    return SiteSettings.objects.select_for_update().get(pk=1)


def _accept(request):
    if request.headers.get("HX-Request") == "true":
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "lead-ok"
        return response
    return redirect("thanks")


def _invalid(request, form):
    context = build_context(request)
    context["form"] = form
    if request.headers.get("HX-Request") == "true":
        response = render(request, "modals/booking_panel.html", context)
        response["HX-Retarget"] = "#modal-booking .modal__panel"
        response["HX-Reswap"] = "innerHTML"
        return response
    context["open_booking"] = True
    return render(request, "home.html", context)
