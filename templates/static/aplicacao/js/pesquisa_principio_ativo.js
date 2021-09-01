const searchPrincipio = document.getElementById('search-principio')
const resultsBoxPrincipio = document.getElementById('results-box-principio')

const sendSearchPrincipio = (prod) => {
    $.ajax({
        type: 'POST',
        url: '/painel/search/principio',
        data: {
            'csrfmiddlewaretoken': csrf,
            'princ': prod,
        },
        success: (res) => {
            const data = res.data
            if (Array.isArray(data)) {
                resultsBoxPrincipio.innerHTML = ""
                data.forEach(prod => {
                    resultsBoxPrincipio.innerHTML += `
                    <input name="item-principio" class="form-check-input" type="checkbox" value="${prod.principio}" id="${prod.principio}" 
                    style="display: block" onclick="selecao_principio()   ">
                        <label style="display: block" class="form-check-label" for="${prod.principio}">
                            ${prod.principio}
                        </label>
                    `
                })
            } else {
                if (searchPrincipio.value.length > 0) {
                    resultsBoxPrincipio.innerHTML = `<b>${data}</b>`
                } else {
                    resultsBoxPrincipio.classList.add('d-none')
                    resultadosPProdutos.innerHTML = ""
                    listaMarcaSelecionar.innerHTML = ""
                    listaCurvaSelecionar.innerHTML = ""
                }
            }
        },
        error: function (error) {
            console.log(error)
        }

    })
}

searchPrincipio.addEventListener('keyup', e => {

    if (resultsBoxPrincipio.classList.contains('d-none')) {
        resultsBoxPrincipio.classList.remove('d-none')
    }

    sendSearchPrincipio(e.target.value)


})