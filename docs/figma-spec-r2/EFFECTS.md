# EFFECTS — точні значення з Figma (r2)

**Джерело:** Plugin API read-only (`use_figma`: `node.effects / fills / strokes / cornerRadius`) по всіх нодах фреймів `16:3628`, `16:4246`, модалок, `16:4791`, `16:4602`, `16:4632` → `tokens/effects-raw-nodes.json`.
**Важливо:** `get_design_context` ці ефекти **НЕ віддає** (у сирому коді нема `backdrop-blur`) — тому r1 «вгадувала». Нічого не вигадано: нижче тільки зчитані значення.

## Glass-ефект (єдиний тип ефекту в макеті)
У макеті використано новий Figma-ефект **GLASS** (не Background Blur, не Drop Shadow). Параметри однакові для всіх скляних елементів:

| параметр Figma | значення |
|---|---|
| type | `GLASS` |
| radius (frost) | **12** (кнопка-outline hero: **4**) |
| refraction | 0.8 |
| depth | 20 |
| lightAngle | −45° |
| lightIntensity | 0.8 |
| dispersion | 0.5 |
| splay | 0 |
| fill під склом | `rgba(38,38,38,0.2)` (overlay-варіант: `rgba(0,0,0,0.6)`) |
| border / stroke | **немає** (крім outline-кнопки: `#45db00` 1px inside) |
| box-shadow | **немає** (жодного DROP/INNER_SHADOW у файлі) |
| градієнт бордера | **немає** (зовнішній вигляд краю дає light/refraction GLASS) |

CSS-переклад (рішення Frontend, не з Figma): `background: rgba(38,38,38,.2); backdrop-filter: blur(12px)` — Figma frost 12 ≈ CSS blur 6–12px; щоб не було «занадто матово», стартувати з `blur(6px)` і звірити з скріном. Підсвітку краю від lightIntensity 0.8 / angle −45° можна імітувати `box-shadow: inset 1px 1px 0 rgba(255,255,255,.x)` — **це апроксимація, у Figma такої тіні нема**.

## Зведена таблиця по секціях
| секція | елемент (node) | radius | bg | glass frost | border | shadow |
|---|---|---|---|---|---|---|
| Header desk | `16:4049` 1340×107 | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| Header desk роздільник біля адреси | `16:4053` 0×30 | — | — | — | rgba(234,234,234,0.4) 1px | — |
| Header mob | `16:4507` 363×68 | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| Mobile menu | `16:4794` 363×627 | 20 | rgba(38,38,38,0.2) | 12 | розділювачі пунктів 335px rgba(234,234,234,0.4) 1px | — |
| Hero картки-напрямки | `16:4073/4079/4085` 490×70 (mob 363×56) | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| Hero outline-кнопка | `16:4095` 160×44 (mob `16:4544` 362×44) | 12 | rgba(38,38,38,0.2) | **4** | #45db00 1px inside | — |
| Hero бейджі — роздільники | `16:4101`, `16:4105` | — | — | — | **#dadada 1px, висота 71px**, cap ROUND | — |
| Hero бейджі — іконки | Calendar/Ticket/Shield | — | — | — | #45db00 stroke 1.5px | — |
| Чому обирають | 4 картки 320×201 (mob 362×118/135) | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| Послуги — картки | 320×… | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| Послуги — плашки цін | `Frame 15` 320×54 ×12, `16:3804`; Ходова 660×54 (mob 175×40 / 365×40) | 20 (mob 14/12) | rgba(38,38,38,0.2) | 12 | — | — |
| Послуги mob «Завантажити ще» | `16:4340` 362×44 | 12 | rgba(38,38,38,0.2) | 4 | #45db00 1px inside | — |
| Нова пошта | `Frame 15` 624×179 (mob 365×202) | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| НП кроки | 4 картки 640×204/206 (mob 344×152/169) | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| Відгуки | 4 картки 320×253 (mob 225×181) | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| FAQ | рядки 660×70, відкритий 660×161 (mob 364×72 / 153) | 20 | rgba(38,38,38,0.2) | 12 | — | — |
| Футер | смуга `16:4020` 1340×54 (mob 365×54) | 20 | rgba(38,38,38,0.2) | 12 | роздільник mob 0×30 1px | — |
| Модалки 2/4 поля | 569×44 (mob 336×44) | 12 | rgba(38,38,38,0.2) | 12 | — | — |
| Модалки — close ✕ | `Group 1` 2 лінії 43px | — | — | — | 1px (rgba(0,0,0,1) у даних) | — |
| Hero overlay | `16:4048` | 0 | linear rgba(1,11,13,0) → rgba(1,11,13,0.7) | — | — | — |

## Іконки / лінії
- **FAQ-шеврон і стрілки слайдерів** (Відгуки, Роботи, mob Послуги): один SVG `assets/icon-left2-chevron.svg` (Hicon/Outline/Left 2), 5.5×11.5 viewBox, **outlined fill-path** (stroke уже сконвертовано у fill, відповідає 1.5px outline Hicon), fill `#010B0D` у SVG → перефарбувати (`currentColor`). Поворот — `rotate(...)` у сирому коді секції.
- **Тонка галочка НП**: `assets/icon-np-check.svg` (Hicon «Tick»), 29.17×19.69, fill-path `#45DB00` (не stroke). Товщина лінії закладена в path ≈2.5px — це оцінка з геометрії path, окремого strokeWidth нема.
- Буллети послуг: `icon-service-bullet-check.svg` (16×14).
- Іконки Iconly (Calling, Calendar, Arrow) — stroke `#45db00` **1.5px**.

## Повна таблиця по нодах
| секція | node | name | type | size | radius | fill | effect | stroke |
|---|---|---|---|---|---|---|---|---|
| 16:3628/16:3628  | `16:4048` | Rectangle 1 | RECTANGLE | 1440×900 | 0 | GRADIENT_LINEAR[rgba(1,11,13,0)@0 rgba(1,11,13,0.7)@1] op1 | — | — |
| Чому обирають | `16:3653` | Frame 17 | FRAME | 320×201 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Чому обирають | `16:3646` | Frame 16 | FRAME | 320×201 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Чому обирають | `16:3639` | Frame 15 | FRAME | 320×201 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Чому обирають | `16:3632` | Frame 14 | FRAME | 320×201 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3900` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3887` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3873` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3869` | Frame 43 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3852` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3836` | Frame 15 | FRAME | 660×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3804` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3785` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3769` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3753` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3730` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3712` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3697` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Послуги (плашки цін; вкл. Ходова 16:3808) | `16:3682` | Frame 15 | FRAME | 320×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Нова пошта | `16:3909` | Frame 15 | FRAME | 624×179 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Відгуки | `16:3941` | Frame 68 | FRAME | 320×253 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Відгуки | `16:3935` | Frame 67 | FRAME | 320×253 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Відгуки | `16:3929` | Frame 66 | FRAME | 320×253 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Відгуки | `16:3923` | Frame 14 | FRAME | 320×253 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:4001` | Frame 81 | FRAME | 660×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:3996` | Frame 80 | FRAME | 660×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:3991` | Frame 79 | FRAME | 660×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:3986` | Frame 78 | FRAME | 660×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:3980` | Frame 81 | FRAME | 660×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:3975` | Frame 80 | FRAME | 660×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:3970` | Frame 79 | FRAME | 660×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| FAQ | `16:3964` | Frame 78 | FRAME | 660×161 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Футер | `16:4020` | Frame 15 | FRAME | 1340×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| НП: як працює (кроки) | `16:4042` | Frame 62 | FRAME | 640×204 | 20 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| НП: як працює (кроки) | `16:4037` | Frame 61 | FRAME | 640×204 | 20 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| НП: як працює (кроки) | `16:4032` | Frame 60 | FRAME | 640×206 | 20 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| НП: як працює (кроки) | `16:4027` | Frame 14 | FRAME | 640×206 | 20 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| Header | `16:4049` | Frame 2 | FRAME | 1340×107 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Header | `I16:4064;29221:1685` | Stroke 5 | VECTOR | 16×16 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Header | `I16:4064;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Header | `I16:4064;29221:1683` | Stroke 1 | VECTOR | 6×6 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Header | `16:4053` | Vector 1 | VECTOR | 0×30 | 0 | — | — | rgba(234,234,234,0.4) 1px CENTER |
| Hero + бейджі | `16:4108` | Vector | VECTOR | 18×20 | mixed | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Hero + бейджі | `16:4105` | Vector 9 | VECTOR | 0×71 | 0 | — | — | rgba(218,218,218,1) 1px CENTER |
| Hero + бейджі | `I16:4103;437:4282` | Vector | VECTOR | 0×12 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Hero + бейджі | `I16:4103;437:4281` | Vector | VECTOR | 22×16 | mixed | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Hero + бейджі | `16:4101` | Vector 8 | VECTOR | 0×71 | 0 | — | — | rgba(218,218,218,1) 1px CENTER |
| Hero + бейджі | `16:4095` | Frame 8 | FRAME | 160×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 4 | rgba(69,219,0,1) 1px INSIDE |
| Hero + бейджі | `16:4085` | Frame 10 | FRAME | 490×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Hero + бейджі | `16:4079` | Frame 9 | FRAME | 490×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Hero + бейджі | `16:4073` | Frame 8 | FRAME | 490×70 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4177/0:0 Document | `16:4177` | modal  2 | FRAME | 669×538 | 20 | — | — | rgba(69,219,0,1) 1px INSIDE |
| 16:4177/16:4178 Group 1 | `16:4180` | Vector 2 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4177/16:4178 Group 1 | `16:4179` | Vector 1 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4177/16:4181 Frame 17 | `I16:4209;29221:1685` | Stroke 5 | VECTOR | 16×16 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4177/16:4181 Frame 17 | `I16:4209;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4177/16:4181 Frame 17 | `I16:4209;29221:1683` | Stroke 1 | VECTOR | 6×6 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4177/16:4181 Frame 17 | `16:4198` | Frame 6 | FRAME | 569×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4177/16:4181 Frame 17 | `16:4192` | Frame 5 | FRAME | 569×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4177/16:4181 Frame 17 | `16:4186` | Frame 3 | FRAME | 569×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4221/0:0 Document | `16:4221` | modal  3 | FRAME | 669×343 | 20 | — | — | rgba(69,219,0,1) 1px INSIDE |
| 16:4221/16:4222 Group 1 | `16:4224` | Vector 2 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4221/16:4222 Group 1 | `16:4223` | Vector 1 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4221/16:4225 Frame 17 | `I16:4236;29221:1685` | Stroke 5 | VECTOR | 16×16 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4221/16:4225 Frame 17 | `I16:4236;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4221/16:4225 Frame 17 | `I16:4236;29221:1683` | Stroke 1 | VECTOR | 6×6 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4246/16:4246  | `16:4505` | Rectangle 1 | RECTANGLE | 395×805 | 0 | GRADIENT_LINEAR[rgba(1,11,13,0)@0 rgba(1,11,13,0.7)@1] op1 | — | — |
| Mobile чому | `16:4271` | Frame 17 | FRAME | 362×135 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile чому | `16:4264` | Frame 16 | FRAME | 362×118 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile чому | `16:4257` | Frame 15 | FRAME | 362×118 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile чому | `16:4250` | Frame 14 | FRAME | 362×118 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile послуги (+Ходова 16:4339) | `16:4367` | Frame 15 | FRAME | 365×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile послуги (+Ходова 16:4339) | `16:4340` | Frame 8 | FRAME | 362×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 4 | rgba(69,219,0,1) 1px INSIDE |
| Mobile послуги (+Ходова 16:4339) | `16:4335` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile послуги (+Ходова 16:4339) | `16:4324` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile послуги (+Ходова 16:4339) | `16:4313` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile послуги (+Ходова 16:4339) | `16:4302` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile послуги (+Ходова 16:4339) | `16:4291` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile послуги (+Ходова 16:4339) | `I16:4283;23:3847` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile НП | `16:4377` | Frame 15 | FRAME | 365×202 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile НП кроки | `16:4401` | Frame 62 | FRAME | 344×169 | 14 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| Mobile НП кроки | `16:4396` | Frame 61 | FRAME | 344×152 | 14 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| Mobile НП кроки | `16:4391` | Frame 60 | FRAME | 344×152 | 14 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| Mobile НП кроки | `16:4386` | Frame 14 | FRAME | 344×169 | 14 | rgba(0,0,0,0.6) | GLASS radius 12 | — |
| Mobile відгуки | `16:4421` | Frame 15 | FRAME | 225×181 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile відгуки | `16:4415` | Frame 14 | FRAME | 225×181 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4478` | Frame 85 | FRAME | 364×72 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4473` | Frame 84 | FRAME | 364×72 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4468` | Frame 83 | FRAME | 364×72 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4463` | Frame 82 | FRAME | 364×94 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4458` | Frame 81 | FRAME | 364×72 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4453` | Frame 80 | FRAME | 364×72 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4448` | Frame 79 | FRAME | 364×72 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile FAQ | `16:4442` | Frame 78 | FRAME | 364×153 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile футер | `16:4500` | Frame 15 | FRAME | 365×54 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile футер | `16:4486` | Vector 1 | VECTOR | 0×30 | 0 | — | — | rgba(234,234,234,0.4) 1px CENTER |
| Mobile header+hero | `16:4544` | Frame 8 | FRAME | 362×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 4 | rgba(69,219,0,1) 1px INSIDE |
| Mobile header+hero | `16:4534` | Frame 10 | FRAME | 363×56 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile header+hero | `16:4528` | Frame 9 | FRAME | 363×56 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile header+hero | `16:4522` | Frame 8 | FRAME | 363×56 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile header+hero | `16:4507` | Frame 2 | FRAME | 363×68 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile header+hero | `I16:4513;29221:1685` | Stroke 5 | VECTOR | 14×14 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Mobile header+hero | `I16:4513;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Mobile header+hero | `I16:4513;29221:1683` | Stroke 1 | VECTOR | 5×5 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4602/0:0 Document | `16:4602` | Component 1 | COMPONENT_SET | 404×416 | 5 | — | — | rgba(151,71,255,1) 1px INSIDE |
| 16:4602/16:4603 Property 1=Frame 97 | `16:4610` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4602/16:4614 Property 1=Frame 98 | `16:4621` | Frame 15 | FRAME | 175×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4632/16:4633 Component 7 | `16:4640` | Frame 15 | FRAME | 176×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4632/16:4644 Component 8 | `16:4651` | Frame 15 | FRAME | 176×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4632/16:4655 Component 9 | `16:4662` | Frame 15 | FRAME | 176×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4632/16:4666 Component 10 | `16:4673` | Frame 15 | FRAME | 176×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4632/16:4677 Component 11 | `16:4688` | Frame 97 | FRAME | 176×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4632/16:4677 Component 11 | `16:4684` | Frame 15 | FRAME | 176×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4632/16:4692 Component 12 | `16:4699` | Frame 15 | FRAME | 176×40 | 14 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4716/0:0 Document | `16:4716` | modal  4 | FRAME | 364×491 | 20 | — | — | rgba(69,219,0,1) 1px INSIDE |
| 16:4716/16:4717 Group 1 | `16:4719` | Vector 2 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4716/16:4717 Group 1 | `16:4718` | Vector 1 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4716/16:4720 Frame 17 | `I16:4748;29221:1685` | Stroke 5 | VECTOR | 16×16 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4716/16:4720 Frame 17 | `I16:4748;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4716/16:4720 Frame 17 | `I16:4748;29221:1683` | Stroke 1 | VECTOR | 6×6 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4716/16:4720 Frame 17 | `16:4737` | Frame 6 | FRAME | 336×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4716/16:4720 Frame 17 | `16:4731` | Frame 5 | FRAME | 336×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4716/16:4720 Frame 17 | `16:4725` | Frame 3 | FRAME | 336×44 | 12 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| 16:4763/0:0 Document | `16:4763` | modal  5 | FRAME | 364×298 | 20 | — | — | rgba(69,219,0,1) 1px INSIDE |
| 16:4763/16:4764 Group 1 | `16:4766` | Vector 2 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4763/16:4764 Group 1 | `16:4765` | Vector 1 | VECTOR | 43×0 | 0 | — | — | rgba(0,0,0,1) 1px CENTER |
| 16:4763/16:4767 Frame 17 | `I16:4778;29221:1685` | Stroke 5 | VECTOR | 16×16 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4763/16:4767 Frame 17 | `I16:4778;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4763/16:4767 Frame 17 | `I16:4778;29221:1683` | Stroke 1 | VECTOR | 6×6 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| 16:4791/16:4791  | `16:4793` | Rectangle 1 | RECTANGLE | 393×805 | 0 | GRADIENT_LINEAR[rgba(1,11,13,0)@0 rgba(1,11,13,0.7)@1] op1 | — | — |
| Mobile menu (16:4791) | `16:4794` | Frame 2 | FRAME | 363×627 | 20 | rgba(38,38,38,0.2) | GLASS radius 12 | — |
| Mobile menu (16:4791) | `I16:4822;29221:1685` | Stroke 5 | VECTOR | 16×16 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Mobile menu (16:4791) | `I16:4822;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Mobile menu (16:4791) | `I16:4822;29221:1683` | Stroke 1 | VECTOR | 6×6 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Mobile menu (16:4791) | `16:4815` | Vector 7 | VECTOR | 335×0 | 0 | — | — | rgba(234,234,234,0.4) 1px CENTER |
| Mobile menu (16:4791) | `16:4813` | Vector 6 | VECTOR | 335×0 | 0 | — | — | rgba(234,234,234,0.4) 1px CENTER |
| Mobile menu (16:4791) | `16:4811` | Vector 5 | VECTOR | 335×0 | 0 | — | — | rgba(234,234,234,0.4) 1px CENTER |
| Mobile menu (16:4791) | `16:4809` | Vector 4 | VECTOR | 335×0 | 0 | — | — | rgba(234,234,234,0.4) 1px CENTER |
| Mobile menu (16:4791) | `16:4807` | Vector 3 | VECTOR | 335×0 | 0 | — | — | rgba(234,234,234,0.4) 1px CENTER |
| Mobile menu (16:4791) | `I16:4800;29221:1685` | Stroke 5 | VECTOR | 14×14 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Mobile menu (16:4791) | `I16:4800;29221:1684` | Stroke 3 | VECTOR | 3×3 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |
| Mobile menu (16:4791) | `I16:4800;29221:1683` | Stroke 1 | VECTOR | 5×5 | 0 | — | — | rgba(69,219,0,1) 1.5px CENTER |