document.getElementById('Accept').addEventListener("click", accept_requirement);

function get_last_requirement(node_id) {
    if (requirement_id) {
    fetch('/requirements/get_last_requirement/' + node_id).then(function(response) {
        response.json().then(function(data) {
            fill_requirement(data)
            get_requirement_history(data.requirement.requirement_node_id)
        });
    });
    }
    else {
        new_requirement()
    }
}

function get_requirement(requirement_id) {
    if (requirement_id) {
    fetch('/requirements/get_requirement/' + requirement_id).then(function(response) {
        response.json().then(function(data) {
            fill_requirement(data)
            get_requirement_history(data.requirement.requirement_node_id)
        });
    });
    }
    else {
        new_requirement()
    }
}

function fill_requirement(data) {
    document.getElementById('requirement_id').value = data.requirement.requirement_id
    document.getElementById('requirement_node_id').value = data.requirement.requirement_node_id
    document.getElementById('name').value = data.requirement.name
    document.getElementById('description').value = data.requirement.description
    document.getElementsByClassName(' nicEdit-main')[0].innerHTML = data.requirement.description
    document.getElementById('status').value = data.requirement.status_id
    document.getElementById('tags').value = data.requirement.tags
    document.getElementById('priority').value = data.requirement.priority_id
    document.getElementById('type').value = data.requirement.type_id
    if (data.requirement.release){
        document.getElementById('release').checked=true
    } else {
        document.getElementById('release').checked=false
    }

    if (data.requirement.release) {
        document.getElementById('Accept').setAttribute('style' , 'display: inline;')
        if (data.requirement.is_accept) {
            document.getElementById('Accept').value = 'ОДОБРЕНО'
        } else {
            document.getElementById('Accept').value = 'Одобрить'
        }
    } else {
        document.getElementById('Accept').setAttribute('style' , 'display:none')
    }
}


function new_requirement(){
    document.getElementById('requirement_id').value = null
    document.getElementById('name').value = null
    document.getElementsByClassName(' nicEdit-main')[0].innerHTML = ''
    document.getElementById('status').value = null
    document.getElementById('tags').value = null
    document.getElementById('priority').value = null
    document.getElementById('type').value = null
}

function accept_requirement(){
    requirement_id = document.getElementById('requirement_id').value;
    fetch('/requirements/accept/' + requirement_id);
    get_requirement(requirement_id)
    }

function get_requirement_doc(){
fetch('/requirements/requirement_doc/' + document.getElementById('project_id').value).then(function(response) {
    response.json().then(function(data) {
        let requirement_doc = document.getElementById('requirement_doc');
        let doc_HTML = data.requirement_doc != '' ? data.requirement_doc : '';
        requirement_doc.innerHTML = doc_HTML;
    });
});
}

function get_requirement_history(node_id){

fetch('/requirements/history/' + node_id).then(function(response) {
    response.text().then(function(data) {
        let requirement_doc = document.getElementById('requirement_doc');
        let doc_HTML = data != '' ? data : '';
        requirement_doc.innerHTML = doc_HTML;
        });
    });
}
