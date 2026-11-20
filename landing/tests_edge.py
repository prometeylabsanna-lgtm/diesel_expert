import threading

from django.db import connection
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from landing.forms import LeadForm
from landing.models import Lead
from landing.seed import seed_if_empty

SERVICE = "Ремонт турбін"
PHONE_A = "0681112233"
PHONE_B = "0681112244"


def _post_lead(client, phone=PHONE_A, name="Олег", service=SERVICE, **extra):
    data = {"name": name, "phone": phone, "service": service}
    data.update(extra)
    return client.post("/zayavka/", data, HTTP_HX_REQUEST="true")


class LeadEdgeTests(TestCase):
    def test_get_zayavka_is_not_allowed(self):
        self.assertEqual(self.client.get("/zayavka/").status_code, 405)

    def test_missing_csrf_is_forbidden(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            "/zayavka/",
            {"name": "Олег", "phone": PHONE_A, "service": SERVICE},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Lead.objects.count(), 0)

    def test_plain_post_redirects_to_thanks(self):
        response = self.client.post(
            "/zayavka/",
            {"name": "Олег", "phone": PHONE_A, "service": SERVICE},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("thanks"))
        self.assertEqual(Lead.objects.count(), 1)

    def test_honeypot_accepts_without_lead(self):
        response = self.client.post(
            "/zayavka/",
            {
                "name": "Бот",
                "phone": PHONE_A,
                "service": SERVICE,
                "company": "spam",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["HX-Trigger"], "lead-ok")
        self.assertFalse(response.has_header("HX-Push-Url"))
        self.assertEqual(Lead.objects.count(), 0)

    def test_unknown_service_is_rejected(self):
        response = _post_lead(self.client, service="Неіснуюча послуга")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Оберіть послугу зі списку.")
        self.assertEqual(Lead.objects.count(), 0)

    def test_duplicate_phone_is_silent_success(self):
        first = _post_lead(self.client, name="Олег", service=SERVICE)
        second = _post_lead(self.client, name="Інна", service="Ремонт форсунок")
        self.assertEqual(first.status_code, 204)
        self.assertEqual(second.status_code, 204)
        self.assertEqual(second["HX-Trigger"], "lead-ok")
        lead = Lead.objects.get()
        self.assertEqual(lead.name, "Олег")
        self.assertEqual(lead.service_title, SERVICE)
        self.assertEqual(lead.phone, "+380681112233")

    def test_phone_formats_normalize(self):
        samples = [
            "(068) 806-83-16",
            "+38 068 806 83 16",
            "380688068316",
            "80688068316",
            "0688068316",
        ]
        for raw in samples:
            form = LeadForm({"name": "Олег", "phone": raw, "service": SERVICE})
            self.assertTrue(form.is_valid(), (raw, form.errors))
            self.assertEqual(form.cleaned_data["phone"], "+380688068316")


class CookieEdgeTests(TestCase):
    def test_xhr_sets_cookie_without_redirect(self):
        response = self.client.post(
            reverse("cookie_consent"),
            {"choice": "accepted", "next": "https://evil.example/phish"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 204)
        self.assertNotIn("Location", response)
        self.assertEqual(self.client.cookies["cookie_consent"].value, "accepted")
        self.assertTrue(self.client.cookies["cookie_consent"]["httponly"])


class LeadRaceTests(TransactionTestCase):
    def setUp(self):
        seed_if_empty()

    def test_parallel_posts_keep_one_lead(self):
        barrier = threading.Barrier(2)
        errors = []

        def worker():
            try:
                barrier.wait(5)
                client = Client()
                response = _post_lead(client, phone=PHONE_B, name="Олег")
                if response.status_code != 204:
                    errors.append(response.status_code)
            except Exception as exc:
                errors.append(repr(exc))
            finally:
                connection.close()

        threads = [threading.Thread(target=worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(10)
            if thread.is_alive():
                errors.append("timeout")
        self.assertFalse(errors, errors)
        self.assertEqual(Lead.objects.filter(phone="+380681112244").count(), 1)
