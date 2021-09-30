const listaProdutos = document.getElementsByName('item-produto')
const resultadosPProdutos = document.getElementById('results-produtos')
const checkProduto = []


const filterProd = (prod) => {
    $.ajax({
        type: 'POST',
        url: '/painel/filter-prod/',
        data: prod,
        processData: false,
        contentType: false,
        success: (res_fil_prod) => {
            const data = res_fil_prod.data

            const data_p = data[0]
            const marcas = data[1]

            if (Array.isArray(data_p)) {
                resultadosPProdutos.innerHTML = `<option class="option-analise" value="0" selected>Selecione o produto</option>`
                listaCurvaSelecionar.innerHTML = `
                    <select class="form-control select-analise" id="curva_abc_select">
                        <option class="option-analise" selected value="0">Selecione</option>
                        <option class="option-analise" value="A">A</option>
                        <option class="option-analise" value="B">B</option>
                        <option class="option-analise" value="C">C</option>
                        <option class="option-analise" value="D">D</option>
                        <option class="option-analise" value="E">E</option>
                    </select>
                `
                data_p.forEach(prod => {
                    resultadosPProdutos.innerHTML += `
                        <option name="option-product" class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome}</option>
                    `
                })
            }
            if (Array.isArray(marcas)) {
                listaMarcaSelecionar.innerHTML = `<option class="option-analise" value="0" selected>Selecione</option>`

                marcas.forEach(p_marcas => {

                    listaMarcaSelecionar.innerHTML += `
                        <option class="option-analise" value="${p_marcas.marca_p}">${p_marcas.marca_p}</option>
                    `
                })
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function selecao_produto() {
    for (var i = 0; i < listaProdutos.length; i++) {
        if (listaProdutos[i].checked == true) {
            const marcado = listaProdutos[i].value
            if (checkProduto.indexOf(marcado) > -1) {

            } else {
                checkProduto.push(marcado)
            }

        } else if (listaProdutos[i].checked == false) {
            const desmarq = listaProdutos[i].value
            if (checkProduto.indexOf(desmarq) > -1) {
                checkProduto.splice(checkProduto.indexOf(desmarq), 1)
            }
        }
    }

    const produtos_selecionados = new FormData()
    produtos_selecionados.append('csrfmiddlewaretoken', csrf)
    produtos_selecionados.append('produto', checkProduto)


    filterProd(produtos_selecionados)
}
