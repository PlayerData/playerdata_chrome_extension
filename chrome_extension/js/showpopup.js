document.addEventListener("DOMContentLoaded", function () {
  $("#gh_button").click(function() {
    var search_term = $("#gh_search").val();
    chrome.tabs.create({url:'https://github.com/search?q=org%3APlayerData+' + search_term});
  });
});
