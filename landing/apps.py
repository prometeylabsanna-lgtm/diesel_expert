from django.apps import AppConfig


class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"
    verbose_name = "Сайт"

    def ready(self):
        from django.db.models.signals import post_migrate

        from landing.admin_recent import register_recent_actions
        from landing.seed import seed_if_empty

        def on_migrate(sender, **kwargs):
            seed_if_empty()

        post_migrate.connect(on_migrate, sender=self, dispatch_uid="landing.seed")
        register_recent_actions()
