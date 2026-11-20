const body = document.body;

const menu = document.getElementById("mobile-menu");
const burger = document.querySelector("[data-menu-toggle]");

function anyOverlayOpen() {
  const modalOpen = document.querySelector(".modal:not([hidden])");
  const menuOpen = menu && !menu.hidden;
  return Boolean(modalOpen || menuOpen);
}

let menuReturnFocus = null;
let lockScrollY = 0;

function rememberScroll() {
  if (body.style.top) return;
  lockScrollY = window.scrollY || document.documentElement.scrollTop || 0;
  body.style.top = `-${lockScrollY}px`;
}

function releaseScroll() {
  const top = body.style.top;
  body.style.top = "";
  if (!top) return;
  const y = Math.abs(parseInt(top, 10));
  window.scrollTo(0, Number.isNaN(y) ? lockScrollY : y);
}

function syncLock() {
  const lock = anyOverlayOpen();
  if (lock) {
    rememberScroll();
    body.classList.add("is-locked");
    return;
  }
  body.classList.remove("is-locked");
  releaseScroll();
}

function closeMenu(options) {
  if (!menu || menu.hidden) return;
  menu.hidden = true;
  body.classList.remove("is-menu-open");
  document.querySelectorAll("[data-menu-toggle]").forEach((btn) => {
    btn.setAttribute("aria-expanded", "false");
  });
  if (!options || !options.keepLock) syncLock();
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
  closeMenu({ keepLock: true });
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
    if (select && opener.hasAttribute("data-service")) {
      select.value = opener.getAttribute("data-service") || "";
    }
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
  const booking = document.getElementById("modal-booking");
  if (booking) booking.hidden = true;
  openModal("success");
});

function trapTab(event, panel) {
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
}

document.addEventListener("keydown", (event) => {
  const modal = document.querySelector(".modal:not([hidden])");
  if (event.key === "Tab") {
    if (modal) {
      trapTab(event, modal.querySelector(".modal__panel") || modal);
      return;
    }
    if (menu && !menu.hidden) {
      const panel = menu.querySelector(".mobile-menu__panel") || menu;
      trapTab(event, panel);
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

if (menu) {
  menu.addEventListener("click", (event) => {
    if (event.target === menu) closeMenu();
  });
}

const desktopNav = window.matchMedia("(min-width: 1280px)");
const closeMenuOnDesktop = () => {
  if (desktopNav.matches) closeMenu();
};
if (typeof desktopNav.addEventListener === "function") {
  desktopNav.addEventListener("change", closeMenuOnDesktop);
} else if (typeof desktopNav.addListener === "function") {
  desktopNav.addListener(closeMenuOnDesktop);
}

if (body.classList.contains("is-locked")) rememberScroll();

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
