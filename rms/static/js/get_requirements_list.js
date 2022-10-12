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
            get_requirement(requirement_select.value);
            document.getElementById('project_id').value = project_id
            document.getElementById('requirement_id').value = requirement_select.value
        });
    });

    fetch('/requirements/requirement_doc/' + project_id).then(function(response) {
        response.json().then(function(data) {
            let requirement_doc = document.getElementById('requirement_doc');
            let doc_HTML = data.requirement_doc != '' ? data.requirement_doc : '';
            requirement_doc.innerHTML = doc_HTML;
        });
    });

});

requirement_select.addEventListener("change", function() {
    requirement_id = requirement_select.value;
    get_requirement(requirement_id)
    document.getElementById('requirement_id').value = requirement_id

})

function get_requirement(requirement_id) {
    if (requirement_id) {
    fetch('/requirements/get_requirement/' + requirement_id).then(function(response) {
        response.json().then(function(data) {
            document.getElementById('id').value = data.requirement.id
            document.getElementById('name').value = data.requirement.name
            document.getElementById('description').innerHTML = data.requirement.description
            document.getElementById('status').value = data.requirement.status_id
            document.getElementById('tags').value = data.requirement.tags
            document.getElementById('priority').value = data.requirement.priority_id
            document.getElementById('type').value = data.requirement.type_id
        });
    });
    }
    else {
        new_requirement()
    }
}

function new_requirement(){
    document.getElementById('id').value = null
    document.getElementById('name').value = null
    document.getElementById('description').innerHTML = ''
    document.getElementById('status').value = null
    document.getElementById('tags').value = null
    document.getElementById('priority').value = null
    document.getElementById('type').value = null
}