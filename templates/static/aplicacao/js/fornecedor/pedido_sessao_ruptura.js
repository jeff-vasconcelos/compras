

const botaoExportarRupturaFornec = document.getElementById('btn-expo-modal-ruptura_fornec')

const verPedidoRupturaFornec = document.getElementById('ver_pedido_ruptura_fornec')

const msmSucessoRupturaFornec = document.getElementById('div-mensagem-sucesso_ruptura_fornec')
const msmAlertaRupturaFornec = document.getElementById('div-mensagem-alerta_ruptura_fornec')

const resultsPedidoRupturaFornec = document.getElementById('tbody_pedidos_ruptura_fornec')

const csrf_ = document.getElementsByName('csrfmiddlewaretoken')[0].value


function GetNome_alerta(CodProd) {

    const filial_ruptura_fornec = document.getElementById('filial_ruptura_fornec-'+CodProd)
    const produtos_ruptura_fornec = document.getElementById('produto_ruptura_fornec-'+CodProd)
    const input_valor_ruptura_fornec = document.getElementById('vl_digit_ruptura_fornec-'+CodProd)
    const input_quantidade_ruptura_fornec = document.getElementById('qt_digit_ruptura_fornec-'+CodProd)


    const produto = produtos_ruptura_fornec.value
    const filial = filial_ruptura_fornec.value

    console.log(produto)

    const qt_dig = input_quantidade_ruptura_fornec.value
    var qt_digitada = 0
    if (qt_dig === "") {
        qt_digitada = 0
    } else {
        qt_digitada = qt_dig
    }

    // PEGANDO PR COMPRA
    const p_comp = input_valor_ruptura_fornec.value
    var p_compra = 0
    if (p_comp === "") {
        p_compra = 0
    } else {
        p_compra = p_comp
    }

    input_quantidade_ruptura_fornec.value = ''
    input_valor_ruptura_fornec.value = ''


    add_pedido_ruptura_fornec(produto, qt_digitada, p_compra, filial)

    //alert(NomeBotao);
}

// ADD PRODUTO AO PEDIDO NA SESSAO
const add_pedido_ruptura_fornec = (produto, qt_digitada, pr_compra, filial) => {
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

                msmSucessoRupturaFornec.innerHTML += `
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

                msmAlertaRupturaFornec.innerHTML += `
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
const ver_pedido_ruptura_fornec = () => {
    $.ajax({
        type: 'GET',
        url: '/painel/ver-produto-pedido/',
        success: (pedido_sessao) => {

            const data = pedido_sessao.data

            if (data === "FALSE") {
                botaoExportarRupturaFornec.style.display = 'none'
            }

            if (Array.isArray(data)) {
                resultsPedidoRupturaFornec.innerHTML = ""
                data.forEach(prod => {
                    resultsPedidoRupturaFornec.innerHTML += `
                    <tr>
                        <td>${prod.ped_cod_filial}</td>
                        <td>${prod.ped_produto_cod}</td>
                        <td>${prod.ped_produto_nome}</td>
                        <td>${prod.ped_pr_compra}</td>
                        <td>${prod.ped_qt_digitada}</td>

                        <td>
                            <button onclick="rm_prod_pedido_ruptura_fornec(this.id)" type="button" name="botao_remover_prod_sessao" id="${prod.ped_produto_id}" class="botao_remover_p_sessao btn btn-danger btn-sm">
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
verPedidoRupturaFornec.addEventListener('click', e => {
    ver_pedido_ruptura_fornec()
})


// REMOVER PRODUTO AO PEDIDO NA SESSAO
const rmPedidoRupturaFornec = (produto) => {
    $.ajax({
        type: 'POST',
        url: '/painel/rm-produto-pedido/',
        data: {
            'csrfmiddlewaretoken': csrf_,
            'produto': produto
        },
        success: (pedido_sessao) => {
            msmSucessoRupturaFornec.innerHTML += `
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                            <use xlink:href="#check-circle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Produto <strong>removido</strong> do pedido com sucesso!
                        </div>
                    </div>
                `
            resultsPedidoRupturaFornec.innerHTML = ""
            // location.reload();
            $(".modal_pedido_ruptura_fornec").modal('hide');

            $(document).ready(function () {
                // show the alert
                setTimeout(function () {
                    $(".alert").alert('close');
                }, 6000);
            });


        }
    });

}

function rm_prod_pedido_ruptura_fornec(prod_id) {
    const produto = prod_id
    rmPedidoRupturaFornec(produto)
}


const exportPedidoRupturaFornec = (fornecedor) => {
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

botaoExportarRupturaFornec.addEventListener("click", e => {

    const fornecedor = document.getElementById("select_fornec_ruptura_id").value

    exportPedidoRupturaFornec(fornecedor);

    resultsPedidoRupturaFornec.innerHTML = ""
    document.getElementById("search-pedido-ruptura-fornec").value='';
    $(".modal_pedido_ruptura_fornec").modal('hide');

    $(document).ready(function () {
        // show the alert
        setTimeout(function () {
            $(".alert").alert('close');
        }, 6000);
    });

})
