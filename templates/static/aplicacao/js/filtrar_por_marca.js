
const listaMarcaSelecionar = document.getElementById('filtro_marca')

const enviarSelectMarca = (marca) =>{
    $.ajax({
        type: 'POST',
        url: '/painel/filter-marca/',
        data: marca,
        processData: false,
        contentType: false,
        success: (res_fil_marca)=> {
            const data_m = res_fil_marca.data
            if (Array.isArray(data_m)){
                resultadosProdutos.innerHTML = `<option class="option-analise" value="0" selected>Selecione o produto</option>`
                data_m.forEach(prod=> {
                    resultadosProdutos.innerHTML += `
                        <option class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome}</option>
                    `
                })
            }
        }
    })
}

listaMarcaSelecionar.addEventListener('change', e => {
    // PEGANDO PRODUTO SELECIONADO
    const marcaSelecionada = e.target.value

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

    const marca_selecionada = new FormData()
    marca_selecionada.append('csrfmiddlewaretoken', csrf)
    marca_selecionada.append('fornecedor', checkFornecedor)
    marca_selecionada.append('marca', marcaSelecionada)

    enviarSelectMarca(marca_selecionada)
})
