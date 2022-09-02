chrome.storage.sync.get(
  ["ghPat", "pdPat", "quickLinks", "mergefreeze", "motivation"],
  function (result) {
    // Text option setters
    if (result.ghPat) {
      $("#gh-pat").val(result.ghPat);
    }
    if (result.pdPat) {
      $("#pd-pat").val(result.pdPat);
    }
    if (result.quickLinks) {
      $("#quick-urls").val(result.quickLinks);
    }

    // Toggle options setters
    if (result.mergefreeze)
      document
        .getElementById("toggle-mergefreeze")
        .setAttribute("checked", "checked");
    if (result.motivation)
      document
        .getElementById("toggle-motivation")
        .setAttribute("checked", "checked");
  }
);

// Text option setters
document.addEventListener("DOMContentLoaded", function () {
  $("#quick-urls").keyup(function (e) {
    chrome.storage.sync.set({ quickLinks: e.target.value });
  });
  $("#gh-pat").keyup(function (e) {
    chrome.storage.sync.set({ ghPat: e.target.value });
  });
  $("#pd-pat").keyup(function (e) {
    chrome.storage.sync.set({ pdPat: e.target.value });
  });
});

// Toggle options setters
document.getElementById("toggle-mergefreeze").addEventListener("input", (e) => {
  chrome.storage.sync.set({ mergefreeze: e.target.checked });
});
document.getElementById("toggle-motivation").addEventListener("input", (e) => {
  chrome.storage.sync.set({ motivation: e.target.checked });
});
