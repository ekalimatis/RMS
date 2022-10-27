function get_requirement(requirement_id) {
    if (requirement_id) {
    fetch('/requirements/get_requirement/' + requirement_id).then(function(response) {
        response.json().then(function(data) {
            document.getElementById('requirement_id').value = data.requirement.requirement_id
            document.getElementById('requirement_node_id').value = data.requirement.requirement_node_id
            document.getElementById('name').value = data.requirement.name
            document.getElementById('description').textContent = data.requirement.description
            document.getElementById('status').value = data.requirement.status_id
            document.getElementById('tags').value = data.requirement.tags
            document.getElementById('priority').value = data.requirement.priority_id
            document.getElementById('type').value = data.requirement.type_id

            if (data.requirement.is_accept) {
                document.getElementById('Accept').value = 'ОДОБРЕНО'
            } else {
                document.getElementById('Accept').value = 'Одобрить'
            }

        });
    });
    }
    else {
        new_requirement()
    }
}

function new_requirement(){
    document.getElementById('requirement_id').value = null
    document.getElementById('name').value = null
    document.getElementById('description').innerHTML = ''
    document.getElementById('status').value = null
    document.getElementById('tags').value = null
    document.getElementById('priority').value = null
    document.getElementById('type').value = null
}

function accept_requirement(){
    requirement_id = document.getElementById('requirement_id').value;
    fetch('/requirements/accept/' + requirement_id);
    }