let jstree_div = document.getElementById('jstree_div');
let url = '/requirements/tree_data/' + jstree_div.getAttribute('project_id')
function draw_tree(){
    fetch(url).then(function (response){
        response.json().then(
            function(r){jQuery('#jstree_div').jstree(
                {'core':{'data':r.data}}
            )}
        )
    })
}
draw_tree()