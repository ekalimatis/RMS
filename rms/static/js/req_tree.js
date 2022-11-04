let jstree_div = document.getElementById('jstree_div');
let url = '/requirements/tree_data/' + jstree_div.getAttribute('project_id')
document.getElementById('new').addEventListener("click", new_requirement);
function draw_tree(){
    fetch(url).then(function (response){
        response.json().then(
            function(r){
            jQuery('#jstree_div').jstree({'core':{'data':r.data}});
            change_rec()
            }
        )
    })
}
draw_tree()

function change_rec() {
    jQuery('#jstree_div')
        .on('changed.jstree', function (e, data) {
                jQuery(get_requirement(data.instance.get_node(data.selected[0]).id));
        });
};
