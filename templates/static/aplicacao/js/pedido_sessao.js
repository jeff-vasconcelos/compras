
const ProdutosSelecionar = document.getElementById('results-produtos')
const inputPrCompraDigitada = document.getElementById('pr_compra')
const inputMargemDigitada = document.getElementById('porc_margem')
const inputPrSugeridoDigitada = document.getElementById('pr_sugerido')
const inputDDEDigitada = document.getElementById('dde')
const inputQtDigitada = document.getElementById('qt_digit')

const botaoPedidoSessao = document.getElementById('add_pedido_sessao')
const botaoVerPedidoSessao = document.getElementById('ver_pedido_sessao')
const resultPedidoSessao = document.getElementById('tbody_pedidos_sessao')

const botaoRemoverPedidoSessao = document.getElementsByName('botao_remover_prod_sessao')
const modalPedidosSessao = document.getElementById('modal-ver-pedido-geral')


// ADD PRODUTO AO PEDIDO NA SESSAO
const addPedidoSessao = (produto, qt_digitada, pr_compra, margem, pr_sugerido, dde) => {
    $.ajax({
        type: 'POST',
        url: '/painel/add-produto-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': produto,
            'qt_digitada': qt_digitada,
            'pr_compra': pr_compra,
            'margem': margem,
            'pr_sugerido': pr_sugerido,
            'dde': dde
        },
        success: (pedido_sessao) => {
            console.log(pedido_sessao.data)
            location.reload();
        }
    });
}
botaoPedidoSessao.addEventListener('click', e => {
    // PEGANDO PRODUTO SELECIONADO
    const produtoSelecionado = ProdutosSelecionar.value

    console.log(inputQtDigitada)

    // PEGANDO QT DIGITADA
    const qt_dig = inputQtDigitada.value
    var qt_digitada = 0
    if (qt_dig === "") {
        qt_digitada = 0
    } else {
        qt_digitada = qt_dig
    }

    // PEGANDO PR COMPRA
    const p_comp = inputPrCompraDigitada.value
    var p_compra = 0
    if (p_comp === "") {
        p_compra = 0
    } else {
        p_compra = p_comp
    }

    // PEGANDO MARGEM
    const mar = inputMargemDigitada.value
    var margem = 0
    if (mar === "") {
        margem = 0
    } else {
        margem = mar
    }

    // PEGANDO PR SUGERIDO
    const p_sug = inputPrSugeridoDigitada.value
    var p_sugerido = 0
    if (p_sug === "") {
        p_sugerido = 0
    } else {
        p_sugerido = p_sug
    }

    // PEGANDO DDE
    const dde_p = inputDDEDigitada.value
    var dde = 0
    if (dde_p === "") {
        dde = 0
    } else {
        dde = dde_p
    }

    console.log(produtoSelecionado, "PRODUTO SELECIONADO")
    console.log(qt_digitada, "QT DIGITADA")
    console.log(p_compra, "PRECO DE COMPRA")
    console.log(margem, "MARGEM")
    console.log(p_sugerido, "PRECO SUGERIDO")
    console.log(dde, "DDE")

    addPedidoSessao(produtoSelecionado, qt_digitada, p_compra, margem, p_sugerido, dde)
})


// VER PEDIDO NA SESSAO
const verPedidoSessao = () => {
    $.ajax({
        type: 'GET',
        url: '/painel/ver-produto-pedido/',
        success: (pedido_sessao) => {
            console.log(pedido_sessao.data)

            const data = pedido_sessao.data
            console.log(data)
            if (Array.isArray(data)){
                resultPedidoSessao.innerHTML = ""
                data.forEach(prod=> {
                    resultPedidoSessao.innerHTML += `
                    <tr>
                        <td>${prod.ped_cod_filial}</td>
                        <td>${prod.ped_produto_cod}</td>
                        <td>${prod.ped_produto_nome}</td>
                        <td>R$ ${prod.ped_pr_compra}</td>
                        <td>${prod.ped_qt_digitada}</td>
                        <td>${prod.ped_margem} %</td>
                        <td>
                            <button onclick="rm_prod_pedido_sessao(this.id)" type="button" name="botao_remover_prod_sessao" id="${prod.ped_produto_id}" class="btn btn-danger btn-sm">
                                <i class="fas fa-times-circle fa-1x"></i>
                            </button>
                        </td>
                     </tr>
                    `
                })
            }
        }
    });
}
botaoVerPedidoSessao.addEventListener('click', e => {
    verPedidoSessao()
})


// REMOVER PRODUTO AO PEDIDO NA SESSAO
const rmPedidoSessao = (produto) => {
    $.ajax({
        type: 'POST',
        url: '/painel/rm-produto-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': produto
        },
        success: (pedido_sessao) => {
            console.log(pedido_sessao.data)
            location.reload();
        }
    });

}

function rm_prod_pedido_sessao(prod_id) {
    const produto = prod_id
    rmPedidoSessao(produto)
}

//
// // VER PEDIDO NA SESSAO
// const verPedidoSessao = () => {
//     $.ajax({
//         type: 'GET',
//         url: '/painel/ver-produto-pedido/',
//         success: (pedido_sessao) => {
//             console.log(pedido_sessao.data)
//
//             const data = pedido_sessao.data
//             console.log(data)
//             if (Array.isArray(data)){
//                 resultPedidoSessao.innerHTML = ""
//                 data.forEach(prod=> {
//                     resultPedidoSessao.innerHTML += `
//                     <tr>
//                         <td>${prod.ped_cod_filial}</td>
//                         <td>${prod.ped_produto_cod}</td>
//                         <td>${prod.ped_produto_nome}</td>
//                         <td>R$ ${prod.ped_pr_compra}</td>
//                         <td>${prod.ped_qt_digitada}</td>
//                         <td>${prod.ped_margem} %</td>
//                         <td>
//                             <button onclick="rm_prod_pedido_sessao(this.id)" type="button" name="botao_remover_prod_sessao" id="${prod.ped_produto_id}" class="btn btn-danger btn-sm">
//                                 <i class="fas fa-times-circle fa-1x"></i>
//                             </button>
//                         </td>
//                      </tr>
//                     `
//                 })
//             }
//         }
//     });
// }
// botaoVerPedidoSessao.addEventListener('click', e => {
//     verPedidoSessao()
// })
//
