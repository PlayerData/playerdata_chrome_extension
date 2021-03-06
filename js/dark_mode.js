const toggle = document.getElementById('toggle');
const body = document.body;

chrome.storage.sync.get(['darkMode'], function(result) {
  if (result.darkMode) {
    body.classList.add('dark-theme');
    if (toggle) toggle.setAttribute('checked', 'checked');
  }
});

if (toggle) toggle.addEventListener('input', e => {
    chrome.storage.sync.set({ darkMode: e.target.checked })

    chrome.storage.sync.get(['darkMode'], function(data) {
      data.darkMode ? body.classList.add('dark-theme') : body.classList.remove('dark-theme');

      chrome.tabs.query({windowType:'normal'}, function(tabs) {
        tabs.forEach((tab) => {
          if (tab.url === 'chrome://newtab/') {
            chrome.tabs.reload(tab.id);
          }
        })
      }); 
    });
});
