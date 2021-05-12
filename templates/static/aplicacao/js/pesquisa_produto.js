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
            console.log(res.data)
            const data = res.data
            if (Array.isArray(data)){
                resultsBoxProd.innerHTML = ""
                data.forEach(prod=> {
                    resultsBoxProd.innerHTML += `
                    <a href="">
                        <div class="row">
                            <div class="col">
                                <h3>${prod.cod} - ${prod.nome}</h3>
                            </div>
                        </div>
                    </a>
                    `
                })
            }else{
                 if (searchProd.value.length > 0){
                      resultsBoxProd.innerHTML = `<b>${data}</b>`
                 }else{
                     resultsBoxProd.classList.add('d-none')
                 }
            }
        },
        error: (err)=> {
            console.log(err)
        }

    })
}

searchProd.addEventListener('keyup', e=>{
    console.log(e.target.value)

    if (resultsBoxProd.classList.contains('d-none')){
        resultsBoxProd.classList.remove('d-none')
    }

    sendSearchProd(e.target.value)


})