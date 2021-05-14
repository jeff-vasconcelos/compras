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
            console.log(res_fil_prod)
            const data_p = res_fil_prod.data
            if (Array.isArray(data_p)) {
                resultadosPProdutos.innerHTML = `<option class="option-analise" selected>Selecione o produto</option>`
                data_p.forEach(prod => {
                    resultadosPProdutos.innerHTML += `
                        <option name="option-product" class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome} ${prod.emb}</option>
                    `
                })
            }
        }
    })
}

function selecao_produto() {
    console.log('clicado')
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
    console.log(checkProduto)
    const produtos_selecionados = new FormData()
    produtos_selecionados.append('csrfmiddlewaretoken', csrf)
    produtos_selecionados.append('produto', checkProduto)


    filterProd(produtos_selecionados)
}
