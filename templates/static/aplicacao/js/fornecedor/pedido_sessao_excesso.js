

const botaoExportarExcessoFornec = document.getElementById('btn-expo-modal-excesso_fornec')

const verPedidoExcessoFornec = document.getElementById('ver_pedido_excesso_fornec')

const msmSucessoExcessoFornec = document.getElementById('div-mensagem-sucesso_excesso_fornec')
const msmAlertaExcessoFornec = document.getElementById('div-mensagem-alerta_excesso_fornec')

const resultsPedidoExcessoFornec = document.getElementById('tbody_pedidos_excesso_fornec')

const csrf_e = document.getElementsByName('csrfmiddlewaretoken')[0].value


function CarregaInputsExcesso() {

    const input_filial_excesso_fornec = document.getElementsByName('input_excesso_fornec_filial')
    const input_produtos_excesso_fornec = document.getElementsByName('input_excesso_fornec_idproduto')
    const input_quantidade_excesso_fornec = document.getElementsByClassName('input_excesso_fornec_quantidade')
    const input_valor_excesso_fornec = document.getElementsByName('input_excesso_fornec_preco')

    const filiais_excesso = []
    const produtos_excesso = []
    const quantidades_excesso = []
    const valores_excesso = []

    const indices = []


    // Pegando quantidades digitadas
    for (let i = 0; i < input_quantidade_excesso_fornec.length; i++) {
        let quantidade = input_quantidade_excesso_fornec[i];
        // console.log(quantidades_excesso)
        if (quantidade.value !== '') {
            quantidades_excesso.push(quantidade.value.replace(",", "."))
            indices.push(i)
            quantidade.value = ''
        }
    }

    // Pegando preços digitados
    indices.forEach(function (v) {
        let preco = input_valor_excesso_fornec[v];
        let valor_preco = preco.value.replace(".", "")
        valores_excesso.push(valor_preco.replace(",", "."))
        preco.value = ''
    });

    // Pegando codigos de filiais
    indices.forEach(function (i) {
        let filial = input_filial_excesso_fornec[i];
        filiais_excesso.push(filial.value)
    });


    // Pegando ids de produtos
    indices.forEach(function (p) {
        let prodt = input_produtos_excesso_fornec[p];
        produtos_excesso.push(prodt.value)
    });


    console.log('filiais', filiais_excesso)
    console.log('produtos', produtos_excesso)
    console.log('quantidades', quantidades_excesso)
    console.log('preços', valores_excesso)

    const fornecedores_excesso = new FormData()
    fornecedores_excesso.append('csrfmiddlewaretoken', csrf_e)
    fornecedores_excesso.append('filiais', filiais_excesso)
    fornecedores_excesso.append('produtos', produtos_excesso)
    fornecedores_excesso.append('quantidades', quantidades_excesso)
    fornecedores_excesso.append('precos', valores_excesso)

    add_pedido_excesso_fornec(fornecedores_excesso)

}

function calculaDDEExcesso(id_produto) {
    let input_qt_digitada = document.getElementById("input_excesso_fornec_quantidade_" + id_produto);
    let input_media = document.getElementById("input_excesso_fornec_media_" + id_produto);
    let input_dde = document.getElementById("input_excesso_fornec_dde_" + id_produto);

    let media = parseFloat(input_media.value)
    let qt_digitada = parseFloat(input_qt_digitada.value)

    input_dde.value = Math.round(qt_digitada / media)

    // qt_digitada.value = qt_digitada.value.toUpperCase();
}


// ADD PRODUTO AO PEDIDO NA SESSAO
const add_pedido_excesso_fornec = (dados_prods_excesso) => {
    $.ajax({
        type: 'POST',
        url: '/painel/add-produtos-pedido-fornecedores/',
        data: dados_prods_excesso,
        processData: false,
        contentType: false,
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
                            &nbsp; Por favor selecione um produto ou verifique se os campos dos produtos estão preenchidos!
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
            'csrfmiddlewaretoken': csrf_e,
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
            'csrfmiddlewaretoken': csrf_e,
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
