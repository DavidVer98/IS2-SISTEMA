const lista1 = document.getElementById('TO_DO');
const lista2 = document.getElementById('DOING');
const lista3 = document.getElementById('DONE');

Sortable.create(lista1, {

    group: {
        name: 'userStory',

    },
    animation: 150,

    sort: false, // To disable sorting: set sort to false
    filter: ".divider", //anular drop and drag

    store: {
        //Guardamos el orden de la lista
        set: (sortable) => {
            const orden = sortable.toArray();
            localStorage.setItem('to_do', orden.join('|'));
            // console.log(orden);
        },
        get: function () {
            const orden = localStorage.getItem('to_do');
            // console.log("get", orden)
            return orden ? orden.split('|') : [];
        }
    },

    onAdd: function (/**Event*/evt) {
        estado(evt, 'TO DO');
    }

}),


    Sortable.create(lista2, {

        group: {
            name: 'userStory',
        },

        animation: 150,
        sort: false, // To disable sorting: set sort to false
        filter: ".divider", //anular drop and drag
        store: {
            //Guardamos el orden de la lista
            set: (sortable) => {
                const orden = sortable.toArray();
                localStorage.setItem('doing', orden.join('|'));
                //console.log(orden);
            },
            get: function () {
                const orden = localStorage.getItem('doing');
                // console.log("get", orden)
                return orden ? orden.split('|') : [];
            }
        },
        onAdd: function (/**Event*/evt) {
            estado(evt, 'DOING');
        }
    }),
    Sortable.create(lista3, {
        group: {
            name: 'userStory',

        },

        animation: 150,
        filter: ".divider", //anular drop and drag
        store: {
            //Guardamos el orden de la lista
            set: (sortable) => {
                const orden = sortable.toArray();
                localStorage.setItem('done', orden.join('|'));
                //console.log(orden);
            },
            get: (sortable) => {
                const orden = localStorage.getItem('done');
                // console.log("get", orden ? orden.split('|') : [])
                return orden ? orden.split('|') : [];
            }

        },
        onAdd: function (/**Event*/evt) {
            estado(evt, 'DONE');
        }


    })

const estado = function estado(evt, estado) {
    var xhr = new XMLHttpRequest();
    token = document.querySelector('[name=csrfmiddlewaretoken]').value
    // console.log(token)
    xhr.open("POST", 'sprintbacklog/estadous', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', token)
    xhr.send(JSON.stringify({"us_id": evt.item.attributes['data-id'].value, "estado": estado}));
}