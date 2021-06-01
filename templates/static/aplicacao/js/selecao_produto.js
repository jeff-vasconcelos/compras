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


const sendSelectProd = (prod) => {
    $.ajax({
        type: 'POST',
        url: '/painel/select-prod/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': prod
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
                    tabelaInfo.innerHTML += `
                        <td class="tabela-info">${prod.filial}</td>
                        <td class="tabela-info">Matriz</td>
                        <td class="tabela-info">32000</td>
                        <td class="tabela-info">9999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">999</td>
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
    const produtoSelecionado = e.target.value
    console.log(produtoSelecionado)

    sendSelectProd(produtoSelecionado)
})

