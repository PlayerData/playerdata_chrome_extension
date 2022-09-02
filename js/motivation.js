function get_quotes() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "https://zenquotes.io/api/today", true);
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState == 4) {
      var result = JSON.parse(xhttp.responseText);
      set_quotes(result);
      render_quote(result);
    }
  };
  xhttp.setRequestHeader("content-type", "application/json");
  xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
  xhttp.send();
}

function set_quotes(data) {
  chrome.storage.sync.set({
    quotes: {
      data: data,
      timestamp: new Date().setHours(0, 0, 0, 0),
    },
  });
}

function render_quote(data) {
  var quote = data[Math.floor(Math.random() * data.length)];
  document.getElementById("motivation").innerHTML = quote.h;
  document.getElementById("motivation").hidden = false;
}

document.addEventListener("DOMContentLoaded", function () {
  enabled = chrome.storage.sync.get(
    ["motivation", "quotes"],
    function (result) {
      if (result.motivation) {
        if (!result.quotes) {
          return get_quotes();
        }

        if (
          result.quotes.data.length >= 1 &&
          result.quotes.timestamp == new Date().setHours(0, 0, 0, 0)
        ) {
          render_quote(result.quotes.data);
        } else {
          get_quotes();
        }
      }
    }
  );
});
