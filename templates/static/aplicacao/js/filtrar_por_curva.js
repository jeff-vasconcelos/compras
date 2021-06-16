console.log("funcionando aqui")
const listaCurvaSelecionar = document.getElementById('curva_abc_select')
// const resultadosProdutos = document.getElementById('results-produtos')

const enviarSelectCurva = (curva, forn) =>{
    $.ajax({
        type: 'POST',
        url: '/painel/filter-curva/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'fornecedor': forn,
            'curva': curva
        },
        success: (res_fil_curva)=> {
            const data_f = res_fil_curva.data
            if (Array.isArray(data_f)){
                resultadosProdutos.innerHTML = `<option class="option-analise" selected>Selecione o produto</option>`
                data_f.forEach(prod=> {
                    resultadosProdutos.innerHTML += `
                        <option class="option-analise" value="${prod.pk}">${prod.cod} - ${prod.nome} ${prod.emb}</option>
                    `
                })
            }
        }
    })
}

listaCurvaSelecionar.addEventListener('change', e => {
    // PEGANDO PRODUTO SELECIONADO
    const curvaSelecionada = e.target.value

    // PRECISA AUTOMATIZAR O COD FORNECEDOR
    const fornec = 1

    enviarSelectCurva(curvaSelecionada, fornec)
})
