# DieselExpert — figma-spec r2 (per-section raw design_context)

Figma: https://www.figma.com/design/dVjiuXFknESrOGvKPX4Wh4/PrometeyLabsProjects?node-id=16-3627 · fileKey `dVjiuXFknESrOGvKPX4Wh4`.
r1 (`docs/figma-spec/`) — оглядовий; **r2 — джерело для верстки**.

## Рішення Анни (обов'язково)
- Футер: графік **ПН–НД 9:00–20:00** (у макеті інший текст — ігнорувати).
- Футер: **без карти** (mask-зображення `img-footer-mask*` не використовувати як карту).

## Файли
Кожен файл = **дослівний** вихід `get_design_context` (React+Tailwind, `disableCodeConnect`, `forceCode`). Не копіювати як код — перекладати у Django/BEM. Тимчасові URL у коді → `assets/MANIFEST.md`.

| # | desktop (`16:3628`) | node | mobile (`16:4246`) | node |
|---|---|---|---|---|
| 01 | desktop/01-header.tsx | 16:4049 | mobile/01-header.tsx | 16:4507 |
| 02 | desktop/02-hero-badges.tsx | 16:4069 | mobile/02-hero-badges.tsx | 16:4519 |
| 03 | desktop/03-why-choose.tsx | 16:3629 | mobile/03-why-choose.tsx | 16:4247 |
| 04 | desktop/04-services-prices.tsx | 16:3660 | mobile/04-services-prices.tsx | 16:4278 |
| 05 | desktop/05-khodova.tsx | **16:3808** (Frame 54, всередині 16:3660) | mobile/05-khodova.tsx | **16:4339** (Frame 98: «Завантажити ще» + Ходова 16:4343) |
| 06 | desktop/06-nova-poshta.tsx | 16:3904 | mobile/06-nova-poshta.tsx | 16:4373 |
| 06b | desktop/06b-nova-poshta-steps.tsx | 16:4026 (заголовок 16:4025, фон 16:4024) | mobile/06b-nova-poshta-steps.tsx | 16:4383 (фон 16:4382) |
| 07 | desktop/07-reviews.tsx | 16:3914 | mobile/07-reviews.tsx | 16:4406 |
| 08 | desktop/08-works.tsx | 16:3947 | mobile/08-works.tsx | 16:4427 |
| 09 | desktop/09-faq.tsx | 16:3960 | mobile/09-faq.tsx | 16:4439 |
| 10 | desktop/10-footer.tsx | 16:4006 | mobile/10-footer.tsx | 16:4483 |

Модалки/компоненти (сирий код з r1): `docs/figma-spec/raw/m2…m5, c1, f99, mhero`.

## Ефекти по секціях (коротко, деталі — EFFECTS.md)
Всі скляні поверхні: Figma **GLASS** frost 12 (refraction 0.8, depth 20, light −45° / 0.8, dispersion 0.5) + bg `rgba(38,38,38,0.2)`, radius 20 (плашки/поля 12–14), **без border, без shadow**.
- Header: GLASS 12, bg rgba(38,38,38,0.2), r20; роздільник 1px rgba(234,234,234,0.4) h30.
- Hero: картки GLASS 12 r20; outline-CTA GLASS 4 + #45db00 1px r12; роздільники бейджів #dadada 1px h71.
- Чому / послуги / плашки цін / НП / кроки / відгуки / FAQ / футер-смуга: GLASS 12, rgba(38,38,38,0.2), r20.
- Галочка НП: `assets/icon-np-check.svg` (fill path). Шеврон FAQ і стрілки: `assets/icon-left2-chevron.svg`.

**Чому r1 була «навмання»:** `get_design_context` не експортує GLASS-ефект; значення зчитано окремо через Plugin API (`tokens/effects-raw-nodes.json`).
