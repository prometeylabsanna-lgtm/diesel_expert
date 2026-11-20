/**
 * Валідація форми запису: ім’я, послуга, UA-телефон (+380…, 13 символів).
 * Помилки мережі HTMX і стан кнопки на час запиту.
 */
(function () {
  "use strict";

  var NAME_RE = /^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'\u2019\u02BC\-\s]+$/;
  var LETTER_RE = /[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]/;
  var HAS_LETTER = /[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]/;
  var NET_ERROR = "Не вдалося надіслати. Перевірте зв’язок і спробуйте ще.";
  var CSRF_ERROR = "Сесія застаріла. Оновіть сторінку і спробуйте ще.";
  var PENDING_LABEL = "Надсилаємо…";

  if (window.htmx) {
    window.htmx.config.timeout = 15000;
  }

  function ensureError(fieldRoot) {
    var err = fieldRoot.querySelector(".field__error");
    if (!err) {
      err = document.createElement("p");
      err.className = "field__error";
      err.setAttribute("role", "alert");
      fieldRoot.appendChild(err);
    }
    return err;
  }

  function setError(input, message) {
    var root = input.closest(".modal__field");
    if (!root) return;
    var err = ensureError(root);
    err.textContent = message || "";
    err.hidden = !message;
    input.setAttribute("aria-invalid", message ? "true" : "false");
    root.classList.toggle("is-invalid", Boolean(message));
  }

  function statusNode(form) {
    var node = form.querySelector("[data-form-status]");
    if (!node) {
      node = document.createElement("p");
      node.className = "form__status";
      node.setAttribute("data-form-status", "");
      node.setAttribute("role", "alert");
      node.hidden = true;
      form.appendChild(node);
    }
    return node;
  }

  function setStatus(form, message) {
    var node = statusNode(form);
    node.textContent = message || "";
    node.hidden = !message;
  }

  function normalizeUaPhone(raw) {
    var digits = String(raw || "").replace(/\D/g, "");
    if (digits.indexOf("380") === 0 && digits.length === 12) return "+" + digits;
    if (digits.indexOf("80") === 0 && digits.length === 11) return "+3" + digits;
    if (digits.indexOf("0") === 0 && digits.length === 10) return "+38" + digits;
    return null;
  }

  function validateName(input) {
    var value = (input.value || "").trim();
    if (!value) {
      setError(input, "Вкажіть ім’я.");
      return false;
    }
    if (value.length < 2) {
      setError(input, "Вкажіть ім’я (мінімум 2 символи).");
      return false;
    }
    if (!NAME_RE.test(value) || !LETTER_RE.test(value) || /[0-9]/.test(value)) {
      setError(input, "Ім’я може містити лише літери, пробіл, дефіс або апостроф.");
      return false;
    }
    setError(input, "");
    return true;
  }

  function validatePhone(input) {
    var raw = (input.value || "").trim();
    if (!raw) {
      setError(input, "Вкажіть номер телефону.");
      return false;
    }
    if (HAS_LETTER.test(raw)) {
      setError(input, "У номері не можна вводити літери.");
      return false;
    }
    if (/[^0-9+\s\-()]/.test(raw)) {
      setError(input, "У номері дозволені лише цифри та +.");
      return false;
    }
    var phone = normalizeUaPhone(raw);
    if (!phone || phone.length !== 13) {
      setError(input, "Вкажіть український номер: +380XXXXXXXXX (13 символів).");
      return false;
    }
    setError(input, "");
    return true;
  }

  function validateService(select) {
    if (!select) return true;
    if (!select.value) {
      setError(select, "Оберіть послугу зі списку.");
      return false;
    }
    setError(select, "");
    return true;
  }

  function applyNormalizedPhone(input) {
    var phone = normalizeUaPhone(input.value);
    if (phone && phone !== input.value) input.value = phone;
  }

  function setPending(form, pending) {
    var btn = form.querySelector('button[type="submit"]');
    if (!btn) return;
    if (pending) {
      if (!btn.getAttribute("data-idle-label")) {
        btn.setAttribute("data-idle-label", (btn.textContent || "").trim());
      }
      btn.textContent = PENDING_LABEL;
      btn.setAttribute("aria-busy", "true");
      btn.disabled = true;
      return;
    }
    var idle = btn.getAttribute("data-idle-label");
    if (idle) btn.textContent = idle;
    btn.removeAttribute("aria-busy");
    btn.disabled = false;
  }

  function formOf(event) {
    var elt = event.detail && event.detail.elt;
    if (!elt || !elt.closest) return null;
    if (elt.matches && elt.matches("[data-booking-form]")) return elt;
    return elt.closest("[data-booking-form]");
  }

  function failMessage(event) {
    var xhr = event.detail && event.detail.xhr;
    if (xhr && xhr.status === 403) return CSRF_ERROR;
    return NET_ERROR;
  }

  function onRequestFail(event) {
    var form = formOf(event);
    if (!form) return;
    setPending(form, false);
    setStatus(form, failMessage(event));
  }

  function bindForm(form) {
    if (!form || form.getAttribute("data-booking-bound") === "1") return;
    form.setAttribute("data-booking-bound", "1");
    form.noValidate = true;

    var nameInput = form.querySelector('input[name="name"]');
    var phoneInput = form.querySelector('input[name="phone"]');
    var serviceSelect = form.querySelector('select[name="service"]');

    if (nameInput) {
      nameInput.setAttribute("pattern", "[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'\\u2019\\u02BC\\-\\s]{2,80}");
      nameInput.addEventListener("input", function () {
        var cleaned = nameInput.value.replace(/[^A-Za-zА-Яа-яЁёІіЇїЄєҐґ'\u2019\u02BC\-\s]/g, "");
        if (cleaned !== nameInput.value) nameInput.value = cleaned;
        if (nameInput.value.trim()) validateName(nameInput);
        else setError(nameInput, "");
      });
      nameInput.addEventListener("blur", function () {
        if (nameInput.value.trim()) validateName(nameInput);
      });
    }

    if (phoneInput) {
      phoneInput.setAttribute("inputmode", "tel");
      phoneInput.setAttribute("autocomplete", "tel");
      phoneInput.setAttribute("maxlength", "32");
      var syncPhone = function () {
        var cleaned = phoneInput.value.replace(/[^\d+\s\-()]/g, "");
        if (cleaned !== phoneInput.value) phoneInput.value = cleaned;
        applyNormalizedPhone(phoneInput);
        if (phoneInput.value.trim()) validatePhone(phoneInput);
        else setError(phoneInput, "");
      };
      phoneInput.addEventListener("input", syncPhone);
      phoneInput.addEventListener("blur", function () {
        applyNormalizedPhone(phoneInput);
        if (phoneInput.value.trim()) validatePhone(phoneInput);
      });
      phoneInput.addEventListener("paste", function () {
        window.setTimeout(syncPhone, 0);
      });
    }

    if (serviceSelect) {
      serviceSelect.addEventListener("change", function () {
        validateService(serviceSelect);
      });
    }

    form.addEventListener(
      "submit",
      function (event) {
        setStatus(form, "");
        var okName = nameInput ? validateName(nameInput) : true;
        var okPhone = phoneInput ? validatePhone(phoneInput) : true;
        var okService = serviceSelect ? validateService(serviceSelect) : true;
        if (!okName || !okPhone || !okService) {
          event.preventDefault();
          event.stopImmediatePropagation();
          var firstBad = form.querySelector(".modal__field.is-invalid .field__control");
          if (firstBad) firstBad.focus();
        }
      },
      true
    );
  }

  function scan() {
    document.querySelectorAll("[data-booking-form]").forEach(bindForm);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }

  document.body.addEventListener("htmx:afterSwap", scan);
  document.body.addEventListener("htmx:beforeRequest", function (event) {
    var form = formOf(event);
    if (!form) return;
    setStatus(form, "");
    setPending(form, true);
  });
  document.body.addEventListener("htmx:afterRequest", function (event) {
    var form = formOf(event);
    if (!form) return;
    var failed = event.detail && event.detail.successful === false;
    if (!failed) setPending(form, false);
  });
  document.body.addEventListener("htmx:sendError", onRequestFail);
  document.body.addEventListener("htmx:timeout", onRequestFail);
  document.body.addEventListener("htmx:responseError", onRequestFail);
})();
