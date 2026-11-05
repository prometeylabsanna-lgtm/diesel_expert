from django.urls import path

from landing.views import home, lead_create, privacy, thanks

urlpatterns = [
    path("", home, name="home"),
    path("zayavka/", lead_create, name="lead_create"),
    path("dyakuyemo/", thanks, name="thanks"),
    path("polityka-konfidentsiynosti/", privacy, name="privacy"),
]
