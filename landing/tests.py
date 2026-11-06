from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from landing.models import Lead, ServicePrice, SiteSettings

CREDIT_URL = "https://www.prometeylabs.com/corporate-website-v2/"


class LandingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_renders_seeded_hero(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Діагностуємо точно - ремонтуємо надійно")
        self.assertContains(response, "Політика конфіденційності")

    def test_price_edit_reaches_the_page(self):
        price = ServicePrice.objects.get(service__title="Ремонт турбін", sort=1)
        price.value = "9 999 грн"
        price.save()
        response = self.client.get("/")
        self.assertContains(response, "9 999 грн")

    def test_hero_title_comes_from_settings(self):
        site = SiteSettings.objects.get(pk=1)
        site.hero_title = "Тестовий заголовок"
        site.save()
        self.assertContains(self.client.get("/"), "Тестовий заголовок")

    def test_lead_is_stored(self):
        response = self.client.post(
            "/zayavka/",
            {"name": "Олег", "phone": "0688068316", "service": "Ремонт турбін"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["HX-Trigger"], "lead-ok")
        self.assertEqual(response["HX-Push-Url"], "/dyakuyemo/")
        lead = Lead.objects.get()
        self.assertEqual(lead.phone, "+380688068316")
        self.assertEqual(lead.status, Lead.Status.NEW)

    def test_invalid_phone_does_not_create_lead(self):
        response = self.client.post(
            "/zayavka/",
            {"name": "Олег", "phone": "123", "service": "Ремонт турбін"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Вкажіть")
        self.assertEqual(Lead.objects.count(), 0)

    def test_name_rejects_symbols(self):
        response = self.client.post(
            "/zayavka/",
            {"name": "Олег!!!", "phone": "0688068316", "service": "Ремонт турбін"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "літери")
        self.assertEqual(Lead.objects.count(), 0)

    def test_phone_rejects_letters(self):
        response = self.client.post(
            "/zayavka/",
            {"name": "Олег", "phone": "068abc8316", "service": "Ремонт турбін"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "літери")
        self.assertEqual(Lead.objects.count(), 0)

    def test_honeypot_is_dropped(self):
        self.client.post(
            "/zayavka/",
            {
                "name": "Бот",
                "phone": "0688068316",
                "service": "Ремонт турбін",
                "company": "spam",
            },
        )
        self.assertEqual(Lead.objects.count(), 0)

    def test_privacy_and_thanks_pages(self):
        self.assertContains(self.client.get("/polityka-konfidentsiynosti/"), "Політика")
        self.assertContains(self.client.get("/dyakuyemo/"), "Дякуємо за заявку")
        self.assertContains(
            self.client.get("/polityka-konfidentsiynosti/"),
            'href="/#services"',
        )

    def test_admin_leads_are_ukrainian(self):
        user = get_user_model().objects.create_superuser(
            "admin",
            "admin@example.com",
            "DieselExpert-Test-1",
        )
        self.client.force_login(user)
        empty = self.client.get("/admin/landing/lead/")
        self.assertContains(empty, "Нічого не знайдено")
        self.assertNotContains(empty, "No results found")
        self.assertNotContains(empty, "За Статус")
        self.assertContains(empty, 'placeholder="Від"')
        recent = self.client.get("/admin/recent-actions/")
        self.assertContains(recent, "recent-actions-page")
        self.assertContains(recent, "Недавніх дій ще немає")


class FooterDeveloperLinkTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_has_nofollow_credit_link(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, CREDIT_URL)
        self.assertContains(response, "nofollow")
        self.assertContains(response, ">PrometeyLabs</a>")
        self.assertContains(response, "Дизайн розроблено")

    def test_inner_pages_show_credit_without_link(self):
        for url_name in ("privacy", "offer", "thanks"):
            response = self.client.get(reverse(url_name))
            self.assertContains(response, "PrometeyLabs")
            self.assertContains(response, "Дизайн розроблено")
            self.assertNotContains(response, CREDIT_URL)
            self.assertNotContains(response, "footer__credit-link")
