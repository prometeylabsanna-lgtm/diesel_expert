(function () {
  function bindColor(input) {
    if (input.dataset.cmsColorBound) return;
    input.dataset.cmsColorBound = "1";
    var hex = input.parentElement && input.parentElement.querySelector("[data-cms-color-hex]");
    input.addEventListener("input", function () {
      if (hex) hex.textContent = input.value;
    });
    var reset = input.parentElement && input.parentElement.querySelector("[data-cms-color-reset]");
    if (!reset || reset.dataset.cmsColorResetBound) return;
    reset.dataset.cmsColorResetBound = "1";
    reset.addEventListener("click", function () {
      var fallback = input.getAttribute("data-cms-color-default") || "";
      if (!fallback) return;
      input.value = fallback;
      if (hex) hex.textContent = fallback;
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    });
  }

  function bindAll(root) {
    (root || document).querySelectorAll("[data-cms-color]").forEach(bindColor);
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindAll(document);
  });
})();
