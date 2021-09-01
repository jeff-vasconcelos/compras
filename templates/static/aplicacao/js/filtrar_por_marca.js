const listaMarcaSelecionar = document.getElementById('filtro_marca')

const enviarSelectMarca = (marca) => {
    $.ajax({
        type: 'POST',
        url: '/painel/filter-marca/',
        data: marca,
        processData: false,
        contentType: false,
        success: (res_fil_marca) => {
            const data_m = res_fil_marca.data
            if (Array.isArray(data_m)) {
                resultadosProdutos.innerHTML = `<option class="option-analise" value="0" selected>Selecione o produto</option>`
                data_m.forEach(prod => {
                    resultadosProdutos.innerHTML += `
                        <option class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome}</option>
                    `
                })
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}

listaMarcaSelecionar.addEventListener('change', e => {
    // PEGANDO PRODUTO SELECIONADO
    const marcaSelecionada = e.target.value
    // const curvaSelecionada = listaCurvaSelecionar.value

    for (var i = 0; i < listaFornecedores.length; i++) {
        if (listaFornecedores[i].checked == true) {
            const marcado = listaFornecedores[i].value
            if (checkFornecedor.indexOf(marcado) > -1) {

            } else {
                checkFornecedor.push(marcado)
            }

        } else if (listaFornecedores[i].checked == false) {
            const desmarq = listaFornecedores[i].value
            if (checkFornecedor.indexOf(desmarq) > -1) {
                checkFornecedor.splice(checkFornecedor.indexOf(desmarq), 1)
            }
        }
    }

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

    for (var i = 0; i < listaPrincipio.length; i++) {
        if (listaPrincipio[i].checked == true) {
            const marcado = listaPrincipio[i].value

            if (checkPrincipio.indexOf(marcado) > -1) {

            } else {
                checkPrincipio.push(marcado)
            }

        } else if (listaPrincipio[i].checked == false) {
            const desmarq = listaPrincipio[i].value

            if (checkPrincipio.indexOf(desmarq) > -1) {
                checkPrincipio.splice(checkPrincipio.indexOf(desmarq), 1)
            }
        }
    }

    const marca_selecionada = new FormData()
    marca_selecionada.append('csrfmiddlewaretoken', csrf)
    marca_selecionada.append('fornecedor', checkFornecedor)
    marca_selecionada.append('produto', checkProduto)
    marca_selecionada.append('principio', checkPrincipio)
    marca_selecionada.append('marca', marcaSelecionada)
    // marca_selecionada.append('curva', curvaSelecionada)

    enviarSelectMarca(marca_selecionada)
})
