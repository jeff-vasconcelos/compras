console.log("selecao_produto")
const listaProdutosSelecionar = document.getElementById('results-produtos')
const tabelaInfo = document.getElementById('tabela-info-analise')


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
                        <td class="tabela-info">999</td>


                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="">
                        </td>
                        <td class="tabela-form">
                            <input class="input-tabela-analise" name="">
                        </td>
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

