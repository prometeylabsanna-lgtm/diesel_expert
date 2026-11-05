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

let menuReturnFocus = null;

function closeMenu() {
  if (!menu || menu.hidden) return;
  menu.hidden = true;
  body.classList.remove("is-menu-open");
  document.querySelectorAll("[data-menu-toggle]").forEach((btn) => {
    btn.setAttribute("aria-expanded", "false");
  });
  syncLock();
  const back = menuReturnFocus;
  menuReturnFocus = null;
  if (back && typeof back.focus === "function" && document.contains(back)) back.focus();
}

function openMenu() {
  if (!menu) return;
  const opener = document.activeElement;
  menuReturnFocus = opener && opener !== document.body ? opener : document.querySelector(".header__burger");
  menu.hidden = false;
  body.classList.add("is-menu-open");
  document.querySelectorAll("[data-menu-toggle]").forEach((btn) => {
    btn.setAttribute("aria-expanded", "true");
  });
  syncLock();
  const panel = menu.querySelector(".mobile-menu__panel") || menu;
  const focusTarget = getFocusable(panel)[0] || panel.querySelector("a[href], button:not([disabled])");
  if (focusTarget) focusTarget.focus();
}

document.querySelectorAll("[data-menu-toggle]").forEach((btn) => {
  btn.addEventListener("click", () => {
    if (menu.hidden) openMenu();
    else closeMenu();
  });
});
if (menu) {
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });
}

let lastFocus = null;

function getFocusable(container) {
  return Array.from(
    container.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    )
  ).filter((el) => {
    if (el.hasAttribute("disabled") || el.tabIndex < 0) return false;
    if (el.closest("[aria-hidden='true']")) return false;
    return el.offsetParent !== null;
  });
}

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
  const panel = modal.querySelector(".modal__panel") || modal;
  requestAnimationFrame(() => {
    const focusTarget = getFocusable(panel)[0];
    if (focusTarget) focusTarget.focus();
  });
}

function closeModal(modal) {
  modal.hidden = true;
  syncLock();
  if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
}

document.addEventListener("click", (event) => {
  const opener = event.target.closest("[data-modal-open]");
  if (opener) {
    openModal(opener.getAttribute("data-modal-open"));
    const select = document.querySelector('#modal-booking select[name="service"]');
    if (select) select.value = opener.getAttribute("data-service") || "";
    return;
  }
  const closer = event.target.closest("[data-modal-close]");
  if (!closer) return;
  const modal = closer.closest(".modal");
  if (modal) closeModal(modal);
});

document.body.addEventListener("lead-ok", () => {
  const form = document.querySelector("[data-booking-form]");
  if (form) form.reset();
  const thanks = document.body.getAttribute("data-thanks-url");
  if (thanks && window.location.pathname !== thanks) {
    window.history.pushState({ thanks: true }, "", thanks);
  }
  const booking = document.getElementById("modal-booking");
  if (booking) booking.hidden = true;
  openModal("success");
});

document.addEventListener("keydown", (event) => {
  const modal = document.querySelector(".modal:not([hidden])");
  if (modal && event.key === "Tab") {
    const panel = modal.querySelector(".modal__panel") || modal;
    const focusable = getFocusable(panel);
    if (!focusable.length) {
      event.preventDefault();
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    } else if (!panel.contains(document.activeElement)) {
      event.preventDefault();
      first.focus();
    }
    return;
  }
  if (event.key !== "Escape") return;
  if (modal) {
    closeModal(modal);
    return;
  }
  closeMenu();
});

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
