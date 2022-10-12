let project_select = document.getElementById('project');
let requirement_select = document.getElementById('requirement');

project_select.addEventListener("change", function() {
    project_id = project_select.value;

    fetch('/requirements/requirement_list/' + project_id).then(function(response) {
        response.json().then(function(data) {
            let optionHTML = '';

            for (let requirement of data.requirements) {
                optionHTML += '<option value="' + requirement.id + '">' + requirement.name + '</option>';
            }

            requirement_select.innerHTML = optionHTML;
        });
    });
        fetch('/requirements/requirement_doc/' + project_id).then(function(response) {
        response.json().then(function(data) {
            let requirement_doc = document.getElementById('requirement_doc');
            let doc_HTML = data.requirement_doc != '' ? data.requirement_doc : '';
            console.log(requirement_doc)
            requirement_doc.innerHTML = doc_HTML;
        });
    });
})

requirement_select.addEventListener("change", function() {
    requirement_id = requirement_select.value;
    fetch('/requirements/get_requirement/' + requirement_id).then(function(response) {
        response.json().then(function(data) {
            console.log(data.requirement.id);
            document.getElementById('id').value = data.requirement.id
            document.getElementById('name').value = data.requirement.name
            document.getElementById('description').innerHTML = data.requirement.description
            document.getElementById('status').value = data.requirement.status_id
            document.getElementById('tags').value = data.requirement.tags
            document.getElementById('priority').value = data.requirement.priority_id
            document.getElementById('type').value = data.requirement.type_id
        });
    });
})