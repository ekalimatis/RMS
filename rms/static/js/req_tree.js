let jstree_div = document.getElementById('jstree_div');
let url = '/requirements/tree_data/1';






jstree_div.addEventListener('load', function (){
    fetch(url).then(function (response){
        let r = response.json()
        console.log(r)
    })

})



/*
$('#jstree_demo_div').jstree({ 'core' : {
        'data' : [
            {
                "id": "1",
                "parent": "#",
                "text": "[\u041a\u043e\u0440\u0435\u043d\u0432\u043e\u0435 \u0442\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430]"
            },
            {
                "id": "10",
                "parent": "1",
                "text": "[\u041a\u043e\u0440\u0435\u043d\u0432\u043e\u0435 \u0442\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430] -> [asdadsd]"
            },
            {
                "id": "11",
                "parent": "10",
                "text": "[\u041a\u043e\u0440\u0435\u043d\u0432\u043e\u0435 \u0442\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430] -> [asdadsd] -> [\u044b\u0432\u0444\u044b\u0432\u0444\u044b]"
            }
        ]
    } });*/
/*
let jstree_div = document.getElementById('jstree_div');

fetch('/requirements/requirement_list/' + 1).then(function(response) {
    response.json().then(function(data) {
        jstree_div.jstree({


            'core' : {
                'data' : {
                    'url' : '/requirements/requirement_list/1',
                    'data' : function (node) {
                        return { 'id' : node.id };
                    }
                }}

        })

    });
});

 */

/*
fetch(url)
    .then(res.json())
    .then(out
        //console.log('Checkout this JSON! ', out.data))
    (function () {
            jstree_div.jstree({'core': { 'data': out.data}})}));

 */
/*
fetch(url).then(
    function (response){
        response.json().then(
            function (resp){
                jstree_div.jstree()
            }
        )
    }
)
*/


