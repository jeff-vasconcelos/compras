console.log("selecao_produto")
const listaProdutosSelecionar = document.getElementById('results-produtos')
const tabelaInfo = document.getElementById('tabela-info-analise')

//CARDS
const porc_faturamento = document.getElementById('porc_fat')
const valor_faturamento = document.getElementById('valor_fat')
const porc_curva = document.getElementById('porc_curva')
const valor_curva = document.getElementById('valor_curva')
const porc_media = document.getElementById('porc_media')
const valor_media = document.getElementById('valor_media')
const porc_ruptura = document.getElementById('porc_ruptura')
const valor_ruptura = document.getElementById('valor_ruptura')

const leadtime = document.getElementById('leadtime')
const t_reposicao = document.getElementById('tempo_reposicao')



const sendSelectProd = (prod, lead, t_repo) => {
    $.ajax({
        type: 'POST',
        url: '/painel/select-prod/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': prod,
            'leadtime': lead,
            'tempo_reposicao': t_repo
        },
        success: (info_prod) => {
            const data = info_prod.data
            if (Array.isArray(data)) {
                valor_faturamento.innerHTML = ""
                valor_curva.innerHTML = ""
                valor_media.innerHTML = ""
                valor_ruptura.innerHTML = ""

                tabelaInfo.innerHTML = ""
                data.forEach(prod => {
                    if (prod.ruptura < 0) {
                        valor_ruptura.style.color = "#ec2300"
                    } else if (prod.ruptura >= 0) {
                        valor_ruptura.style.color = "#228b22"
                    }
                    tabelaInfo.innerHTML += `
                        <td class="tabela-info">${prod.filial}</td>
                        <td class="tabela-info">Matriz</td>
                        <td class="tabela-info">${prod.estoque}</td>
                        <td class="tabela-info">${prod.avaria}</td>
                        <td class="tabela-info">${prod.saldo}</td>
                        <td class="tabela-info">${prod.dt_ult_entrada}</td>
                        <td class="tabela-info">${prod.qt_ult_entrada}</td>
                        <td class="tabela-info">R$ ${prod.vl_ult_entrada}</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">${prod.est_seguranca}</td>
                        <td class="tabela-info">${prod.p_reposicao}</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">10</td>


                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="qt_digitada">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="pr_compra">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="porc_margem">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="pr_sugerido">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="dde">
                        </td>
                    `

                    valor_faturamento.innerHTML += `
                        ${prod.valor_fatur}
                    `
                    valor_curva.innerHTML += `
                        ${prod.curva}
                    `
                    valor_media.innerHTML += `
                        ${prod.media_ajustada}
                    `
                    valor_ruptura.innerHTML += `
                        ${prod.ruptura}
                    `
                })
            }
        }
    })
}

listaProdutosSelecionar.addEventListener('change', e => {
    // PEGANDO PRODUTO SELECIONADO
    const produtoSelecionado = e.target.value

    // PEGANDO LEADTIME
    const valorlead = leadtime.value
    var lead = 0
    if (valorlead === ""){
        lead = 0
    } else {
        lead = valorlead
    }

    // PEGANDO TEMPO DE REPOSIÇÃO
    const valor_treposicao = t_reposicao.value
    var t_repo = 0
    if (valor_treposicao === ""){
        t_repo = 0
    } else {
        t_repo = valorlead
    }

    console.log(produtoSelecionado)
    console.log(lead)

    sendSelectProd(produtoSelecionado, lead, t_repo)
})

