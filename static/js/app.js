function nav_control() {
    var element = document.getElementById("nav-menu");
    element.classList.toggle("nav-open");

    var element = document.getElementById("open");
    element.classList.toggle("open");

    var main = document.getElementById("main")
    main.classList.toggle("main-full")

    var top_p = document.getElementById("top")
    top_p.classList.toggle("opacity-1")
    
    var top_p = document.getElementById("nav2")
    top_p.classList.toggle("opacity-1")
    
}
function project_nav() {
    var element = document.getElementById("projects");
    element.classList.toggle("show");
    var element = document.getElementById("project-icon");
    element.classList.toggle("show");

}

function dept_modal(dept) {
    var element = document.getElementById(dept);
    console.log(element)
    element.classList.toggle("modal-show");
}

function pfp_modal() {
    var element = document.getElementById("user-modal");
    element.classList.toggle("show");
}
function add_user_modal() {
    var element = document.getElementById("add-user");
    element.classList.toggle("modal-show");
}
function edit_modal(dept) {
    var element = document.getElementById(dept);
    console.log(dept)
    console.log(element)
    element.classList.toggle("modal-show");
}

function edit_project_modal() {
    const element = document.getElementById("add-proj-modal");
    console.log(element)
    element.classList.toggle("modal-show");
}
function update_project_modal(id) {
    const element = document.getElementById(id);
    console.log(element)
    element.classList.toggle("modal-show");
}
function trash_project_modal(id) {
    const element = document.getElementById(id);
    console.log(element)
    element.classList.toggle("modal-show");
}
function add_task_modal(id) {
    const element = document.getElementById(id);
    console.log(element)
    element.classList.toggle("modal-show");
}
function add_dept_modal() {
    const element = document.getElementById("add_dept");
    console.log(element)
    element.classList.toggle("modal-show");
}

function settings_modal() {
    const element = document.getElementById("settings");
    console.log(element)
    element.classList.toggle("modal-show");
}
function global_notif_modal() {
    const element = document.getElementById("global-notif");
    console.log(element)
    element.classList.toggle("modal-show");
}
function man_notif_modal() {
    const element = document.getElementById("man-notif");
    console.log(element)
    element.classList.toggle("modal-show");
}




function hide_modal(obs) {

    obs.classList.toggle("hide");
}
// document.getElementById("imageid").src="../template/save.png";
$(document).ready(function() {
    // Initialize Select2 for the static multi-select dropdown
    $('#myMultiSelect').select2({
        placeholder: 'Select options',
        allowClear: true
    });
});

