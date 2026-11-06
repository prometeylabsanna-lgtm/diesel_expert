/**
 * Валідація форми запису: ім’я без спецсимволів, UA-телефон (+380…, 13 символів).
 */
(function () {
  "use strict";

  var NAME_RE = /^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'\u2019\u02BC\-\s]+$/;
  var LETTER_RE = /[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]/;
  var HAS_LETTER = /[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]/;

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

  function bindForm(form) {
    if (!form || form.getAttribute("data-booking-bound") === "1") return;
    form.setAttribute("data-booking-bound", "1");

    var nameInput = form.querySelector('input[name="name"]');
    var phoneInput = form.querySelector('input[name="phone"]');

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
      phoneInput.setAttribute("maxlength", "17");
      phoneInput.addEventListener("input", function () {
        var cleaned = phoneInput.value.replace(/[^\d+\s\-()]/g, "");
        if (cleaned !== phoneInput.value) phoneInput.value = cleaned;
        if (phoneInput.value.trim()) validatePhone(phoneInput);
        else setError(phoneInput, "");
      });
      phoneInput.addEventListener("blur", function () {
        if (phoneInput.value.trim()) validatePhone(phoneInput);
      });
    }

    form.addEventListener(
      "submit",
      function (event) {
        var okName = nameInput ? validateName(nameInput) : true;
        var okPhone = phoneInput ? validatePhone(phoneInput) : true;
        if (!okName || !okPhone) {
          event.preventDefault();
          event.stopImmediatePropagation();
          var firstBad = form.querySelector('.modal__field.is-invalid .field__control');
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
})();
