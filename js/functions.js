async function getCurrentTab() {
  let queryOptions = { active: true, currentWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

async function search_kb(input_id, new_tab = false) {
  var search_term = $("#" + input_id).val();
  var tab = await getCurrentTab();

  if (new_tab && tab.url !== "chrome://newtab/") {
    chrome.tabs.create({
      url: "https://github.com/search?q=org%3APlayerData+" + search_term,
    });
  } else {
    chrome.tabs.update({
      url: "https://github.com/search?q=org%3APlayerData+" + search_term,
    });
  }
}
