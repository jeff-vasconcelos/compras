const url = window.location.href
const searchFornec = document.getElementById('search-fornec')
const resultsBoxFornec = document.getElementById('results-box-fornec')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (fornec) =>{
    console.log(fornec)
    $.ajax({
        type: 'POST',
        url: '/painel/search/fornec',
        data: {
            'csrfmiddlewaretoken': csrf,
            'fornecedor': fornec,
        },
        success: (res_f)=> {
            console.log(res_f.data)
            const data = res_f.data
            if (Array.isArray(data)){
                resultsBoxFornec.innerHTML = ""
                data.forEach(fornec=> {
                    resultsBoxFornec.innerHTML += `
                    <input name="item-fornecedor" class="form-check-input" type="checkbox" value="${fornec.pk}" id="${fornec.pk}" 
                    style="display: block" onclick="selecao_fornecedor()">
                        <label style="display: block" class="form-check-label" for="${fornec.pk}">
                            ${fornec.cod} - ${fornec.nome}
                        </label>
                    `
                })
            }else{
                 if (searchFornec.value.length > 0){
                      resultsBoxFornec.innerHTML = `<b>${data}</b>`
                 }else{
                     resultsBoxFornec.classList.add('d-none')
                     resultadosPProdutos.innerHTML = ""
                 }
            }
        },
        error: (err)=> {
            console.log(err)
        }

    })
}

searchFornec.addEventListener('keyup', e=>{
    console.log(e.target.value)

    if (resultsBoxFornec.classList.contains('d-none')){
        resultsBoxFornec.classList.remove('d-none')
    }

    sendSearchData(e.target.value)


})