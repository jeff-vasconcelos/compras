const listaFornecedores = document.getElementsByName('item-fornecedor')

const resultadosProdutos = document.getElementById('results-produtos')
const checkFornecedor = []


const filterFornec = (forn) =>{
    $.ajax({
        type: 'POST',
        url: '/painel/filter-fornec/',
        data: forn,
        processData: false,
        contentType: false,
        success: (res_fil_fornec)=> {
            console.log(res_fil_fornec)
            const data = res_fil_fornec.data

            const data_f = data[0]
            const marcas = data[1]

            if (Array.isArray(data_f)){
                resultadosProdutos.innerHTML = `<option class="option-analise" value="0" selected>Selecione o produto</option>`
                data_f.forEach(prod=> {
                    resultadosProdutos.innerHTML += `
                        <option class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome} ${prod.emb}</option>
                    `
                })
            }
            if (Array.isArray(marcas)){
                listaMarcaSelecionar.innerHTML = `<option class="option-analise" value="0" selected>Selecione</option>`

                marcas.forEach(p_marcas=> {

                    listaMarcaSelecionar.innerHTML += `
                        <option class="option-analise" value="${p_marcas.marca_p}">${p_marcas.marca_p}</option>
                    `
                })
            }
        }
    })
}

function selecao_fornecedor(){
    for (var i = 0; i < listaFornecedores.length; i++){
        if (listaFornecedores[i].checked == true){
            const marcado = listaFornecedores[i].value
            if (checkFornecedor.indexOf(marcado) > -1){

            }else{
                checkFornecedor.push(marcado)
            }

        }else if (listaFornecedores[i].checked == false){
            const desmarq = listaFornecedores[i].value
            if (checkFornecedor.indexOf(desmarq) > -1){
                checkFornecedor.splice(checkFornecedor.indexOf(desmarq), 1)
            }
        }
    }

    const fornecedores_selecionados = new FormData()
    fornecedores_selecionados.append('csrfmiddlewaretoken', csrf)
    fornecedores_selecionados.append('fornecedor', checkFornecedor)

    filterFornec(fornecedores_selecionados)
}
