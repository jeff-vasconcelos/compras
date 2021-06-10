console.log("selecao_produto")
const listaProdutosSelecionar = document.getElementById('results-produtos')
const tabelaInfo = document.getElementById('tabela-info-analise')
const tabelaPedidosPendentes = document.getElementById('pedidos-pendentes-modal')

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
            //VALIDANDO
            console.log(info_prod)
            const dados = info_prod.data

            if (dados === 0) {
                console.log("vazio")
                location.reload();
            } else {
                console.log("tem dados")

                const data = dados[0]
                const graficos = dados[1]

                //GRAFICO 01
                var ctx = document.getElementById("ChartSerieHist");
                var ChartSerieHist = new Chart(ctx, {
                    data: {
                        datasets: [{
                            type: 'line',
                            yAxisID: 'B',
                            label: 'Máximo',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            pointRadius: 0,
                            borderWidth: 2,
                            pointBackgroundColor: "#ed1b24",
                            pointBorderColor: "#ed1b24",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#ed1b24",
                            pointHoverBorderColor: "#ed1b24",
                            pointHitRadius: 4,
                            pointBorderWidth: 1,
                            borderColor: "#ed1b24",
                            data: graficos.data_max,
                        }, {
                            type: 'line',
                            yAxisID: 'B',
                            label: 'Média',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            pointRadius: 0,
                            borderWidth: 2,
                            pointBackgroundColor: "#f47a20",
                            pointBorderColor: "#f47a20",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#f47a20",
                            pointHoverBorderColor: "#f47a20",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            borderColor: "#f47a20",
                            data: graficos.data_med,
                        }, {
                            type: 'line',
                            yAxisID: 'B',
                            label: 'Minímo',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            pointRadius: 0,
                            borderWidth: 2,
                            pointBackgroundColor: "#274ea2",
                            pointBorderColor: "#274ea2",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#274ea2",
                            pointHoverBorderColor: "#274ea2",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            borderColor: "#274ea2",
                            data: graficos.data_min,
                        }, {
                            type: 'line',
                            yAxisID: 'A',
                            label: 'Preço unitário - R$',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            pointRadius: 2,
                            borderWidth: 1,
                            pointBackgroundColor: "#4c66a3",
                            pointBorderColor: "#4c66a3",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#4c66a3",
                            pointHoverBorderColor: "#4c66a3",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            borderColor: "#4c66a3",
                            data: graficos.data_preco,
                        }, {
                            type: 'line',
                            yAxisID: 'A',
                            label: 'Custo unitário - R$',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            borderColor: "#f5ea03",
                            pointRadius: 2,
                            borderWidth: 1,
                            pointBackgroundColor: "#f5ea03",
                            pointBorderColor: "#f5ea03",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#f5ea03",
                            pointHoverBorderColor: "#f5ea03",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            data: graficos.data_custo,
                        }, {
                            type: 'line',
                            yAxisID: 'A',
                            label: 'Lucro bruto - R$',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            pointRadius: 1,
                            borderWidth: 1,
                            pointBackgroundColor: "#60ba47",
                            pointBorderColor: "#60ba47",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#60ba47",
                            pointHoverBorderColor: "#60ba47",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            borderColor: "#60ba47",
                            data: graficos.data_lucro,
                        }, {
                            type: 'bar',
                            yAxisID: 'B',
                            label: 'Quantidade vendida',
                            backgroundColor: "#6acadb",
                            hoverBackgroundColor: "#6acadb",
                            borderColor: "#6acadb",
                            data: graficos.data_qtvenda
                        }],

                        labels: graficos.label_dt_serie,
                    },
                    options: {
                        maintainAspectRatio: false,
                        responsive: true,
                        layout: {
                            padding: {
                                left: 10,
                                right: 25,
                                top: 25,
                                bottom: 0
                            }
                        },
                        scales: {
                            xAxes: [{
                                time: {
                                    unit: 'day'
                                },
                                gridLines: {
                                    display: false,
                                    drawBorder: false
                                },
                                ticks: {
                                    //limite de dias da serie historica
                                    maxTicksLimit: 120,
                                    major: {
                                        enabled: true
                                    }
                                },
                                maxBarThickness: 250,
                            }],
                            yAxes: [{
                                id: 'A',
                                ticks: {
                                    min: 0,
                                    maxTicksLimit: 10,
                                    padding: 10,
                                    // Include a dollar sign in the ticks
                                    callback: function (value, index, values) {
                                        return 'R$' + number_format(value);
                                    }
                                },
                                gridLines: {
                                    color: "rgb(234, 236, 244)",
                                    zeroLineColor: "rgb(234, 236, 244)",
                                    drawBorder: false,
                                    borderDash: [2],
                                    zeroLineBorderDash: [2]
                                }
                            }, {
                                id: 'B',
                                position: 'right',
                                ticks: {
                                    min: 0,
                                    maxTicksLimit: 10,
                                    padding: 10,
                                    // Include a dollar sign in the ticks
                                    callback: function (value, index, values) {
                                        return number_format(value);
                                    }
                                },
                                gridLines: {
                                    color: "rgb(234, 236, 244)",
                                    zeroLineColor: "rgb(234, 236, 244)",
                                    drawBorder: false,
                                    borderDash: [2],
                                    zeroLineBorderDash: [2]
                                }
                            }],
                        },
                        legend: {
                            display: true
                        },
                        tooltips: {
                            titleMarginBottom: 10,
                            titleFontColor: '#6e707e',
                            titleFontSize: 16,
                            backgroundColor: "rgb(255,255,255)",
                            bodyFontColor: "#858796",
                            borderColor: '#dddfeb',
                            borderWidth: 1,
                            xPadding: 15,
                            yPadding: 15,
                            displayColors: false,
                            caretPadding: 10,
                            callbacks: {
                                label: function (tooltipItem, chart) {
                                    var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                                    return datasetLabel + ": " + number_format(tooltipItem.yLabel);
                                }
                            }
                        },
                    }
                });


                //GRAFICO 02
                var ctxdois = document.getElementById("ChartCobertura");
                var ChartCobertura = new Chart(ctxdois, {

                    data: {
                        datasets: [{
                            type: 'line',
                            label: 'Quantidade estoque',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            pointRadius: 2,
                            borderWidth: 1,
                            pointBackgroundColor: "#4c66a3",
                            pointBorderColor: "#4c66a3",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#4c66a3",
                            pointHoverBorderColor: "#4c66a3",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            borderColor: "#4c66a3",
                            data: graficos.qt_estoque,
                        }],

                        labels: graficos.label_dt_serie_est,
                    },
                    options: {
                        maintainAspectRatio: false,
                        layout: {
                            padding: {
                                left: 10,
                                right: 25,
                                top: 25,
                                bottom: 0
                            }
                        },
                        scales: {
                            xAxes: [{
                                time: {
                                    unit: 'day'
                                },
                                gridLines: {
                                    display: false,
                                    drawBorder: false
                                },
                                ticks: {
                                    maxTicksLimit: 120,
                                    major: {
                                        enabled: true
                                    }
                                },
                                maxBarThickness: 250,
                            }],
                            yAxes: [{
                                ticks: {
                                    min: 0,
                                    maxTicksLimit: 10,
                                    padding: 10,
                                    // Include a dollar sign in the ticks
                                    callback: function (value, index, values) {
                                        return number_format(value);
                                    }
                                },
                                gridLines: {
                                    color: "rgb(234, 236, 244)",
                                    zeroLineColor: "rgb(234, 236, 244)",
                                    drawBorder: false,
                                    borderDash: [2],
                                    zeroLineBorderDash: [2]
                                }
                            }],
                        },
                        legend: {
                            display: true
                        },
                        tooltips: {
                            titleMarginBottom: 10,
                            titleFontColor: '#6e707e',
                            titleFontSize: 14,
                            backgroundColor: "rgb(255,255,255)",
                            bodyFontColor: "#858796",
                            borderColor: '#dddfeb',
                            borderWidth: 1,
                            xPadding: 15,
                            yPadding: 15,
                            displayColors: false,
                            caretPadding: 10,
                            callbacks: {
                                label: function (tooltipItem, chart) {
                                    var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                                    return datasetLabel + ': ' + number_format(tooltipItem.yLabel) + ' Unidades';
                                }
                            }
                        },
                    }
                });

                //DADOS DA TABELA

                if (!data) {
                    valor_faturamento.innerHTML = ""
                    valor_curva.innerHTML = ""
                    valor_media.innerHTML = ""
                    valor_ruptura.innerHTML = ""
                    porc_ruptura.innerHTML = ""
                    tabelaInfo.innerHTML = ""
                } else {
                    valor_faturamento.innerHTML = ""
                    valor_curva.innerHTML = ""
                    valor_media.innerHTML = ""
                    valor_ruptura.innerHTML = ""
                    porc_ruptura.innerHTML = ""
                    tabelaInfo.innerHTML = ""

                    if (data.ruptura < 0) {
                        valor_ruptura.style.color = "#707070"
                    } else if (data.ruptura >= 0) {
                        valor_ruptura.style.color = "#de200d"
                    }
                    tabelaInfo.innerHTML += `
                        <td class="tabela-info">${data.filial}</td>
                        <td class="tabela-info">Matriz</td>
                        <td class="tabela-info">${data.estoque}</td>
                        <td class="tabela-info">${data.avaria}</td>
                        <td class="tabela-info">${data.saldo}</td>
                        <td class="tabela-info">${data.dt_ult_entrada}</td>
                        <td class="tabela-info">${data.qt_ult_entrada}</td>
                        <td class="tabela-info">R$ ${data.vl_ult_entrada}</td>
                        <td class="tabela-info">${data.dde}</td>
                        <td class="tabela-info">${data.est_seguranca}</td>
                        <td class="tabela-info">${data.p_reposicao}</td>
                        <td class="tabela-info">${data.sugestao_caixa}</td>
                        <td class="tabela-info">${data.sugestao_unidade}</td>
                        <td class="tabela-info">${data.sugestao}</td>
                        <td class="tabela-info">999</td>
                        <td class="tabela-info">10</td>
                    `

                    valor_faturamento.innerHTML += `
                        ${data.condicao_estoque}
                    `
                    valor_curva.innerHTML += `
                        ${data.curva}
                    `
                    valor_media.innerHTML += `
                        ${data.media_ajustada}
                    `
                    valor_ruptura.innerHTML += `
                        ${data.ruptura}
                    `
                    porc_ruptura.innerHTML += `
                        ${data.ruptura_porc} %
                    `

                }
            }

        }
    })
}

// EXECUTA AO MUDAR DE PRODUTO
listaProdutosSelecionar.addEventListener('change', e => {
    resultsBoxFornec.classList.add('d-none')
    resultsBoxProd.classList.add('d-none')

    // PEGANDO PRODUTO SELECIONADO
    const produtoSelecionado = e.target.value

    // PEGANDO LEADTIME
    const valorlead = leadtime.value
    var lead = 0
    if (valorlead === "") {
        lead = 0
    } else {
        lead = valorlead
    }

    // PEGANDO TEMPO DE REPOSIÇÃO
    const valor_treposicao = t_reposicao.value
    var t_repo = 0
    if (valor_treposicao === "") {
        t_repo = 0
    } else {
        t_repo = valor_treposicao
    }

    console.log(produtoSelecionado, "PRODUTO SELECIONADO")
    console.log(lead, "LEADTIME")
    console.log(t_repo, "TEMPO DE REPOSICAO")

    sendSelectProd(produtoSelecionado, lead, t_repo)
})

// EXECUTA AO ALTERAR LEADTIME
leadtime.addEventListener('keyup', a => {
    resultsBoxFornec.classList.add('d-none')
    resultsBoxProd.classList.add('d-none')

    // PEGANDO PRODUTO SELECIONADO

    const produtoSelecionado = listaProdutosSelecionar.value

    // PEGANDO LEADTIME
    const valorlead = leadtime.value
    var lead = 0
    if (valorlead === "") {
        lead = 0
    } else {
        lead = valorlead
    }

    // PEGANDO TEMPO DE REPOSIÇÃO
    let valor_treposicao = ""
    valor_treposicao = t_reposicao.value
    var t_repo = 0
    if (valor_treposicao === "") {
        t_repo = 0
    } else {
        t_repo = valor_treposicao
    }

    console.log(produtoSelecionado, "PRODUTO SELECIONADO")
    console.log(lead, "LEADTIME")
    console.log(t_repo, "TEMPO DE REPOSICAO")

    sendSelectProd(produtoSelecionado, lead, t_repo)
})

// EXECUTA AO ALTERAR TEMPO DE REPOSICAO
t_reposicao.addEventListener('keyup', a => {
    resultsBoxFornec.classList.add('d-none')
    resultsBoxProd.classList.add('d-none')

    // PEGANDO PRODUTO SELECIONADO

    const produtoSelecionado = listaProdutosSelecionar.value

    // PEGANDO LEADTIME
    const valorlead = leadtime.value
    var lead = 0
    if (valorlead === "") {
        lead = 0
    } else {
        lead = valorlead
    }

    // PEGANDO TEMPO DE REPOSIÇÃO
    let valor_treposicao = ""
    valor_treposicao = t_reposicao.value
    console.log(valor_treposicao)
    var t_repo = 0
    if (valor_treposicao === "") {
        t_repo = 0
    } else {
        t_repo = valor_treposicao
    }

    console.log(produtoSelecionado, "PRODUTO SELECIONADO")
    console.log(lead, "LEADTIME")
    console.log(t_repo, "TEMPO DE REPOSICAO")

    sendSelectProd(produtoSelecionado, lead, t_repo)
})

