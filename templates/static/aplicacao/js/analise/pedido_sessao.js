const ProdutosSelecionar = document.getElementById('results-produtos')
const inputPrCompraDigitada = document.getElementById('pr_compra')
const inputMargemDigitada = document.getElementById('porc_margem')
// const inputPrSugeridoDigitada = document.getElementById('pr_sugerido')
// const inputDDEDigitada = document.getElementById('dde')
const inputQtDigitada = document.getElementById('qt_digit')

const botaoExportarPedido = document.getElementById('btn-expo-modal-analise')
const botaoPedidoSessao = document.getElementById('add_pedido_sessao')
const botaoVerPedidoSessao = document.getElementById('ver_pedido_sessao')
const resultPedidoSessao = document.getElementById('tbody_pedidos_sessao')

const botaoRemoverPedidoSessao = document.getElementsByName('botao_remover_prod_sessao')
const modalPedidosSessao = document.getElementById('modal-ver-pedido-geral')

const mensagemSucesso = document.getElementById('div-mensagem-sucesso')
const mensagemAlerta = document.getElementById('div-mensagem-alerta')
const mensagemErro = document.getElementById('div-mensagem-erro')


// ADD PRODUTO AO PEDIDO NA SESSAO
const addPedidoSessao = (produto, qt_digitada, pr_compra, filial) => {
    $.ajax({
        type: 'POST',
        url: '/painel/add-produto-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': produto,
            'qt_digitada': qt_digitada,
            'pr_compra': pr_compra,
            'filial': filial
        },
        success: (pedido_sessao) => {
            console.log(pedido_sessao.data)
            const resposta = pedido_sessao.data

            if (resposta === "SUCESSO") {
                inputQtDigitada.value = ""
                inputPrCompraDigitada.value = ""
                mensagemSucesso.innerHTML += `
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                            <use xlink:href="#check-circle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Produto <strong>adicionado</strong> ao pedido com sucesso!
                        </div>
                    </div>
                `

            } else {
                inputQtDigitada.value = ""
                inputPrCompraDigitada.value = ""
                mensagemAlerta.innerHTML += `
                    <div class="alert alert-warning d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:">
                            <use xlink:href="#exclamation-triangle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Por favor selecione um produto!
                        </div>
                    </div>
                `
            }
            $(document).ready(function () {
                // show the alert
                setTimeout(function () {
                    $(".alert").alert('close');
                }, 5000);
            });

            // location.reload();

        }
    });
}
botaoPedidoSessao.addEventListener('click', e => {
    // PEGANDO PRODUTO SELECIONADO
    const produtoSelecionado = ProdutosSelecionar.value
    const filialSelecionado = listaFiliais.value


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
    // const mar = inputMargemDigitada.value
    // var margem = 0
    // if (mar === "") {
    //     margem = 0
    // } else {
    //     margem = mar
    // }

    // // PEGANDO PR SUGERIDO
    // const p_sug = inputPrSugeridoDigitada.value
    // var p_sugerido = 0
    // if (p_sug === "") {
    //     p_sugerido = 0
    // } else {
    //     p_sugerido = p_sug
    // }
    //
    // // PEGANDO DDE
    // const dde_p = inputDDEDigitada.value
    // var dde = 0
    // if (dde_p === "") {
    //     dde = 0
    // } else {
    //     dde = dde_p
    // }

    let input_dde = document.getElementById("input_analise_dde");
    input_dde.value = ''

    addPedidoSessao(produtoSelecionado, qt_digitada, p_compra, filialSelecionado)
})


// VER PEDIDO NA SESSAO
const verPedidoSessao = () => {
    $.ajax({
        type: 'GET',
        url: '/painel/ver-produto-pedido/',
        success: (pedido_sessao) => {

            const data = pedido_sessao.data

            if (data === "FALSE") {
                botaoExportarPedido.style.display = 'none'
            }

            if (Array.isArray(data)) {
                resultPedidoSessao.innerHTML = ""
                data.forEach(prod => {
                    resultPedidoSessao.innerHTML += `
                    <tr>
                        <td>${prod.ped_cod_filial}</td>
                        <td>${prod.ped_produto_cod}</td>
                        <td>${prod.ped_produto_nome}</td>
                        <td>${prod.ped_pr_compra}</td>
                        <td>${prod.ped_qt_digitada}</td>
                        
                        <td>
                            <button onclick="rm_prod_pedido_sessao(this.id)" type="button" name="botao_remover_prod_sessao" id="${prod.ped_produto_id}" class="botao_remover_p_sessao btn btn-danger btn-sm">
                                <i class="fas fa-times-circle fa-1x"></i>
                            </button>
                        </td>
                     </tr>
                    `
                })
            }
        },
        error: function (error) {
            console.log(error)
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
            mensagemSucesso.innerHTML += `
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                            <use xlink:href="#check-circle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Produto <strong>removido</strong> do pedido com sucesso!
                        </div>
                    </div>
                `
            resultPedidoSessao.innerHTML = ""
            // location.reload();
            $(".modal-pedido").modal('hide');

            $(document).ready(function () {
                // show the alert
                setTimeout(function () {
                    $(".alert").alert('close');
                }, 6000);
            });


        }
    });

}

function rm_prod_pedido_sessao(prod_id) {
    const produto = prod_id
    rmPedidoSessao(produto)
}


const exportPedidoSessao = (fornecedor) => {
    $.ajax({
        type: 'POST',
        url: '/painel/fornecedor-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'fornecedor': fornecedor
        },
        success: () => {

        },
        error: function (error) {

        }
    });
}

botaoExportarPedido.addEventListener("click", e => {
    const fornecedor = document.getElementById("fornec_select_id").value
    resultPedidoSessao.innerHTML = ""
    document.getElementById("search-pedido-fornec").value='';
    $(".modal-pedido").modal('hide');

    $(document).ready(function () {
        // show the alert
        setTimeout(function () {
            $(".alert").alert('close');
        }, 6000);
    });

    exportPedidoSessao(fornecedor);

})
