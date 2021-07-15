console.log("funcionando aqui")
const listaCurvaSelecionar = document.getElementById('curva_abc_select')

const enviarSelectCurva = (curva) =>{
    $.ajax({
        type: 'POST',
        url: '/painel/filter-curva/',
        data: curva,
        processData: false,
        contentType: false,
        success: (res_fil_curva)=> {
            const data_f = res_fil_curva.data

            if (data_f === "FALSE") {
                resultadosProdutos.innerHTML = `<option class="option-analise" value="0" selected>Selecione o produto</option>`
                mensagemErro.innerHTML += `
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
                            <use xlink:href="#exclamation-triangle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Não há produtos que correspondem a curva selecionada!
                        </div>
                    </div>
                `
                $(document).ready(function () {
                    // show the alert
                    setTimeout(function () {
                        $(".alert").alert('close');
                    }, 5000);
                });
            } else {
                if (Array.isArray(data_f)) {
                    resultadosProdutos.innerHTML = `<option class="option-analise" value="0" selected>Selecione o produto</option>`
                    data_f.forEach(prod => {
                        resultadosProdutos.innerHTML += `
                        <option class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome} ${prod.emb}</option>
                    `
                    })
                }
            }
        }
    })
}

listaCurvaSelecionar.addEventListener('change', e => {
    // PEGANDO PRODUTO SELECIONADO
    const curvaSelecionada = e.target.value

    resultsBoxFornec.classList.add('d-none')
    resultsBoxProd.classList.add('d-none')

    // PEGANDO COD FORNECEDOR
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

    console.log(checkFornecedor)
    console.log(checkProduto)

    const curva_selecionada = new FormData()
    curva_selecionada.append('csrfmiddlewaretoken', csrf)
    curva_selecionada.append('fornecedor', checkFornecedor)
    curva_selecionada.append('produto', checkProduto)
    curva_selecionada.append('curva', curvaSelecionada)

    enviarSelectCurva(curva_selecionada)
})
