const STORAGE_KEY = "de_cookie_consent";
const CHOICES = new Set(["accepted", "declined"]);
const FAIL_TEXT = "Не вдалося зберегти вибір. Спробуйте ще.";

function remember(choice) {
  try {
    localStorage.setItem(STORAGE_KEY, choice);
  } catch (error) {
    /* приватний режим Safari */
  }
}

const banner = document.getElementById("cookie-banner");
if (banner) {
  const form = banner.querySelector("[data-cookie-form]");
  const errorNode = banner.querySelector("[data-cookie-error]");

  window.addEventListener("storage", (event) => {
    if (event.key !== STORAGE_KEY || !CHOICES.has(event.newValue)) return;
    banner.hidden = true;
  });

  if (form) {
    let picked = "";
    form.querySelectorAll('button[name="choice"]').forEach((button) => {
      button.addEventListener("click", () => {
        picked = button.value;
      });
    });

    const setBusy = (busy) => {
      form.querySelectorAll("button").forEach((button) => {
        button.disabled = busy;
      });
    };

    const showError = (message) => {
      if (!errorNode) return;
      errorNode.textContent = message || "";
      errorNode.hidden = !message;
    };

    form.addEventListener("submit", (event) => {
      const submitter = event.submitter;
      const choice = picked || (submitter && submitter.value) || "";
      if (!CHOICES.has(choice)) return;
      event.preventDefault();
      showError("");
      setBusy(true);
      const data = new FormData(form);
      data.set("choice", choice);
      fetch(form.action, {
        method: "POST",
        body: data,
        credentials: "same-origin",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((response) => {
          if (!response.ok) throw new Error("cookie");
          remember(choice);
          banner.hidden = true;
        })
        .catch(() => {
          setBusy(false);
          showError(FAIL_TEXT);
        });
    });
  }
}
