# DieselExpert — Build Spec (Figma → Frontend)

> Build spec для Frontend. Не DESIGN.md / не SSOT (G-DESIGN-SIGN — Design Lead).

## 0. Контекст
- **Репо порожнє на старті** (`/Users/olegbonislavskyi/Sites/DieselExpert`, git ініціалізовано цим комітом, гілка `diesel/layout`, без remote).
- Figma: https://www.figma.com/design/dVjiuXFknESrOGvKPX4Wh4/PrometeyLabsProjects?node-id=16-3627
- fileKey `dVjiuXFknESrOGvKPX4Wh4`, сторінка Diesel `16:3627`.
- **Токени зібрані з design_context нод (Figma Variables порожні)** → `tokens/tokens.md`, `tokens/tokens.json`.
- Сирий design_context (React+Tailwind референс, НЕ для копіювання) → `raw/*.design-context.tsx.txt` (node ids у `data-node-id`).
- Code Connect не використовувався (оркестратор: не потрібен; виклики з `disableCodeConnect: true`).

## 1. Стек очікування
Django templates + CSS (BEM) + мінімальний vanilla JS (бургер, модалки, FAQ-акордеон, слайдер відгуків/робіт). Кожна секція — окремий partial під майбутні моделі / SiteBlock / адмінку Unfold. Бекенду на цьому етапі немає: контент статичний у шаблонах, але структурований як списки (див. «поля моделі»). Без React/Tailwind.

## 2. Брейкпоінти
| BP | Figma | статус |
|---|---|---|
| desktop | 1440 (`16:3628`, висота 7368) | є |
| mobile | 393 (`16:4246` full, `16:4791` viewport 393×828 = відкрите меню) | є |
| tablet | — | **відсутній у Figma**. Пропозиція: 768–1023 = mobile-розкладка з 2 колонками карток; open question |

## 3. Desktop 1440 — секції по порядку
| # | Секція | node | Контент | Повторювані → поля моделі |
|---|---|---|---|---|
| 1 | Hero bg | `16:4047` фото + `16:4048` gradient overlay | фото майстерні | `hero.bg_image` |
| 2 | Header | `16:4049` Frame 2 | лого (`image 1`), адреса «м. Луцьк вул, Мирослава Скорика 2А», меню: Головна / Послуги / Ціни / Про нас / Контакти; телефон 068 806 83 16 (іконка Calling); CTA «Записатись на сервіс» (Calendar) → modal 2 | `NavItem{label,url}`, `SiteSettings{phone,address,logo}` |
| 3 | Hero content | `16:4069` Frame 110 | H1 54 «Діагностуємо точно - ремонтуємо надійно»; 3 картки-напрямки з фото (Mask group `16:4075/4081/4087`): «Паливна система: діагностика та ремонт», «Ремонт турбін», «Шліфування ГБЦ та колекторів» (стрілка Arrow-Right); CTA «Записатись на діагностику»; 3 переваги з іконками: «Швидкий запис» (Calendar), «Консультація безкоштовно» (Ticket Expired), «Гарантія на роботи» (Shield Tick) | `HeroCard{title,image,url}`, `HeroBadge{icon,text}` |
| 4 | Чому обирають | `16:3629` Frame 19 | H2 «Чому обирають Diesel Expert»; 4 картки: Досвід (Award) «Понад 10 років у сфері дизельних систем», Гарантія (Setting), Якісні запчастини (Shield Tick) «…брендами», Прозорі ціни (Wallet) «…прихованих платежів» | `Advantage{icon,title,text}` |
| 5 | Наші послуги | `16:3660` Frame 57 | H2 «Наші послуги», підзаг. «Комплексний ремонт та обслуговування дизельних автомобілів»; сітка карток 320px (≈14): фото, назва, опис, буллети з ✓ (Vector), «Ціна ремонту від: N грн» (lime), «Консультація безкоштовна». Послуги: Ремонт турбін 3000, Ремонт форсунок 1000, Ремонт ПНВТ 4000, Ремонт рульових рейок (механічних/гідравлічних/електричних), Поточний ремонт / кап. ремонт ДВЗ, Ремонт ГБЦ 30000 / 2500, Очищення DPF 3000, ГРМ 3500, Кондиціонер R134a 1500, Ходова (амортизація, важелі, кермове, стабілізатори, трансмісія, гальма — «*розраховується індивідуально»), Двомасовий маховик 4500, Пневмопідвіска (реставрація від / демонтаж від), Мех. обробка агрегатів 800 | `Service{title,image,description,bullets[],price_from,price_label,price2_label?,price2?,note?}` |
| 6 | Ремонт Новою поштою (promo) | `16:3904` Frame 59 | H2 «Ремонт агрегатів Новою поштою по всій Україні», текст «Знаходитесь в іншому місті…», фото (`image 7`), CTA | `PromoBlock{title,text,image,cta}` |
| 7 | Як працює ремонт по пошті | `16:4024` Frame 65 (title `16:4025`, steps `16:4026` Frame 63) | 4 кроки з номерами 01–04 (lime): Заявка та консультація / Діагностика та узгодження / Ремонт і тестування / Доставка та оплата | `Step{num,title,text}` |
| 8 | Відгуки | `16:3914` Frame 73 | H2 «Відгуки»; картки: аватар-літера («М»), ім'я «Максим», текст; стрілки Left2 (слайдер) | `Review{name,initial,text,rating?}` |
| 9 | Наші роботи | `16:3947` Frame 76 | H2 «Наші роботи»; галерея фото (`image 6/7/8` `16:3957–3959`), слайдер | `WorkPhoto{image,alt}` |
| 10 | FAQ | `16:3960` Frame 85 | H2 «Відповіді на питання»; 8 питань-акордеон (перше відкрите): Які автомобілі ви обслуговуєте? / Чи можна дізнатися вартість заздалегідь? / Скільки часу займає ремонт? / Чи надаєте гарантію? / Чи можна відправити деталь поштою? / Як відбувається ремонт поштою? / Чи потрібен попередній запис? / Чи використовуєте оригінальні запчастини? | `FaqItem{question,answer,order}` |
| 11 | Footer | `16:4006` Frame 92 | лого, меню, графік («Субота з 9.00 до 15.00», «Неділя вихідний»; будні — у raw), адреса, телефон, Mask group (карта/фото `16:4017`), «Політика конфіденційності», «Публічний договір (офферта)», «Усі права захищені.», «PrometeyLabs» | `SiteSettings{schedule[],legal_links[]}` |

## 4. Mobile 393 (`16:4246`) — секції по порядку
1. Header + Hero — Frame 111 `16:4506` (лого, телефон, бургер TextAlignRight; H1; картки-напрямки; CTA)
2. Чому обирають — `16:4247` (картки в 1 колонку)
3. Послуги — `16:4278` (картки 1 колонка / компактні — див. Frame 99)
4. Новою поштою promo — `16:4373`
5. Як працює — `16:4382` / `16:4383` (кроки вертикально)
6. Відгуки — `16:4406` (слайдер)
7. Наші роботи — `16:4427`
8. FAQ — `16:4439`
9. Footer — `16:4483`
- Mobile menu (відкритий бургер) — `16:4791` 393×828: телефон, меню Головна/Послуги/Ціни/Про нас/**Відгуки**/Контакти, CTA «Записатись на діагностику», адреса. (На desktop пункту «Відгуки» нема — open question.)

## 5. Модалки
| modal | node | розмір | призначення | поля | CTA |
|---|---|---|---|---|---|
| 2 | `16:4177` | 669×538 desktop | «Записатись на сервіс» — форма заявки | Ваше ім'я (Profile), Номер телефону (Call), Оберіть потрібну послугу (select), close ✕ | кнопка відправки; «Або зв'яжіться з нами напряму» 068 806 83 16 |
| 3 | `16:4221` | 669×343 desktop | Success «Дякуємо за заявку!» | — | «На головну»; телефон |
| 4 | `16:4716` | 364×491 mobile | = modal 2 (mobile) | ті самі | ті самі |
| 5 | `16:4763` | 364×298 mobile | = modal 3 (mobile) | — | «На головну» |
Підкладка: `rgba(0,0,0,0.6)`. Тригери: всі CTA «Записатись…» (header, hero, картки послуг?). Submit → поки фронтовий стан modal 2→3 (бекенду немає).

## 6. Component 1 і Frame 99
- **Component 1** `16:4602` (404×416): компонент-картка послуги з варіантами `property1: "Frame 97" | "Frame 98"` (ймовірно default/hover або згорнута/розгорнута): фото, «Ремонт турбін», «Ціна від: 3 000 грн».
- **Frame 99** `16:4632` (365×828): набір 6 компактних мобільних карток послуг (DPF 3000, ГРМ 3500, Кондиціонер 1500, Маховик 4500, Пневмопідвіска рес. 4000 / демонт., Мех. обробка 800) — мобільний варіант картки з короткими лейблами «Рес. від:», «Демонт. від:».

## 7. Include-контракти (Django, без React)
```
templates/base.html                     <header> <main> <footer>, блок modals
partials/header.html        {% include "partials/header.html" with nav=nav settings=settings %}
partials/mobile_menu.html   nav, settings
sections/hero.html          hero, hero_cards, hero_badges
sections/advantages.html    advantages
sections/services.html      services  → loop {% include "components/service_card.html" with service=s %}
sections/mail_promo.html    promo
sections/mail_steps.html    steps
sections/reviews.html       reviews
sections/works.html         works
sections/faq.html           faq_items   (<details>/<summary> або button[aria-expanded])
partials/footer.html        settings, nav
modals/booking.html         id="modal-booking"  (modal 2/4), services для select
modals/success.html         id="modal-success"  (modal 3/5)
```
Landmarks: `header[role=banner]`, `nav[aria-label]`, `main`, кожна секція `section[aria-labelledby]` з id-якорем (#services, #prices, #about, #reviews, #contacts), `footer`, модалки `dialog`/`role="dialog" aria-modal`. Тригер модалки: `data-modal-open="booking"`.

## 8. Motion
У Figma прототипних анімацій не видно. Прийнятно: hover кнопок/карток, плавне відкриття FAQ, fade модалок, слайдер відгуків/робіт (стрілки Left2). Варіанти Component 1 → можливий hover-стан картки.

## 9. Асети (`assets/`, 97 файлів, ~74 MB)
Префікс = джерело: `desk-` (16:3628), `mob-` (16:4246), `m2-…m5-` (модалки), `c1-` (Component 1), `f99-` (Frame 99), `mhero-` (16:4791).
- Hero фото: `desk-telegram-cloud-photo-size25427027925866848633-y1.png` (мобайл `mob-…`)
- Hero картки: `desk-rectangle2/3/4.png`
- Лого: `desk-image1.png`, `mhero-image1.png`; footer mask: `desk-202610301009222.png` + `desk-202610301009221.svg`
- Фото послуг: `desk-image6…image18.png` (у порядку карток), Новою поштою: `desk-image19.png`; роботи: `desk-image15.png` (повторюється — плейсхолдер?)
- Іконки SVG (Hicon/Iconly): award1, setting, shield-tick(1), wallet, vector(✓ буллет), vector1 (pin), vector8, calling, calendar(1), arrow-right, ticket-expired, tick, left2 (стрілка слайдера), text-align-right (бургер), close, call, profile1, group1
- `raw/` — design_context кожної ноди для точних розмірів.
Асети — PNG 1x з Figma; для продакшну потрібна оптимізація (WebP/AVIF, srcset).

## 10. Open questions / неясно
1. Tablet відсутній — підтвердити BP 768–1023 і розкладку.
2. Шрифт Involve: ліцензія + woff2 файли (у Figma не експортуються).
3. Меню: «Ціни», «Про нас» — якорі чи окремі сторінки? «Відгуки» є лише в mobile меню.
4. Сторінки «Політика конфіденційності», «Публічний договір» — не намальовані.
5. Галерея «Наші роботи» використовує одне фото 3× — потрібні реальні фото.
6. Відгуки — один шаблонний («Максим»), опечатки в тексті («швідко», «виконалі»); джерело (Google reviews?).
7. Modal 2: список опцій select «Оберіть потрібну послугу» = список Service? Валідація/маска телефону, куди йде заявка (Telegram/email) — бекенд пізніше.
8. Component 1 варіанти Frame 97/98 — hover чи розкриття?
9. Ціни ГБЦ: 30 000 і 2 500 у різних картках — уточнити.
10. Графік будніх днів, карта в footer (embed Google Maps чи статичне зображення).
11. Hero картки-напрямки — куди ведуть (якорі на послуги?).
