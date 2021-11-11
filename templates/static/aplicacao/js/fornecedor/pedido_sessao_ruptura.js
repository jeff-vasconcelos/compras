const botaoExportarRupturaFornec = document.getElementById('btn-expo-modal-ruptura_fornec')

const verPedidoRupturaFornec = document.getElementById('ver_pedido_ruptura_fornec')

const msmSucessoRupturaFornec = document.getElementById('div-mensagem-sucesso_ruptura_fornec')
const msmAlertaRupturaFornec = document.getElementById('div-mensagem-alerta_ruptura_fornec')

const resultsPedidoRupturaFornec = document.getElementById('tbody_pedidos_ruptura_fornec')

const csrf_ = document.getElementsByName('csrfmiddlewaretoken')[0].value


function CarregaInputs() {

    const input_filial_ruptura_fornec = document.getElementsByName('input_ruptura_fornec_filial')
    const input_produtos_ruptura_fornec = document.getElementsByName('input_ruptura_fornec_idproduto')
    const input_quantidade_ruptura_fornec = document.getElementsByClassName('input_ruptura_fornec_quantidade')
    const input_valor_ruptura_fornec = document.getElementsByName('input_ruptura_fornec_preco')

    const filiais_ruptura = []
    const produtos_ruptura = []
    const quantidades_ruptura = []
    const valores_ruptura = []

    const indices = []


    // Pegando quantidades digitadas
    for (let i = 0; i < input_quantidade_ruptura_fornec.length; i++) {
        let quantidade = input_quantidade_ruptura_fornec[i];
        // console.log(quantidades_ruptura)
        if (quantidade.value !== '') {
            quantidades_ruptura.push(quantidade.value.replace(",", "."))
            indices.push(i)
            quantidade.value = ''
        }
    }

    // Pegando preços digitados
    indices.forEach(function (v) {
        let preco = input_valor_ruptura_fornec[v];
        let valor_preco = preco.value.replace(".", "")
        valores_ruptura.push(valor_preco.replace(",", "."))
        preco.value = ''
    });

    // Pegando codigos de filiais
    indices.forEach(function (i) {
        let filial = input_filial_ruptura_fornec[i];
        filiais_ruptura.push(filial.value)
    });


    // Pegando ids de produtos
    indices.forEach(function (p) {
        let prodt = input_produtos_ruptura_fornec[p];
        produtos_ruptura.push(prodt.value)
    });


    console.log('filiais', filiais_ruptura)
    console.log('produtos', produtos_ruptura)
    console.log('quantidades', quantidades_ruptura)
    console.log('preços', valores_ruptura)

    const fornecedores_ruptura = new FormData()
    fornecedores_ruptura.append('csrfmiddlewaretoken', csrf_)
    fornecedores_ruptura.append('filiais', filiais_ruptura)
    fornecedores_ruptura.append('produtos', produtos_ruptura)
    fornecedores_ruptura.append('quantidades', quantidades_ruptura)
    fornecedores_ruptura.append('precos', valores_ruptura)

    add_pedido_ruptura_fornec(fornecedores_ruptura)

}


function CarregarSugestaoPreco() {

    let sugestao_lista = []
    let indice = []
    let valores_sugestao = []

    let inputs_ids_produtos = document.getElementsByClassName("input_ruptura_fornec_quantidade");
    let inputs_sugestao = document.getElementsByName("input_ruptura_fornec_sugestao");
    let medias = document.getElementsByName("input_ruptura_fornec_media");
    let ddes = document.getElementsByName("input_ruptura_fornec_dde");

    for (let i = 0; i < inputs_sugestao.length; i++) {
        let sugest = inputs_sugestao[i];
        if (sugest.value !== '') {
            sugestao_lista.push(sugest.value.replace(",", "."))
            indice.push(i)
        }
    }

    indice.forEach(function (v) {
        let sugestao = inputs_sugestao[v];
        let valor_sugestao = sugestao.value.replace(".", "")

        valores_sugestao.push(valor_sugestao.replace(",0", ""))
        // sugestao.value = ''
        console.log(valores_sugestao)
    });

    for (let i = 0; i < inputs_ids_produtos.length; i++) {
        let id_prod = inputs_ids_produtos[i];
        let media = parseFloat(medias[i].value);
        let qt = parseFloat(valores_sugestao[i]);
        let dde = Math.round(qt / media);
        ddes[i].value = dde;
        id_prod.value = qt;
    }

    // let input_dde = document.getElementById("input_ruptura_fornec_dde_" + id_produto);

    // let media = parseFloat(input_media.value)
    // let qt_digitada = parseFloat(input_qt_digitada.value)
    //
    // input_dde.value = Math.round(qt_digitada / media)

    // qt_digitada.value = qt_digitada.value.toUpperCase();
}


function calculaDDERuptura(id_produto) {
    let input_qt_digitada = document.getElementById("input_ruptura_fornec_quantidade_" + id_produto);
    let input_media = document.getElementById("input_ruptura_fornec_media_" + id_produto);
    let input_dde = document.getElementById("input_ruptura_fornec_dde_" + id_produto);

    let media = parseFloat(input_media.value)
    let qt_digitada = parseFloat(input_qt_digitada.value)

    input_dde.value = Math.round(qt_digitada / media)

    // qt_digitada.value = qt_digitada.value.toUpperCase();
}


// ADD PRODUTO AO PEDIDO NA SESSAO
const add_pedido_ruptura_fornec = (dados_prods_ruptura) => {
    console.log(dados_prods_ruptura)
    $.ajax({
        type: 'POST',
        url: '/painel/add-produtos-pedido-fornecedores/',
        data: dados_prods_ruptura,
        processData: false,
        contentType: false,
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
    document.getElementById("search-pedido-ruptura-fornec").value = '';
    $(".modal_pedido_ruptura_fornec").modal('hide');

    $(document).ready(function () {
        // show the alert
        setTimeout(function () {
            $(".alert").alert('close');
        }, 6000);
    });

})
