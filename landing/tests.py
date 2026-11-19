from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from landing.models import Lead, Service, ServicePrice, SiteSettings

CREDIT_URL = "https://www.prometeylabs.com/corporate-website-v2/"


class LandingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_renders_seeded_hero(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "СПЕЦІАЛІЗОВАНИЙ АВТОСЕРВІС У ЛУЦЬКУ")
        self.assertContains(response, "DIESEL")
        self.assertContains(response, "hero__brand-accent")
        self.assertContains(response, "EXPERT")
        self.assertContains(response, "ДІАГНОСТУЄМО ТОЧНО — РЕМОНТУЄМО НАДІЙНО")
        self.assertContains(response, "Дізнатись більше")
        self.assertContains(response, "Записатись</span>")
        self.assertContains(response, "Ремонт ДВЗ")
        self.assertContains(response, "Політика конфіденційності")

    def test_copy_fixes_from_client_notes(self):
        response = self.client.get("/")
        self.assertContains(response, "будь-якої")
        self.assertNotContains(response, "будь якої")
        self.assertContains(response, "турбокомпресорів")
        self.assertNotContains(response, "турбокомпрессор")
        self.assertContains(response, "(кодування)")
        self.assertNotContains(response, "(Кодування)")
        self.assertContains(response, "механічних")
        self.assertContains(response, "гідравлічних")
        self.assertContains(response, "електричних")
        self.assertContains(response, "Консультація безкоштовна")
        injectors = Service.objects.get(title="Ремонт форсунок")
        pnvt = Service.objects.get(title="Ремонт ПНВТ")
        self.assertEqual(injectors.image_static, "img/services/pnvt.webp")
        self.assertEqual(pnvt.image_static, "img/services/injectors.webp")
        steering = Service.objects.get(title="Ремонт рульових рейок")
        self.assertIn("  механічних,", steering.bullets)
        self.assertIn("  гідравлічних,", steering.bullets)
        self.assertIn("  електричних.", steering.bullets)
        self.assertContains(response, "механічних,")
        self.assertContains(response, "гідравлічних,")
        self.assertContains(response, "електричних.")

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


class SeoSystemFilesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response["Content-Type"])
        body = response.content.decode()
        self.assertIn("Disallow: /admin/", body)
        self.assertIn("Disallow: /zayavka/", body)
        self.assertIn("Disallow: /dyakuyemo/", body)
        self.assertIn("Sitemap:", body)
        self.assertIn("/sitemap.xml", body)

    def test_sitemap_xml(self):
        response = self.client.get(reverse("sitemap_xml"))
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn("<urlset", body)
        self.assertIn(reverse("home"), body)
        self.assertIn(reverse("privacy"), body)
        self.assertIn(reverse("offer"), body)
        self.assertNotIn(reverse("thanks"), body)

    def test_llms_txt_and_alias(self):
        for name in ("llms_txt", "llm_txt"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            body = response.content.decode()
            self.assertIn("# Diesel Expert", body)
            self.assertIn("Луцьк", body)
            self.assertIn("/polityka-konfidentsiynosti/", body)

    def test_home_links_llms_describedby(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'rel="describedby"')
        self.assertContains(response, reverse("llms_txt"))


class SectionVisibilityTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_reviews_section_hidden_by_default_and_can_be_shown(self):
        site = SiteSettings.objects.get(pk=1)
        self.assertFalse(site.show_reviews_section)
        hidden = self.client.get("/")
        self.assertNotContains(hidden, 'id="reviews"')
        self.assertNotContains(hidden, 'href="#reviews"')
        self.assertNotContains(hidden, ">Відгуки</a>")
        site.show_reviews_section = True
        site.save(update_fields=["show_reviews_section"])
        shown = self.client.get("/")
        self.assertContains(shown, 'id="reviews"')
        self.assertContains(shown, 'href="#reviews"')
        self.assertContains(shown, ">Відгуки</a>")

    def test_faq_section_can_be_hidden(self):
        site = SiteSettings.objects.get(pk=1)
        site.show_faq_section = False
        site.save(update_fields=["show_faq_section"])
        response = self.client.get("/")
        self.assertNotContains(response, 'id="faq-title"')
        self.assertNotContains(response, '"@type":"FAQPage"')


class SeoOnPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_meta_og_and_jsonld(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ремонт дизеля в Луцьку")
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'property="og:image"')
        self.assertContains(response, 'property="og:image:width" content="1200"')
        self.assertContains(response, 'type="application/ld+json"')
        self.assertContains(response, '"@type":"AutoRepair"')
        self.assertContains(response, '"@type":"FAQPage"')
        self.assertContains(response, 'fetchpriority="high"')
        self.assertContains(response, 'class="hero__bg"')
        self.assertContains(response, "Ремонт турбін — Diesel Expert, Луцьк")

    def test_thanks_is_noindex(self):
        response = self.client.get(reverse("thanks"))
        self.assertContains(response, 'name="robots" content="noindex, nofollow"')

    def test_privacy_has_breadcrumb_schema(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, '"@type":"BreadcrumbList"')
        self.assertContains(response, 'rel="canonical"')


class LegalPagesContentTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_privacy_has_real_policy(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, "Які дані ми збираємо")
        self.assertContains(response, "ім’я")
        self.assertContains(response, "номер телефону")
        self.assertContains(response, "Сайт збирає файли cookie")
        self.assertContains(response, "[назва ФОП / ТОВ]")
        self.assertNotContains(response, "тимчасовий і стоїть")
        self.assertContains(response, "<p>")
        self.assertNotContains(response, "&lt;p&gt;")

    def test_offer_has_real_contract(self):
        response = self.client.get(reverse("offer"))
        self.assertContains(response, "публічною офертою")
        self.assertContains(response, "Предмет договору")
        self.assertContains(response, "Нову Пошту")
        self.assertContains(response, "м. Луцьк")
        self.assertContains(response, "068 806 83 16")
        self.assertContains(response, "[ЄДРПОУ / ІПН]")
        self.assertNotContains(response, "буде замінений")
        self.assertNotContains(response, "офферта")

    def test_richtext_unescapes_stored_html_entities(self):
        from landing.templatetags.landing_extras import richtext

        rendered = richtext("&lt;p&gt;Тест абзацу&lt;/p&gt;")
        self.assertIn("<p>", str(rendered))
        self.assertNotIn("&lt;p&gt;", str(rendered))
