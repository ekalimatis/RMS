let project_select = document.getElementById('project');
let requirement_select = document.getElementById('requirement');
let requirement_doc = document.getElementById('requirement_doc');

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

            let doc_HTML = data.requirement_doc != '' ? data.requirement_doc : '';

            requirement_doc.innerHTML = doc_HTML;
        });
    });
})