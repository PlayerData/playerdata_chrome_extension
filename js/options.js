chrome.storage.sync.get(
  ["ghPat", "pdPat", "mergefreeze", "motivation"],
  function (result) {
    // Text option setters
    if (result.ghPat) {
      $("#gh-pat").val(result.ghPat);
    }
    if (result.pdPat) {
      $("#pd-pat").val(result.pdPat);
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
var quickLinksCnt = 0;

function setQuickLinksFields() {
  var quickLinks = [];
  const elements = document.getElementsByClassName("quick-url-field");
  for (var i = 0; i < elements.length; i++) {
    const inputs = elements[i].getElementsByTagName("input");
    quickLinks.push({
      name: inputs[0].value,
      url: inputs[1].value,
      order: elements[i].id.replace("quick-url-", ""),
    });
  }

  chrome.storage.sync.set({ quickLinks });
  document.getElementById("quick-links-success-message").style.display = "block";
  setTimeout(() => {
    document.getElementById("quick-links-success-message").style.display = "none";
  }, 5000)
}

function renderQuickLinkField(field) {
  return `<div id="quick-url-${field.order}" class="input-group mb-3 quick-url-field">
  <span class="input-group-text">name</span>
  <input type="text" class="form-control" value="${field.name}" aria-label="Username">
  <span class="input-group-text">url</span>
  <input type="text" class="form-control" value="${field.url}" aria-label="Server">
</div>`;
}

function renderQuickLinks() {
  chrome.storage.sync.get(["quickLinks"], (result) => {
    var quickUrlsHTML = "";
    for (var i = 0; i < result.quickLinks.length; i++) {
      quickUrlsHTML += renderQuickLinkField(result.quickLinks[i]);
      quickLinksCnt++;
    }
    document.getElementById("quick-urls").innerHTML = quickUrlsHTML;
  });
}
// Text option setters
document.addEventListener("DOMContentLoaded", function () {
  renderQuickLinks();
  $("#add-quick-url").click(function () {
    document.getElementById("quick-urls").innerHTML += renderQuickLinkField({
      name: "",
      url: "",
      order: quickLinksCnt,
    });
  });
  $("#save-quick-urls").click(function () {
    setQuickLinksFields();
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
