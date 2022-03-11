function create_a_mergefreeze_item(list_item, idx) {
  var url = `${list_item.url}?access_token=${list_item.token}`;
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", url, true);
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState == 4) {
      var result = JSON.parse(xhttp.responseText);
      const is_frozen = result.frozen;
      const badge_type = is_frozen ? "info" : "success";
      const badge_icon = is_frozen ? '<i class="bi bi-snow3 text-info" style="font-size: 1.5rem;"></i>' : '<i class="bi bi-check2 text-success" style="font-size: 2rem;"></i>';
      const badge_text = is_frozen
        ? `Frozen by ${result.frozen_by}`
        : "Unfrozen";
      var html = `
      <div class="col">
        <div class="card border-${badge_type} mb-3" style="max-width: 18rem;">
          <div class="card-header" style="display: flex; align-items: center; justify-content: space-between;">${list_item.name} <span>${badge_icon}</span></div>
          <div class="card-body text-${badge_type}">
            <p class="card-text">${badge_text}</p>
          </div>
        </div>
      </div>
      `
      // var html = `<a class="card" href="https://mergefreeze.com"> <span class="badge ${badge_type}"></span></a>`;
      document.getElementById("list-group-" + idx).innerHTML += html;
    }
  };
  xhttp.send();
}

function create_a_list_item(list_item, idx) {
  var html = `<a class="list-group-item list-group-item-action" href="${list_item.url}">${list_item.name}</a>`;
  document.getElementById("list-group-" + idx).innerHTML += html;
}

function create_new_row(current_row) {
  var new_id = `row-${current_row}`;
  var html = `<div id="${new_id}" class="row"></div>`;
  document.getElementById("lists").innerHTML += '<div class="container">' + html + '</div>';
  return new_id;
}

function create_a_list(list, idx, row_id) {
  var html = '<div class="col-md mt-2 card-padding">';
  html += `<h3>${list.title}</h3>`;
  html += `<div id="list-group-${idx}" class="row p-2">`;
  html += "</div></div>";
  document.getElementById(row_id).innerHTML += html;

  for (var item_idx = 0; item_idx < list.links.length; item_idx++) {
    if (list.links[item_idx].type === "MERGE") {
      create_a_mergefreeze_item(list.links[item_idx], idx);
    } else {
      create_a_list_item(list.links[item_idx], idx);
    }
  }
}

function refresh_links() {
  document.getElementById("lists").innerHTML = "";
  current_row = 0;
  for (var idx = 0; idx < pdlists.length; idx++) {
    var the_list = pdlists[idx];
    var row_id = "row-" + current_row;
    if (the_list.row != current_row) {
      row_id = create_new_row(the_list.row);
      current_row = the_list.row;
    }
    create_a_list(the_list, idx, row_id);
  }
}
function search_kb() {
  var search_term = $("#gh_search").val();
  chrome.tabs.create({
    url: "https://github.com/PlayerData/KB/search?q=" + search_term,
  });
}

document.addEventListener("DOMContentLoaded", function () {
  $("#gh_search").keyup(function (e) {
    if (e.keyCode == 13) {
      search_kb();
    }
  });
  refresh_links();
});
