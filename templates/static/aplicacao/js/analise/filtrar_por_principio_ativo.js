const listaPrincipio = document.getElementsByName('item-principio')
// const listaProdutosSelecionar = document.getElementById('results-principio')
const checkPrincipio = []


const filterPrincipio = (prod) => {
    $.ajax({
        type: 'POST',
        url: '/painel/filter-principio/',
        data: prod,
        processData: false,
        contentType: false,
        success: (res_fil_prod) => {
            const data = res_fil_prod.data

            const data_p = data[0]
            const marcas = data[1]

            if (Array.isArray(data_p)) {
                listaProdutosSelecionar.innerHTML = `<option class="option-analise" value="0" selected>Selecione o produto</option>`
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
                    listaProdutosSelecionar.innerHTML += `
                        <option name="option-product" class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome}</option>
                    `
                })
            }
            if (Array.isArray(marcas)) {
                listaMarcaSelecionar.innerHTML = `<option class="option-analise" value="0" selected>Selecione</option>`

                marcas.forEach(p_marcas => {

                    listaMarcaSelecionar.innerHTML += `
                        <option class="option-analise" value="${p_marcas.marca_p}">${p_marcas.marca_p_desc}</option>
                    `
                })
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
}

function selecao_principio() {
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

    const principio_selecionados = new FormData()
    principio_selecionados.append('csrfmiddlewaretoken', csrf)
    principio_selecionados.append('principio', checkPrincipio)

    filterPrincipio(principio_selecionados)
}
