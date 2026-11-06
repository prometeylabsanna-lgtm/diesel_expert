from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from landing.models import Service, SiteSettings


class AdminCmsSmokeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "a@b.c", "pass")
        self.client = Client()
        self.client.force_login(self.user)
        SiteSettings.objects.get_or_create(pk=1, defaults={
            "phone": "068 806 83 16",
            "address_line_1": "м. Луцьк",
            "schedule": "тест",
            "copyright": "©",
            "cta_service": "Запис",
            "cta_diagnostics": "Діагностика",
            "hero_title": "Hero",
            "hero_primary_cta": "A",
            "hero_secondary_cta": "B",
            "hero_secondary_url": "#",
            "advantages_title": "Adv",
            "services_title": "Svc",
            "services_lead": "Lead",
            "services_more_label": "More",
            "promo_title": "Promo",
            "steps_title": "Steps",
            "reviews_title": "Reviews",
            "works_title": "Works",
            "booking_title": "Book",
            "booking_lead": "Lead",
            "booking_name_placeholder": "Name",
            "booking_phone_placeholder": "Phone",
            "booking_service_placeholder": "Svc",
            "booking_submit": "Go",
            "booking_direct": "Direct",
            "success_title": "Ok",
            "success_lead": "Lead",
            "success_home": "Home",
            "success_direct": "Direct",
            "privacy_label": "Privacy",
            "privacy_title": "Privacy",
            "privacy_body": "Body",
        })

    def test_privacy_and_offer_admin(self):
        for name in ("privacysettings", "offersettings", "herosettings", "promosectionsettings"):
            url = f"/admin/landing/{name}/1/change/"
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, name)

    def test_service_slug_readonly_and_auto(self):
        service = Service.objects.create(title="Тестова послуга", bullets="a", image_static="x.webp")
        self.assertTrue(service.slug)
        response = self.client.get(f"/admin/landing/service/{service.pk}/change/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cms-countable")
