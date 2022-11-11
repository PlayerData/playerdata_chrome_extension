chrome.storage.sync.get(["quickLinks"], function (result) {
  var linksHTML = "";
  if (result.quickLinks) {
    for (var i = 0; i < result.quickLinks.length; i++) {
      linksHTML += `<a target="_blank" class="list-group-item list-group-item-action"
                href="${result.quickLinks[i].url}">${result.quickLinks[i].name}</a>`;
    }
  }
  document.getElementById("quick-links").innerHTML = linksHTML;
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
