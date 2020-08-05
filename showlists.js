var is_popup = false;

function create_new_row(current_row) {
  var html = "";
  if (current_row > 0) {
    html += "</div>";
  }
  html += '<div class="row">';
  return html;
}

function create_a_list_item(list_item) {
  var html = "";
  if (is_popup) {
    html +=
      '<a target="_blank" class="list-group-item list-group-item-action" href="' +
      list_item.url +
      '">' +
      list_item.name +
      "</a>";
  } else {
    html +=
      '<a class="list-group-item list-group-item-action" href="' +
      list_item.url +
      '">' +
      list_item.name +
      "</a>";
  }
  return html;
}

function create_a_list(list) {
  var html = "";
  html += '<div class="col-sm">';
  html += "<h3>" + list.title + "</h3>";
  html += '<div class="list-group">';
  for (var item_idx = 0; item_idx < list.links.length; item_idx++) {
    html += create_a_list_item(list.links[item_idx]);
  }
  html += "</div></div>";
  return html;
}

function addJenkinsLink() {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
    let url = tabs[0].url;
    // https://ci.playerdata.co.uk/blue/organizations/jenkins/PlayerData%20GitHub%2Fapp/detail/PR-1337/7/pipeline
    //https://ci.playerdata.co.uk/job/PlayerData%20GitHub/job/app/view/change-requests/job/PR-1337/7/
    let oldUiUrl = url.replace("blue/organizations/jenkins", "job");
    oldUiUrl = oldUiUrl.replace(
      "PlayerData%20GitHub%2Fapp/detail",
      "PlayerData%20GitHub/job/app/view/change-requests/job"
    );
    oldUiUrl = oldUiUrl.replace("/pipeline", "/");
    const list = {
        "title": "Jenkins",
        "row": 1,
        "links": [
            { "name": "Open in old", "url": oldUiUrl },
        ]
    };
    is_popup = true;
    document.getElementById('pulists').innerHTML += create_a_list(list);
    is_popup = false;
  });
}

function refreshLinks() {
  document.getElementById("lists").innerHTML = "";
  document.getElementById("pulists").innerHTML = "";
  addJenkinsLink();
  var html = "";
  var puhtml = "";
  current_row = 0;
  for (var idx = 0; idx < pdlists.length; idx++) {
    var the_list = pdlists[idx];
    if (the_list.row != current_row) {
      html += create_new_row(current_row);
      current_row++;
    }
    html += create_a_list(the_list);
    is_popup = true;
    puhtml += create_a_list(the_list);
    is_popup = false;
  }
  // Add the final div to finish the `row` div
  document.getElementById("lists").innerHTML += html + "</div>";
  document.getElementById("pulists").innerHTML += puhtml;
}

document.addEventListener("DOMContentLoaded", function () {
  refreshLinks();
});
