chrome.storage.sync.get(["quickLinks"], function (result) {
  if (result.quickLinks) {
  }
});

document.addEventListener("DOMContentLoaded", function () {
  $('[data-toggle="popover"]').popover();
  $("#gh_search_popup").keyup(function (e) {
    if (e.keyCode == 13) {
      search_kb("gh_search_popup", true);
    }
  });

  $("#settings-button").click(function () {
    if (chrome.runtime.openOptionsPage) {
      chrome.runtime.openOptionsPage();
    } else {
      window.open(chrome.runtime.getURL("options.html"));
    }
  });
});
