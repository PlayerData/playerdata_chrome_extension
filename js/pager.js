
function get_incidents() {
    var url = "https://api.pagerduty.com/incidents?total=false&time_zone=UTC&statuses%5B%5D=triggered";
    var xhttp = new XMLHttpRequest();
    xhttp.withCredentials = true;
    xhttp.open("GET", url, true);
    xhttp.onreadystatechange = function () {
      if (xhttp.readyState == 4) {
        var result = JSON.parse(xhttp.responseText);
        for(var i = 0; i <  result.incidents.length; i++) {
            var incident = result.incidents[i];
            console.log(incident);
            var new_incident_link = '<div class="row" style="padding: 10px">';
            new_incident_link += `<a style="font-size: 50px" href="${incident.html_url}"><span class="badge badge-danger">${incident.title}</span></a>`
            new_incident_link += '</div>';
            document.getElementById("pager").innerHTML += new_incident_link;
        }
      }
    };
    xhttp.setRequestHeader("accept", "application/vnd.pagerduty+json;version=2");
    xhttp.setRequestHeader("content-type", "application/json");
    xhttp.setRequestHeader("authorization", "Token token=" + pager_duty_key);
    xhttp.send();

}


document.addEventListener("DOMContentLoaded", function () {
    if(pager_duty_key) {
        get_incidents();
    }
  });