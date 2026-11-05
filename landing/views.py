from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
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


def thanks(request):
    return render(request, "pages/thanks.html", build_context(request))


@require_POST
def lead_create(request):
    if (request.POST.get("company") or "").strip():
        return _accept(request)
    form = LeadForm(request.POST)
    if not form.is_valid():
        return _invalid(request, form)
    phone = form.cleaned_data["phone"]
    fresh = timezone.now() - timedelta(minutes=2)
    if not Lead.objects.filter(phone=phone, created_at__gte=fresh).exists():
        lead = Lead.objects.create(
            name=form.cleaned_data["name"],
            phone=phone,
            service_title=form.cleaned_data["service"],
        )
        notify_lead(lead, SiteSettings.objects.get(pk=1))
    return _accept(request)


def _accept(request):
    if request.headers.get("HX-Request") == "true":
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "lead-ok"
        response["HX-Push-Url"] = reverse("thanks")
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
