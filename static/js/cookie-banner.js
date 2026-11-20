const STORAGE_KEY = "de_cookie_consent";
const COOKIE_NAME = "cookie_consent";
const MAX_AGE = 60 * 60 * 24 * 365;
const CHOICES = new Set(["accepted", "declined"]);

function readStored() {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    if (CHOICES.has(value)) return value;
  } catch (error) {
    return "";
  }
  return "";
}

function persist(choice) {
  try {
    localStorage.setItem(STORAGE_KEY, choice);
  } catch (error) {
    /* приватний режим Safari */
  }
  const secure = window.location.protocol === "https:" ? "; Secure" : "";
  document.cookie =
    COOKIE_NAME + "=" + choice + "; Path=/; Max-Age=" + MAX_AGE + "; SameSite=Lax" + secure;
}

const banner = document.getElementById("cookie-banner");
if (banner) {
  if (readStored()) banner.hidden = true;

  const form = banner.querySelector("[data-cookie-form]");
  if (form) {
    let picked = "";
    form.querySelectorAll('button[name="choice"]').forEach((button) => {
      button.addEventListener("click", () => {
        picked = button.value;
      });
    });

    form.addEventListener("submit", (event) => {
      const submitter = event.submitter;
      const choice = picked || (submitter && submitter.value) || "";
      if (!CHOICES.has(choice)) return;
      event.preventDefault();
      persist(choice);
      banner.hidden = true;
      const data = new FormData(form);
      data.set("choice", choice);
      fetch(form.action, {
        method: "POST",
        body: data,
        credentials: "same-origin",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      }).catch(() => {});
    });
  }
}
