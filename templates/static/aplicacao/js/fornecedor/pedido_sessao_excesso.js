

const botaoExportarExcessoFornec = document.getElementById('btn-expo-modal-excesso_fornec')

const verPedidoExcessoFornec = document.getElementById('ver_pedido_excesso_fornec')

const msmSucessoExcessoFornec = document.getElementById('div-mensagem-sucesso_excesso_fornec')
const msmAlertaExcessoFornec = document.getElementById('div-mensagem-alerta_excesso_fornec')

const resultsPedidoExcessoFornec = document.getElementById('tbody_pedidos_excesso_fornec')

const csrf_ = document.getElementsByName('csrfmiddlewaretoken')[0].value


function GetNome_alerta(CodProd) {

    const filial_excesso_fornec = document.getElementById('filial_excesso_fornec-'+CodProd)
    const produtos_excesso_fornec = document.getElementById('produto_excesso_fornec-'+CodProd)
    const input_valor_excesso_fornec = document.getElementById('vl_digit_excesso_fornec-'+CodProd)
    const input_quantidade_excesso_fornec = document.getElementById('qt_digit_excesso_fornec-'+CodProd)


    const produto = produtos_excesso_fornec.value
    const filial = filial_excesso_fornec.value

    const qt_dig = input_quantidade_excesso_fornec.value
    var qt_digitada = 0
    if (qt_dig === "") {
        qt_digitada = 0
    } else {
        qt_digitada = qt_dig
    }

    // PEGANDO PR COMPRA
    const p_comp = input_valor_excesso_fornec.value
    var p_compra = 0
    if (p_comp === "") {
        p_compra = 0
    } else {
        p_compra = p_comp
    }

    input_quantidade_excesso_fornec.value = ''
    input_valor_excesso_fornec.value = ''


    add_pedido_excesso_fornec(produto, qt_digitada, p_compra, filial)

    //alert(NomeBotao);
}

// ADD PRODUTO AO PEDIDO NA SESSAO
const add_pedido_excesso_fornec = (produto, qt_digitada, pr_compra, filial) => {
    $.ajax({
        type: 'POST',
        url: '/painel/add-produto-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf_,
            'produto': produto,
            'qt_digitada': qt_digitada,
            'pr_compra': pr_compra,
            'filial': filial
        },
        success: (pedido_sessao) => {
            console.log(pedido_sessao.data)
            const resposta = pedido_sessao.data

            if (resposta === "SUCESSO") {

                msmSucessoExcessoFornec.innerHTML += `
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

                msmAlertaExcessoFornec.innerHTML += `
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


// VER PEDIDO NA SESSAO
const ver_pedido_excesso_fornec = () => {
    $.ajax({
        type: 'GET',
        url: '/painel/ver-produto-pedido/',
        success: (pedido_sessao) => {

            const data = pedido_sessao.data

            if (data === "FALSE") {
                botaoExportarExcessoFornec.style.display = 'none'
            }

            if (Array.isArray(data)) {
                resultsPedidoExcessoFornec.innerHTML = ""
                data.forEach(prod => {
                    resultsPedidoExcessoFornec.innerHTML += `
                    <tr>
                        <td>${prod.ped_cod_filial}</td>
                        <td>${prod.ped_produto_cod}</td>
                        <td>${prod.ped_produto_nome}</td>
                        <td>${prod.ped_pr_compra}</td>
                        <td>${prod.ped_qt_digitada}</td>

                        <td>
                            <button onclick="rm_prod_pedido_excesso_fornec(this.id)" type="button" name="botao_remover_prod_sessao" id="${prod.ped_produto_id}" class="botao_remover_p_sessao btn btn-danger btn-sm">
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
verPedidoExcessoFornec.addEventListener('click', e => {
    ver_pedido_excesso_fornec()
})


// REMOVER PRODUTO AO PEDIDO NA SESSAO
const rmPedidoExcessoFornec = (produto) => {
    $.ajax({
        type: 'POST',
        url: '/painel/rm-produto-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf_,
            'produto': produto
        },
        success: (pedido_sessao) => {
            msmSucessoExcessoFornec.innerHTML += `
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                            <use xlink:href="#check-circle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Produto <strong>removido</strong> do pedido com sucesso!
                        </div>
                    </div>
                `
            resultsPedidoExcessoFornec.innerHTML = ""
            // location.reload();
            $(".modal_pedido_excesso_fornec").modal('hide');

            $(document).ready(function () {
                // show the alert
                setTimeout(function () {
                    $(".alert").alert('close');
                }, 6000);
            });


        }
    });

}

function rm_prod_pedido_excesso_fornec(prod_id) {
    const produto = prod_id
    rmPedidoExcessoFornec(produto)
}


const exportPedidoExcessoFornec = (fornecedor) => {
    $.ajax({
        type: 'POST',
        url: '/painel/fornecedor-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf_,
            'fornecedor': fornecedor
        },
        success: (response) => {
            console.log(response.data)

        },
        error: function (error) {

        }
    });
}

botaoExportarExcessoFornec.addEventListener("click", e => {

    const fornecedor = document.getElementById("select_fornec_excesso_id").value

    exportPedidoExcessoFornec(fornecedor);

    resultsPedidoExcessoFornec.innerHTML = ""
    document.getElementById("search-pedido-excesso-fornec").value='';
    $(".modal_pedido_excesso_fornec").modal('hide');

    $(document).ready(function () {
        // show the alert
        setTimeout(function () {
            $(".alert").alert('close');
        }, 6000);
    });



})
