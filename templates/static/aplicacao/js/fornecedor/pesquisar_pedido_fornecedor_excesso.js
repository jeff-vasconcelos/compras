const searchPedidoExcessoFornec = document.getElementById('search-pedido-excesso-fornec')
const resultPedidoExcessoFornec = document.getElementById('result-pedido-excesso-fornec')
const FornecedoresExcessoFornec = document.getElementsByName('item-fornecedor-pedido_excesso')
const checkFornecedorExcessoFornec = []

const BuscarFornecPedidoExcessoFornc = (fornec) => {
    $.ajax({
        type: 'POST',
        url: '/painel/search/fornec',
        data: {
            'csrfmiddlewaretoken': csrf_,
            'fornecedor': fornec,
        },
        success: (res_f) => {
            const data = res_f.data
            if (Array.isArray(data)) {
                resultPedidoExcessoFornec.innerHTML = ""
                data.forEach(fornec => {
                    resultPedidoExcessoFornec.innerHTML += `
                    <input name="item-fornecedor-pedido_excesso" class="form-check-input" type="checkbox" value="${fornec.nome}" id="${fornec.pk}" 
                    style="display: block" onclick="selecao_fornecedor_pedido_excesso_fornec()">
                        <label style="display: block" class="form-check-label" for="${fornec.pk}">
                            ${fornec.cod} - ${fornec.nome}
                        </label>
                    `
                })
            } else {
                if (searchPedidoExcessoFornec.value.length > 0) {
                    resultPedidoExcessoFornec.innerHTML = `<b>${data}</b>`
                } else {
                    resultPedidoExcessoFornec.classList.add('d-none')

                }
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}

searchPedidoExcessoFornec.addEventListener('keyup', e => {

    if (resultPedidoExcessoFornec.classList.contains('d-none')) {
        resultPedidoExcessoFornec.classList.remove('d-none')
    }

    BuscarFornecPedidoExcessoFornc(e.target.value)
})


const filterFornecpedExcessoFornc = (forn) => {
    $.ajax({
        type: 'POST',
        url: '/painel/filter-fornec/',
        data: forn,
        processData: false,
        contentType: false,
        success: (res_fil_fornec) => {
            resultPedidoExcessoFornec.classList.add('d-none')
            botaoExportarExcessoFornec.style.display = 'block'
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function selecao_fornecedor_pedido_excesso_fornec() {
    for (var i = 0; i < FornecedoresExcessoFornec.length; i++) {
        if (FornecedoresExcessoFornec[i].checked == true) {

            // const idCheck = FornecedoresExcessoFornec[i].value
            const textoLabelCheck = FornecedoresExcessoFornec[i].value
            const idCheck = FornecedoresExcessoFornec[i].id;

            document.getElementById("search-pedido-excesso-fornec").value=textoLabelCheck;
            document.getElementById("select_fornec_excesso_id").value=idCheck;

            if (checkFornecedorExcessoFornec.indexOf(idCheck) > -1) {

            } else {
                checkFornecedorExcessoFornec.push(idCheck)
            }

        } else if (FornecedoresExcessoFornec[i].checked == false) {
            const desmarq = FornecedoresExcessoFornec[i].id
            if (checkFornecedorExcessoFornec.indexOf(desmarq) > -1) {
                checkFornecedorExcessoFornec.splice(checkFornecedorExcessoFornec.indexOf(desmarq), 1)
            }
        }
    }
    console.log(checkFornecedorExcessoFornec)

    const fornecedores_selecionados = new FormData()
    fornecedores_selecionados.append('csrfmiddlewaretoken', csrf_)
    fornecedores_selecionados.append('fornecedor', checkFornecedorExcessoFornec)

    filterFornecpedExcessoFornc(fornecedores_selecionados)
}
