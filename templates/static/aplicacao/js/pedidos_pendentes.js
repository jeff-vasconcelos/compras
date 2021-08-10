const botaoVerPedidosPendentes = document.getElementById('ver_pedidos_pendentes')
const resultsPedidosPendentes = document.getElementById('pedidos-pendentes-modal')

const verPedidosPendentes = (produto, filial) => {
    $.ajax({
        type: 'POST',
        url: '/painel/ver-pedido-pendentes/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': produto,
            'filial':filial
        },
        success: (pedidos_pendentes) => {

            const data = pedidos_pendentes.data
            if (data === 'FALSE'){

                mensagemErro.innerHTML += `
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
                            <use xlink:href="#exclamation-triangle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Por favor selecione um produto!
                        </div>
                    </div>
                `
                $(document).ready(function () {
                    // show the alert
                    setTimeout(function () {
                        $(".alert").alert('close');
                    }, 6000);
                });
            }

            if (data === 'NOTPEDIDO'){

                mensagemErro.innerHTML += `
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
                            <use xlink:href="#exclamation-triangle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Não há pedidos pendentes do produtop selecionado!
                        </div>
                    </div>
                `

                $(document).ready(function () {
                    // show the alert
                    setTimeout(function () {
                        $(".alert").alert('close');
                    }, 6000);
                });
            }

            if (Array.isArray(data)){
                resultsPedidosPendentes.innerHTML = ""
                data.forEach(prod=> {
                    resultsPedidosPendentes.innerHTML += `
                    <tr>
                        <td>${prod.cod_filial}</td>
                        <td>${prod.cod_produto}</td>
                        <td>${prod.desc_produto}</td>
                        <td>${prod.saldo}</td>
                        <td>${prod.data_ped}</td>
                        <td>${prod.num_pedido}</td>
                     </tr>
                    `
                })
            }
        }
    });
}
botaoVerPedidosPendentes.addEventListener('click', e => {
    const produtoSelecionado = listaProdutosSelecionar.value
    const filialSelecionado = listaFiliais.value
    verPedidosPendentes(produtoSelecionado, filialSelecionado)
})