// Call the dataTables jQuery plugin
$(document).ready(function () {
    $('#dataTable').DataTable({
        "order": [[0, "desc"]],
        "language": {
            "search": "Pesquisar",
            "paginate": {
                "next": "Próximo",
                "previous": "Anterior",
                "first": "Primeiro",
                "last": "Último"
            },
            "pageLength": {
                "-1": "Mostrar todos os registros",
                "1": "Mostrar 1 registro",
                "_": "Mostrar %d registros"
            },
            "infoEmpty": "Mostrando 0 até 0 de 0 registros",
            "emptyTable": "Nenhum registro encontrado",
            "zeroRecords": "Nenhum registro encontrado",
            "emptyPanes": "Nenhum Painel de Pesquisa",
            "infoFiltered": "(Filtrados de _MAX_ registros)",
            "info": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
            "count": "{total}",
            "countFiltered": "{shown} ({total})",
            "lengthMenu": "Exibir _MENU_ resultados por página",
            // "lengthMenu": [100, "All"],
        },
        "lengthMenu": [ 100 ]
    });
});