const searchPedidoRupturaFornec = document.getElementById('search-pedido-ruptura-fornec')
const resultPedidoRupturaFornec = document.getElementById('result-pedido-ruptura-fornec')
const FornecedoresRupturaFornec = document.getElementsByName('item-fornecedor-pedido_ruptura')
const checkFornecedorRupturaFornec = []

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
                resultPedidoRupturaFornec.innerHTML = ""
                data.forEach(fornec => {
                    resultPedidoRupturaFornec.innerHTML += `
                    <input name="item-fornecedor-pedido_ruptura" class="form-check-input" type="checkbox" value="${fornec.nome}" id="${fornec.pk}" 
                    style="display: block" onclick="selecao_fornecedor_pedido_ruptura_fornec()">
                        <label style="display: block" class="form-check-label" for="${fornec.pk}">
                            ${fornec.cod} - ${fornec.nome}
                        </label>
                    `
                })
            } else {
                if (searchPedidoRupturaFornec.value.length > 0) {
                    resultPedidoRupturaFornec.innerHTML = `<b>${data}</b>`
                } else {
                    resultPedidoRupturaFornec.classList.add('d-none')

                }
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}

searchPedidoRupturaFornec.addEventListener('keyup', e => {

    if (resultPedidoRupturaFornec.classList.contains('d-none')) {
        resultPedidoRupturaFornec.classList.remove('d-none')
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
            resultPedidoRupturaFornec.classList.add('d-none')
            botaoExportarRupturaFornec.style.display = 'block'
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function selecao_fornecedor_pedido_ruptura_fornec() {
    for (var i = 0; i < FornecedoresRupturaFornec.length; i++) {
        if (FornecedoresRupturaFornec[i].checked == true) {

            // const idCheck = FornecedoresRupturaFornec[i].value
            const textoLabelCheck = FornecedoresRupturaFornec[i].value
            const idCheck = FornecedoresRupturaFornec[i].id;

            document.getElementById("search-pedido-ruptura-fornec").value=textoLabelCheck;
            document.getElementById("select_fornec_ruptura_id").value=idCheck;

            if (checkFornecedorRupturaFornec.indexOf(idCheck) > -1) {

            } else {
                checkFornecedorRupturaFornec.push(idCheck)
            }

        } else if (FornecedoresRupturaFornec[i].checked == false) {
            const desmarq = FornecedoresRupturaFornec[i].id
            if (checkFornecedorRupturaFornec.indexOf(desmarq) > -1) {
                checkFornecedorRupturaFornec.splice(checkFornecedorRupturaFornec.indexOf(desmarq), 1)
            }
        }
    }
    console.log(checkFornecedorRupturaFornec)

    const fornecedores_selecionados = new FormData()
    fornecedores_selecionados.append('csrfmiddlewaretoken', csrf_)
    fornecedores_selecionados.append('fornecedor', checkFornecedorRupturaFornec)

    filterFornecpedExcessoFornc(fornecedores_selecionados)
}
