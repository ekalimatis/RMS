let project_select = document.getElementById('project');
let requirement_select = document.getElementById('requirement');

project_select.addEventListener("change", function() {
    project_id = project_select.value;

    fetch('/requirements/project/' + project_id).then(function(response) {
        response.json().then(function(data) {
            let optionHTML = '';

            for (let requirement of data.requirements) {
                optionHTML += '<option value="' + requirement.id + '">' + requirement.name + '</option>';
            }

            requirement_select.innerHTML = optionHTML;
        });
    });
})