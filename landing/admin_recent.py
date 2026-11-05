from django.contrib.admin.models import LogEntry
from django.template.response import TemplateResponse


def register_recent_actions():
    from django.contrib import admin

    site = admin.site
    if getattr(site, "_diesel_recent", False):
        return
    site._diesel_recent = True
    original = site.get_urls

    def recent(request):
        entries = LogEntry.objects.select_related("content_type", "user")
        if not request.user.is_superuser:
            entries = entries.filter(user_id=request.user.pk)
        return TemplateResponse(
            request,
            "admin/recent_actions.html",
            {
                **site.each_context(request),
                "title": "Недавні дії",
                "entries": entries[:40],
            },
        )

    def get_urls():
        from django.urls import path

        custom = [
            path(
                "recent-actions/",
                site.admin_view(recent),
                name="recent-actions",
            )
        ]
        return custom + original()

    site.get_urls = get_urls
