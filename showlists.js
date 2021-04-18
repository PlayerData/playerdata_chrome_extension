function create_a_mergefreeze_item(list_item, idx) {
  var url = `${list_item.url}?access_token=${list_item.token}`;
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", url, true);
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState == 4) {
      var result = JSON.parse(xhttp.responseText);
      const is_frozen = result.frozen;
      const badge_type = is_frozen ? "badge-danger" : "badge-success";
      const badge_text = is_frozen
        ? `Frozen (by ${result.frozen_by})`
        : "Unfrozen";
      var html = `<a class="list-group-item list-group-item-action" href="https://mergefreeze.com">${list_item.name} <span class="badge ${badge_type}">${badge_text}</span></a>`;
      document.getElementById("list-group-" + idx).innerHTML += html;
    }
  };
  xhttp.send();
}

function create_a_list_item(list_item, idx) {
  if (list_item.token) {
    create_a_mergefreeze_item(list_item, idx);
    return;
  }
  var html = `<a class="list-group-item list-group-item-action" href="${list_item.url}">${list_item.name}</a>`;
  document.getElementById("list-group-" + idx).innerHTML += html;
}

function create_new_row(current_row) {
  var new_id = `row-${current_row}`;
  var html = `<div id="${new_id}" class="row"></div>`;
  document.getElementById("lists").innerHTML += html;
  return new_id;
}

function create_a_list(list, idx, row_id) {
  var html = '<div class="col-sm">';
  html += `<h3>${list.title}</h3>`;
  html += `<div id="list-group-${idx}" class="list-group">`;
  html += "</div></div>";
  document.getElementById(row_id).innerHTML += html;

  for (var item_idx = 0; item_idx < list.links.length; item_idx++) {
    create_a_list_item(list.links[item_idx], idx);
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

document.addEventListener("DOMContentLoaded", function () {
  refresh_links();
});
