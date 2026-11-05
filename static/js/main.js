const body = document.body;

const menu = document.getElementById("mobile-menu");
const burger = document.querySelector("[data-menu-toggle]");

function anyOverlayOpen() {
  const modalOpen = document.querySelector(".modal:not([hidden])");
  const menuOpen = menu && !menu.hidden;
  return Boolean(modalOpen || menuOpen);
}

function syncLock() {
  body.classList.toggle("is-locked", anyOverlayOpen());
}

function closeMenu() {
  if (!menu || !burger) return;
  menu.hidden = true;
  burger.setAttribute("aria-expanded", "false");
  syncLock();
}

function openMenu() {
  if (!menu || !burger) return;
  menu.hidden = false;
  burger.setAttribute("aria-expanded", "true");
  syncLock();
}

if (burger && menu) {
  burger.addEventListener("click", () => {
    if (menu.hidden) openMenu();
    else closeMenu();
  });
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });
}

let lastFocus = null;

function openModal(name) {
  const modal = document.getElementById(`modal-${name}`);
  if (!modal) return;
  document.querySelectorAll(".modal").forEach((item) => {
    item.hidden = true;
  });
  closeMenu();
  lastFocus = document.activeElement;
  modal.hidden = false;
  syncLock();
  const focusTarget = modal.querySelector("input, select, button, a");
  if (focusTarget) focusTarget.focus();
}

function closeModal(modal) {
  modal.hidden = true;
  syncLock();
  if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
}

document.querySelectorAll("[data-modal-open]").forEach((trigger) => {
  trigger.addEventListener("click", () => {
    openModal(trigger.getAttribute("data-modal-open"));
  });
});

document.querySelectorAll("[data-modal-close]").forEach((trigger) => {
  trigger.addEventListener("click", () => {
    const modal = trigger.closest(".modal");
    if (modal) closeModal(modal);
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  const modal = document.querySelector(".modal:not([hidden])");
  if (modal) {
    closeModal(modal);
    return;
  }
  closeMenu();
});

const bookingForm = document.querySelector("[data-booking-form]");
if (bookingForm) {
  bookingForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const booking = document.getElementById("modal-booking");
    if (booking) booking.hidden = true;
    openModal("success");
    bookingForm.reset();
  });
}

document.querySelectorAll(".faq__question").forEach((button) => {
  button.addEventListener("click", () => {
    const item = button.closest(".faq__item");
    const willOpen = button.getAttribute("aria-expanded") !== "true";
    document.querySelectorAll(".faq__item").forEach((other) => {
      const question = other.querySelector(".faq__question");
      const answer = other.querySelector(".faq__answer");
      const open = other === item && willOpen;
      other.classList.toggle("is-open", open);
      question.setAttribute("aria-expanded", open ? "true" : "false");
      answer.hidden = !open;
    });
  });
});

document.querySelectorAll(".service-card__toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const card = button.closest(".service-card");
    const open = !card.classList.contains("is-open");
    card.classList.toggle("is-open", open);
    button.setAttribute("aria-expanded", open ? "true" : "false");
  });
});

const servicesRoot = document.querySelector(".services");
const moreButton = document.querySelector("[data-services-more]");
if (servicesRoot && moreButton) {
  moreButton.addEventListener("click", () => {
    servicesRoot.classList.add("is-expanded");
    moreButton.setAttribute("aria-expanded", "true");
    moreButton.hidden = true;
  });
}

document.querySelectorAll("[data-slider]").forEach((root) => {
  const viewport = root.querySelector("[data-slider-viewport]");
  const track = root.querySelector(".slider__track");
  const prev = root.querySelector("[data-slider-prev]");
  const next = root.querySelector("[data-slider-next]");
  if (!viewport || !track || !prev || !next) return;

  const step = () => {
    const slide = track.querySelector(".slider__slide");
    if (!slide) return viewport.clientWidth;
    const styles = getComputedStyle(track);
    const gap = parseFloat(styles.columnGap || styles.gap) || 0;
    return slide.getBoundingClientRect().width + gap;
  };

  const move = (direction) => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    viewport.scrollBy({
      left: direction * step(),
      behavior: reduce ? "auto" : "smooth",
    });
  };

  prev.addEventListener("click", () => move(-1));
  next.addEventListener("click", () => move(1));
});
