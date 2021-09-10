const searchPedidoFornec = document.getElementById('search-pedido-fornec')
const resultsPedidoFornec = document.getElementById('results-pedido-fornec')
const FornecedoresPed = document.getElementsByName('item-fornecedor-pedido')
const checkFornecedorPed = []

const BuscarPedidoFornec = (fornec) => {
    $.ajax({
        type: 'POST',
        url: '/painel/search/fornec',
        data: {
            'csrfmiddlewaretoken': csrf,
            'fornecedor': fornec,
        },
        success: (res_f) => {
            const data = res_f.data
            if (Array.isArray(data)) {
                resultsPedidoFornec.innerHTML = ""
                data.forEach(fornec => {
                    resultsPedidoFornec.innerHTML += `
                    <input name="item-fornecedor-pedido" class="form-check-input" type="checkbox" value="${fornec.nome}" id="${fornec.pk}" 
                    style="display: block" onclick="selecao_fornecedor_pedido()">
                        <label style="display: block" class="form-check-label" for="${fornec.pk}">
                            ${fornec.cod} - ${fornec.nome}
                        </label>
                    `
                })
            } else {
                if (searchPedidoFornec.value.length > 0) {
                    resultsPedidoFornec.innerHTML = `<b>${data}</b>`
                } else {
                    resultsPedidoFornec.classList.add('d-none')

                }
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}

searchPedidoFornec.addEventListener('keyup', e => {

    if (resultsPedidoFornec.classList.contains('d-none')) {
        resultsPedidoFornec.classList.remove('d-none')
    }

    BuscarPedidoFornec(e.target.value)
})


const filterFornecPed = (forn) => {
    $.ajax({
        type: 'POST',
        url: '/painel/filter-fornec/',
        data: forn,
        processData: false,
        contentType: false,
        success: (res_fil_fornec) => {
            resultsPedidoFornec.classList.add('d-none')
            botaoExportarPedido.style.display = 'block'
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function selecao_fornecedor_pedido() {
    for (var i = 0; i < FornecedoresPed.length; i++) {
        if (FornecedoresPed[i].checked == true) {

            // const idCheck = FornecedoresPed[i].value
            const textoLabelCheck = FornecedoresPed[i].value
            const idCheck = FornecedoresPed[i].id;

            document.getElementById("search-pedido-fornec").value=textoLabelCheck;
            document.getElementById("fornec_select_id").value=idCheck;

            if (checkFornecedorPed.indexOf(idCheck) > -1) {

            } else {
                checkFornecedorPed.push(idCheck)
            }

        } else if (FornecedoresPed[i].checked == false) {
            const desmarq = FornecedoresPed[i].id
            if (checkFornecedorPed.indexOf(desmarq) > -1) {
                checkFornecedorPed.splice(checkFornecedorPed.indexOf(desmarq), 1)
            }
        }
    }

    const fornecedores_selecionados = new FormData()
    fornecedores_selecionados.append('csrfmiddlewaretoken', csrf)
    fornecedores_selecionados.append('fornecedor', checkFornecedorPed)

    filterFornecPed(fornecedores_selecionados)
}
