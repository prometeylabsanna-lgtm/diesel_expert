from django.shortcuts import render

from landing.data import landing_context


def home(request):
    return render(request, "home.html", landing_context())
