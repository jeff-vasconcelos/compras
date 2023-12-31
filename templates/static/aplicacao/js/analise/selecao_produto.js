//TOTAIS
const th_tabela_totais = document.getElementById('th_tabela_totais')
const td_tabela_totais = document.getElementById('td_tabela_totais')
const titulo_vendasxmes = document.getElementById('titulo_vendasxmes')

// INPUT DE MEDIA PARA DDE
const input_analise_media = document.getElementById('input_analise_media')

const productSelect = document.getElementById('results-produtos')
const listaFiliais = document.getElementById('filtro-filial')
const tabelaInfo = document.getElementById('body-tabela-analise')
const tabelaPedidosPendentes = document.getElementById('pedidos-pendentes-modal')

//CARDS
const porc_faturamento = document.getElementById('porc_fat')
const valor_condicao_est = document.getElementById('valor_fat')
const porc_curva = document.getElementById('porc_curva')
const valor_curva = document.getElementById('valor_curva')
const porc_media = document.getElementById('porc_media')
const valor_media = document.getElementById('valor_media')
const valor_media_simples = document.getElementById('valor_media_simples')
const porc_ruptura = document.getElementById('porc_ruptura')
const valor_ruptura = document.getElementById('valor_ruptura')

const leadtimeInput = document.getElementById('leadtime')
const replenishmentTimeInput = document.getElementById('tempo_reposicao')

const area_graf_um = document.getElementById('div-grafico-um')
const area_graf_dois = document.getElementById('div-grafico-dois')

function OnProductChange(event){

    resultsBoxFornec.classList.add('d-none')
    resultsBoxProd.classList.add('d-none')
    resultsBoxPrincipio.classList.add('d-none')

    const selectedProduct = event.target.value
    const selectedBranch = listaFiliais.value
    const selectedLeadTime = leadtimeInput.value
    const selectedReplenishmentTime = replenishmentTimeInput.value

    if (selectedProduct == 0){
        return
    }

    let lead = selectedLeadTime === "" ? 0 : selectedLeadTime
    let replenishmentTime = replenishmentTimeInput.value === "" ? 0 : selectedReplenishmentTime

    sendSelectedProduct(selectedBranch, selectedProduct, lead, replenishmentTime)
}

async function getDefaultAnalisisParameters(product){

    return $.ajax({
        type: 'POST',
        url: '/painel/get-product-parameters/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'product': product,
        },
        success: function(parameters) {
            return parameters
        },
        error: function (error) {
            console.log(error)
        }
    })
}

async function setDefaultAnalisisParameters(event){

    resultsBoxFornec.classList.add('d-none')
    resultsBoxProd.classList.add('d-none')
    resultsBoxPrincipio.classList.add('d-none')

    const selectedProduct = event.target.value

    parameters = await getDefaultAnalisisParameters(selectedProduct)

    leadtimeInput.value = parameters.leadTime
    replenishmentTimeInput.value = parameters.replenishmentTime


}

const sendSelectedProduct = (codFilial, product, lead, replenishmentTime) => {

    $.ajax({
        type: 'POST',
        url: '/painel/select-prod/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'filial': codFilial,
            'produto': product,
            'leadtime': lead,
            'tempo_reposicao': replenishmentTime
        },
        success: (info_prod) => {

            const dados = info_prod.data

            if (dados[0] === 0) {

                // $("canvas#ChartSerieHist").remove();
                // $("canvas#ChartCobertura").remove();
                // $("div#div-grafico-um").append('<canvas id="ChartSerieHist"></canvas>')
                // $("div#div-grafico-dois").append('<canvas id="ChartCobertura"></canvas>')

                botaoVerPedidosPendentes.style.display = 'none'
                titulo_vendasxmes.style.display = 'none'
                valor_condicao_est.innerHTML = "-"
                valor_curva.innerHTML = "-"
                // valor_media.innerHTML = "-"
                valor_ruptura.innerHTML = "-"
                porc_ruptura.innerHTML = "-"
                th_tabela_totais.innerHTML = ""
                td_tabela_totais.innerHTML = ""
                tabelaInfo.innerHTML = "-"
                tabelaInfo.innerHTML = `
                        <tr>
                            <th class="tabela-info">Cód. Filial</th>
                            <th class="tabela-info">Estoque</th>
                            <th class="tabela-info">Bloqueado</th>
                            <th class="tabela-info">Avaria</th>
                            <th class="tabela-info">Ped. pendente</th>
                            <th class="tabela-info">Dt. ult. Ent.</th>
                            <th class="tabela-info">Qt. ult. Ent.</th>
                            <th class="tabela-info">Vl. ult. Ent.</th>
                            <th class="tabela-info">Embal.</th>
                            <th class="tabela-info">Qt. Cx</th>
                            <th class="tabela-info">DDE</th>
                            <th class="tabela-info">Est. seg.</th>
                            <th class="tabela-info">Ponto rep.</th>
                            <th class="tabela-info">Cx Fech.</th>
                            <th class="tabela-info">Und Caixa</th>
                            <th class="tabela-info">Sugestão Und</th>
                            <!--<th class="tabela-info">Pr. tabela</th>-->
                            <!--<th class="tabela-info">Margem</th>-->
                            <!--<th>Qt digitada</th>-->
                            <!--<th>Pr. compra</th>-->
                            <!--<th>% margem</th>-->
                            <!--<th>Pr. sugerido</th>-->
                            <!--<th>DDE</th>-->
                        </tr>
                    `
                // porc_media.innerHTML = "-"
                valor_media_simples.innerHTML = "-"

                mensagemErro.innerHTML += `
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
                            <use xlink:href="#exclamation-triangle-fill"/>
                        </svg>
                        <div>
                            &nbsp; O produto pode não ter <b>vendas no periodo</b> ou os <b>parametros do fornecedor</b> não foram definidos!
                        </div>
                    </div>
                `
                $(document).ready(function () {
                    // show the alert
                    setTimeout(function () {
                        $(".alert").alert('close');
                    }, 6000);
                });

            } else if (dados[0] === 1) {
                const mensagem_erro = dados[1]

                // $("canvas#ChartSerieHist").remove();
                // $("canvas#ChartCobertura").remove();
                // $("div#div-grafico-um").append('<canvas id="ChartSerieHist"></canvas>')
                // $("div#div-grafico-dois").append('<canvas id="ChartCobertura"></canvas>')

                botaoVerPedidosPendentes.style.display = 'none'
                titulo_vendasxmes.style.display = 'none'
                valor_condicao_est.innerHTML = "-"
                valor_curva.innerHTML = "-"
                // valor_media.innerHTML = "-"
                valor_ruptura.innerHTML = "-"
                porc_ruptura.innerHTML = "-"
                th_tabela_totais.innerHTML = ""
                td_tabela_totais.innerHTML = ""
                tabelaInfo.innerHTML = "-"
                tabelaInfo.innerHTML = `
                        <tr>
                            <th class="tabela-info">Cód. Filial</th>
                            <th class="tabela-info">Estoque</th>
                            <th class="tabela-info">Bloqueado</th>
                            <th class="tabela-info">Avaria</th>
                            <th class="tabela-info">Ped. pendente</th>
                            <th class="tabela-info">Dt. ult. Ent.</th>
                            <th class="tabela-info">Qt. ult. Ent.</th>
                            <th class="tabela-info">Vl. ult. Ent.</th>
                            <th class="tabela-info">Embal.</th>
                            <th class="tabela-info">Qt. Cx</th>
                            <th class="tabela-info">DDE</th>
                            <th class="tabela-info">Est. seg.</th>
                            <th class="tabela-info">Ponto rep.</th>
                            <th class="tabela-info">Cx Fech.</th>
                            <th class="tabela-info">Und Caixa</th>
                            <th class="tabela-info">Sugestão Und</th>
                            <!--<th class="tabela-info">Pr. tabela</th>-->
                            <!--<th>Qt digitada</th>-->
                            <!--<th class="tabela-info">Margem</th>-->
                            <!--<th>Pr. compra</th>-->
                            <!--<th>% margem</th>-->
                            <!--<th>Pr. sugerido</th>-->
                            <!--<th>DDE</th>-->
                        </tr>
                    `
                // porc_media.innerHTML = "-"
                valor_media_simples.innerHTML = "-"

                mensagemErro.innerHTML += `
                    <div class="alert alert-danger d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
                            <use xlink:href="#exclamation-triangle-fill"/>
                        </svg>
                        <div>
                            &nbsp; Não é possivel analisar o produto! &nbsp; "${mensagem_erro}"
                            
                        </div>
                    </div>
                `
                $(document).ready(function () {
                    // show the alert
                    setTimeout(function () {
                        $(".alert").alert('close');
                    }, 6000);
                });

            } else {

                const data = dados[0]
                const graficos = dados[1]
                const informacoes = dados[2]
                const totais = dados[3]

                if (graficos.periodo <= 60) {
                    area_graf_um.style.width = "auto";
                    area_graf_dois.style.width = "auto";
                } else if (graficos.periodo > 60) {
                    area_graf_um.style.width = "2000px";
                    area_graf_dois.style.width = "2000px";
                }

                $("canvas#ChartSerieHist").remove();
                $("canvas#ChartCobertura").remove();
                $("div#div-grafico-um").append('<canvas id="ChartSerieHist"></canvas>')
                $("div#div-grafico-dois").append('<canvas id="ChartCobertura"></canvas>')

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
                            borderWidth: 1,
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
                            pointBackgroundColor: "#FF6384",
                            pointBorderColor: "#FF6384",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#FF6384",
                            pointHoverBorderColor: "#FF6384",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            borderColor: "#FF6384",
                            data: graficos.data_min,
                        }, {
                            type: 'line',
                            yAxisID: 'A',
                            label: 'Preço unitário - R$',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            pointRadius: 2,
                            borderWidth: 1,
                            pointBackgroundColor: "#2F6E36",
                            pointBorderColor: "#2F6E36",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#2F6E36",
                            pointHoverBorderColor: "#2F6E36",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            borderColor: "#2F6E36",
                            data: graficos.data_preco,
                        }, {
                            type: 'line',
                            yAxisID: 'A',
                            label: 'Custo unitário - R$',
                            lineTension: 0,
                            backgroundColor: "rgba(255, 255, 255, 0.05)",
                            borderColor: "#707070",
                            pointRadius: 2,
                            borderWidth: 1,
                            pointBackgroundColor: "#707070",
                            pointBorderColor: "#707070",
                            pointHoverRadius: 5,
                            pointHoverBackgroundColor: "#707070",
                            pointHoverBorderColor: "#707070",
                            pointHitRadius: 10,
                            pointBorderWidth: 2,
                            data: graficos.data_custo,
                        }, {
                            type: 'bar',
                            yAxisID: 'B',
                            label: 'Quantidade vendida',
                            backgroundColor: "#36A2EB",
                            hoverBackgroundColor: "#36A2EB",
                            borderColor: "#36A2EB",
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
                                    maxTicksLimit: graficos.periodo,
                                    major: {
                                        enabled: true
                                    }
                                },
                                // maxBarThickness: 250,
                            }],
                            yAxes: [{
                                id: 'A',
                                ticks: {
                                    min: 0,
                                    maxTicksLimit: 10,
                                    padding: 10,
                                    // Include a dollar sign in the ticks
                                    callback: function (value, index, values) {
                                        return 'R$' + value;
                                    }
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
                                        return value;
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
                            display: true,
                            labels: {
                                usePointStyle: true,
                            }
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
                            // callbacks: {
                            //     label: function (tooltipItem, chart) {
                            //         var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                            //         return datasetLabel + ": " + tooltipItem.yLabel.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                            //     }
                            // },
                            // callbacks: {
                            //     label: function (tooltipItem, chart) {
                            //         var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                            //         return datasetLabel + ": " + number_format(tooltipItem.yLabel);
                            //     }
                            // }
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
                                    maxTicksLimit: graficos.periodo,
                                    major: {
                                        enabled: true
                                    }
                                },
                                // maxBarThickness: 250,
                            }],
                            yAxes: [{
                                ticks: {
                                    min: 0,
                                    maxTicksLimit: 10,
                                    padding: 10,
                                    // Include a dollar sign in the ticks
                                    callback: function (value, index, values) {
                                        return value;
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
                            display: true,
                            labels: {
                                usePointStyle: true,
                            }
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
                                    return datasetLabel + ': ' + tooltipItem.yLabel + ' Unidades';
                                }
                            }
                        },
                    }
                });

                //DADOS DA TABELA

                if (!data) {
                    botaoVerPedidosPendentes.style.display = 'none'
                    titulo_vendasxmes.style.display = 'none'
                    valor_condicao_est.innerHTML = "-"
                    valor_curva.innerHTML = "-"
                    // valor_media.innerHTML = "-"
                    valor_ruptura.innerHTML = "-"
                    porc_ruptura.innerHTML = "-"
                    th_tabela_totais.innerHTML = ""
                    td_tabela_totais.innerHTML = ""
                    tabelaInfo.innerHTML = "-"
                    tabelaInfo.innerHTML = `
                        <tr>
                                <th class="tabela-info">Filial</th>
                                <th class="tabela-info">Est.</th>
                                <th class="tabela-info">Bloq.</th>
                                <th class="tabela-info">Avaria</th>
                                <th class="tabela-info">Ped. pend.</th>
                                <th class="tabela-info">Ult. Ent.</th>
                                <th class="tabela-info">Qt. ult. Ent.</th>
                                <th class="tabela-info">$ ult. Ent.</th>
                                <th class="tabela-info">Embal.</th>
                                <th class="tabela-info">Qt. Cx</th>
                                <th class="tabela-info">DDE</th>
                                <th class="tabela-info">Est. seg.</th>
                                <th class="tabela-info">P. rep.</th>
                                <th class="tabela-info">Cx Fech.</th>
                                <th class="tabela-info">Und Caixa</th>
                                <th class="tabela-info">Sugest. Und</th>
                                <th class="tabela-info">Excesso</th>
<!--                            <th class="tabela-info">Pr. tabela</th>-->
<!--                            <th class="tabela-info">Margem</th>-->
                            <!--                                <th>Qt digitada</th>-->
                            <!--                                <th>Pr. compra</th>-->
                            <!--                                <th>% margem</th>-->
                            <!--                                <th>Pr. sugerido</th>-->
                            <!--                                <th>DDE</th>-->

                        </tr>
                    `
                    // porc_media.innerHTML = "-"
                    valor_media_simples.innerHTML = "-"
                } else {
                    botaoVerPedidosPendentes.style.display = "initial"
                    titulo_vendasxmes.style.display = "initial"
                    valor_condicao_est.innerHTML = ""
                    valor_curva.innerHTML = ""
                    // valor_media.innerHTML = ""
                    valor_ruptura.innerHTML = ""
                    porc_ruptura.innerHTML = ""
                    tabelaInfo.innerHTML = ""
                    th_tabela_totais.innerHTML = ""
                    td_tabela_totais.innerHTML = ""
                    tabelaInfo.innerHTML = `
                        <tr>
                                <th class="tabela-info">Filial</th>
                                <th class="tabela-info">Est.</th>
                                <th class="tabela-info">Bloq.</th>
                                <th class="tabela-info">Avaria</th>
                                <th class="tabela-info">Ped. pend.</th>
                                <th class="tabela-info">Ult. Ent.</th>
                                <th class="tabela-info">Qt. ult. Ent.</th>
                                <th class="tabela-info">$ ult. Ent.</th>
                                <th class="tabela-info">Embal.</th>
                                <th class="tabela-info">Qt. Cx</th>
                                <th class="tabela-info">DDE</th>
                                <th class="tabela-info">Est. seg.</th>
                                <th class="tabela-info">P. rep.</th>
                                <th class="tabela-info">Cx Fech.</th>
                                <th class="tabela-info">Und Caixa</th>
                                <th class="tabela-info">Sugest. Und</th>
                                <th class="tabela-info">Excesso</th>
<!--                            <th class="tabela-info">Pr. tabela</th>-->
<!--                            <th class="tabela-info">Margem</th>-->
                            <!--                                <th>Qt digitada</th>-->
                            <!--                                <th>Pr. compra</th>-->
                            <!--                                <th>% margem</th>-->
                            <!--                                <th>Pr. sugerido</th>-->
                            <!--                                <th>DDE</th>-->

                        </tr>
                    `
                    // porc_media.innerHTML = ""
                    valor_media_simples.innerHTML = ""

                    // VALIDANDO COR DA RUPTURA
                    if (informacoes.ruptura_cor === 'positivo') {
                        valor_ruptura.style.color = "#707070"
                    } else if (informacoes.ruptura_cor === 'negativo') {
                        valor_ruptura.style.color = "#de200d"
                    }

                    // VALIDANDO COR DA SITUAÇÃO ESTOQUE
                    if (informacoes.condicao_estoque === 'NORMAL') {
                        valor_condicao_est.style.color = "#707070"
                    } else if (informacoes.condicao_estoque === 'PARCIAL') {
                        valor_condicao_est.style.color = "#ff8518"
                    } else if (informacoes.condicao_estoque === 'RUPTURA') {
                        valor_condicao_est.style.color = "#de200d"
                    }

                    // VALIDANDO COR DA CURVA
                    if (informacoes.curva === 'A') {
                        valor_curva.style.color = "#3B8A44"
                    } else if (informacoes.curva === 'B') {
                        valor_curva.style.color = "#0576E0"
                    } else if (informacoes.curva === 'C') {
                        valor_curva.style.color = "#FFA500"
                    } else if (informacoes.curva === 'D') {
                        valor_curva.style.color = "#a3a0fb"
                    } else if (informacoes.curva === 'E') {
                        valor_curva.style.color = "#ec6666"
                    }


                    if (Array.isArray(data)) {
                        data.forEach(produto_info => {
                            tabelaInfo.innerHTML += `
                        
                            <td class="tabela-info">${produto_info.filial}</td>
                            <td class="tabela-info">${produto_info.estoque}</td>
                            <td class="tabela-info">${produto_info.qt_bloqueada}</td>
                            <td class="tabela-info">${produto_info.avaria}</td>
                            <td class="tabela-info">${produto_info.saldo}</td>
                            <td class="tabela-info">${produto_info.dt_ult_entrada}</td>
                            <td class="tabela-info">${produto_info.qt_ult_entrada}</td>
                            <td class="tabela-info">R$ ${produto_info.vl_ult_entrada}</td>
                            <td class="tabela-info">${produto_info.embalagem}</td>
                            <td class="tabela-info">${produto_info.quantidade_caixa}</td>
                            <td class="tabela-info">${produto_info.dde}</td>
                            <td class="tabela-info">${produto_info.est_seguranca}</td>
                            <td class="tabela-info">${produto_info.p_reposicao}</td>
                            <td class="tabela-info">${produto_info.sugestao_caixa}</td>
                            <td class="tabela-info">${produto_info.sugestao_unidade}</td>
                            <td class="tabela-info">${produto_info.sugestao}</td>
                            <td class="tabela-info">${produto_info.qt_excesso}</td>
                                              
                            `
                            //     <td
                            // className = "tabela-info" > R$ ${produto_info.preco_tabela} < /td>
                            // <td className="tabela-info">${produto_info.margem} %</td>
                        })
                    }

                    if (Array.isArray(totais)) {
                        totais.forEach(t_mes => {
                            th_tabela_totais.innerHTML += `
                            <th class="th_totais">${t_mes.mes} de ${t_mes.ano}</th>

                            `

                            td_tabela_totais.innerHTML += `
                            <td class="td_totais">${t_mes.quantidade}</td>
                            
                            `
                        })
                    }


                    valor_condicao_est.innerHTML += `
                        ${informacoes.condicao_estoque}
                    `
                    valor_curva.innerHTML += `
                        ${informacoes.curva}
                    `
                    // valor_media.innerHTML += `
                    //     ${informacoes.media_ajustada}
                    // `
                    valor_media_simples.innerHTML += `
                        ${informacoes.media_simples}
                    `
                    // porc_media.innerHTML += `
                    //     ${informacoes.porc_media} %
                    // `
                    valor_ruptura.innerHTML += `
                        ${informacoes.ruptura}
                    `
                    porc_ruptura.innerHTML += `
                        ${informacoes.ruptura_porc} %
                    `
                    // console.log(informacoes.media_simples)
                    input_analise_media.value = informacoes.media_simples

                }
            }

        },
        error: function (error) {
            console.log(error)
        }
    })
}

function calculaDDEAnalise() {
    let input_qt_digitada = document.getElementById("qt_digit");
    let input_media = document.getElementById("input_analise_media");
    let input_dde = document.getElementById("input_analise_dde");

    if (input_media.value !== '' && input_qt_digitada.value !== '') {
        let media = parseFloat(input_media.value)
        let qt_digitada = parseFloat(input_qt_digitada.value)

        input_dde.value = Math.round(qt_digitada / media)
    } else {
        input_dde.value = 0
    }
}


productSelect.addEventListener('change', event => {
    setDefaultAnalisisParameters(event)
    OnProductChange(event)
})

listaFiliais.addEventListener('change', event => {
    OnProductChange(event)
})

leadtimeInput.addEventListener('keyup', event => {
    OnProductChange(event)
})

replenishmentTimeInput.addEventListener('keyup', event => {
    OnProductChange(event)
})

