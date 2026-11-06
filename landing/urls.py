from django.urls import path

from landing.seo import llm_txt, llms_txt, robots_txt, sitemap_xml
from landing.views import home, lead_create, offer, privacy, thanks

urlpatterns = [
    path("", home, name="home"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
    path("llms.txt", llms_txt, name="llms_txt"),
    path("llm.txt", llm_txt, name="llm_txt"),
    path("zayavka/", lead_create, name="lead_create"),
    path("dyakuyemo/", thanks, name="thanks"),
    path("polityka-konfidentsiynosti/", privacy, name="privacy"),
    path("publichnyy-dogovir/", offer, name="offer"),
]
