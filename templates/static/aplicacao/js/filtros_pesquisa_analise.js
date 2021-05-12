const itemResultsFornec = document.getElementsByName('item-fornec')
const resultFilterProd = document.getElementById('results-produtos')
var checkvaluesFornec = []


const filterFornec = (forn) =>{
    $.ajax({
        type: 'POST',
        url: '/painel/filter-fornec/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'fornecedor': forn,
        },
        success: (res_fil_fornec)=> {
            console.log(res_fil_fornec)
            const data_f = res_fil_fornec.data
            if (Array.isArray(data_f)){
                resultFilterProd.innerHTML = ""
                data_f.forEach(prod=> {
                    resultFilterProd.innerHTML += `
                        <option class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome}</option>
                    `
                })
            }
        }
    })
}

function teste(){
    for (var i = 0; i < itemResultsFornec.length; i++){
        if (itemResultsFornec[i].checked == true){
            const marcado = parseInt(itemResultsFornec[i].value)
            if (checkvaluesFornec.indexOf(marcado) > -1){

            }else{
                checkvaluesFornec.push(marcado)

            }

        }else if (itemResultsFornec[i].checked == false){
            const desmarq = parseInt(itemResultsFornec[i].value)
            if (checkvaluesFornec.indexOf(desmarq) > -1){
                checkvaluesFornec.splice(checkvaluesFornec.indexOf(desmarq), 1)

            }
        }
    }
    console.log(checkvaluesFornec)
    filterFornec(3)
}
