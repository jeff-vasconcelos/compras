const searchProd = document.getElementById('search-prod')
const resultsBoxProd = document.getElementById('results-box-prod')

const sendSearchProd = (prod) =>{
    $.ajax({
        type: 'POST',
        url: '/painel/search/prod',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': prod,
        },
        success: (res)=> {
            const data = res.data
            console.log(data)
            if (Array.isArray(data)){
                resultsBoxProd.innerHTML = ""
                data.forEach(prod=> {
                    resultsBoxProd.innerHTML += `
                    <input name="item-produto" class="form-check-input" type="checkbox" value="${prod.pk}" id="${prod.pk}" 
                    style="display: block" onclick="selecao_produto()   ">
                        <label style="display: block" class="form-check-label" for="${prod.pk}">
                            ${prod.cod} - ${prod.nome} ${prod.emb}
                        </label>
                    `
                })
            }else{
                 if (searchProd.value.length > 0){
                      resultsBoxProd.innerHTML = `<b>${data}</b>`
                 }else{
                     resultsBoxProd.classList.add('d-none')
                     resultadosPProdutos.innerHTML = ""
                     listaMarcaSelecionar.innerHTML = ""
                 }
            }
        },
        error: (err)=> {
            console.log(err)
        }

    })
}

searchProd.addEventListener('keyup', e=>{

    if (resultsBoxProd.classList.contains('d-none')){
        resultsBoxProd.classList.remove('d-none')
    }

    sendSearchProd(e.target.value)


})