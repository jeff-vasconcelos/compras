const botaoVerPedidosPendentes = document.getElementById('ver_pedidos_pendentes')
const resultsPedidosPendentes = document.getElementById('pedidos-pendentes-modal')

const verPedidosPendentes = (produto) => {
    $.ajax({
        type: 'POST',
        url: '/painel/ver-pedido-pendentes/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': produto
        },
        success: (pedidos_pendentes) => {
            console.log(pedidos_pendentes.data)

            const data = pedidos_pendentes.data
            console.log(data)
            if (Array.isArray(data)){
                resultsPedidosPendentes.innerHTML = ""
                data.forEach(prod=> {
                    resultsPedidosPendentes.innerHTML += `
                    <tr>
                        <td>${prod.cod_filial}</td>
                        <td>${prod.cod_produto}</td>
                        <td>${prod.desc_produto}</td>
                        <td>R$ ${prod.saldo}</td>
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
    verPedidosPendentes(produtoSelecionado)
})