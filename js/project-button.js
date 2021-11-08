var btn = document.createElement("a");
btn.innerHTML = "Projects";
btn.href = "https://github.com/orgs/PlayerData/projects/";
btn.classList=["ButtonBase-sc-181ps9o-0 Button-xjtz72-0 hcJZfK dTPxBq"];
btn.style="max-width: 250px"

var project_root = document.getElementById("memex-project-view-root");

project_root.prepend(btn);
