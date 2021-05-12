const url = window.location.href
const searchFornec = document.getElementById('search-fornec')
const resultsBoxFornec = document.getElementById('results-box-fornec')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (fornec) =>{
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
                    <a href="" value="${fornec.cod}">
                        <h3>${fornec.cod} - ${fornec.nome}</h3>
                    </a>
                    `
                })
            }else{
                 if (searchFornec.value.length > 0){
                      resultsBoxFornec.innerHTML = `<b>${data}</b>`
                 }else{
                     resultsBoxFornec.classList.add('d-none')
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