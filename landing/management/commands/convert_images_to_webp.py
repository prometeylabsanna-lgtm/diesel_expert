"""Конвертує завантажені media/ (і опційно static/img) у WebP."""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from landing.image_webp import convert_path_to_webp

_SKIP_NAME_PARTS = (
    "favicon",
    "apple-touch",
    "icon-192",
    "icon-512",
    "thumb-fuel",
    "thumb-turbo",
    "thumb-gbc",
)


class Command(BaseCommand):
    help = "Переводить растрові зображення в WebP. За замовчуванням лише MEDIA_ROOT."

    def add_arguments(self, parser):
        parser.add_argument(
            "--static",
            action="store_true",
            help="Також обробити static/img (пропускає favicon і mask-іконки hero).",
        )
        parser.add_argument(
            "--keep-source",
            action="store_true",
            help="Не видаляти оригінал після конвертації.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Лише показати, що буде змінено.",
        )

    def handle(self, *args, **options):
        roots = [Path(settings.MEDIA_ROOT)]
        if options["static"]:
            roots.append(Path(settings.BASE_DIR) / "static" / "img")
        keep = options["keep_source"]
        dry = options["dry_run"]
        exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff"}
        done = 0
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in exts:
                    continue
                low = path.name.lower()
                if any(part in low for part in _SKIP_NAME_PARTS):
                    continue
                if dry:
                    self.stdout.write(f"would convert: {path}")
                    done += 1
                    continue
                out = convert_path_to_webp(path, delete_source=not keep)
                if out:
                    self.stdout.write(self.style.SUCCESS(f"{path.name} → {out.name}"))
                    done += 1
        self.stdout.write(self.style.NOTICE(f"Оброблено: {done}"))
