var project_items = [
    { "name": "EdgeV2", "url": "https://github.com/orgs/PlayerData/projects/11" },
    { "name": "Real-Time Edge Data (WiFi)", "url": "https://github.com/orgs/PlayerData/projects/10" },
    { "name": "Freedom Board", "url": "https://github.com/orgs/PlayerData/projects/8" }
];

function getProjectLine(is_popup, item) {
    var html = '<a class="list-group-item list-group-item-action"';
    if (is_popup) {
        html += ' target="_blank" ';
    }  
    html += 'href="' + item.url + '">' + item.name + '</a>';
    return html
}
function refreshProjects() {
    // Get the list
    document.getElementById("list").innerHTML = "";
    var html = '';
    var popuphtml = '';
    for (var idx = 0; idx < project_items.length; idx++) {
        html += getProjectLine(false, project_items[idx]);
        popuphtml += getProjectLine(true, project_items[idx]);
    }
    document.getElementById("list").innerHTML += html;
    document.getElementById("popupList").innerHTML += popuphtml
}

document.addEventListener('DOMContentLoaded', function () {
    refreshProjects();
});