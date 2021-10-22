const area_graf_um_fornec_excesso = document.getElementById('div-grafico-umFornecExcesso')
const area_graf_dois_fornec_excesso = document.getElementById('div-grafico-doisFornecExcesso')

const th_tabela_totais_excesso_fornec = document.getElementById('th_tabela_totais_excesso_fornec')
const td_tabela_totais_excesso_fornec = document.getElementById('td_tabela_totais_excesso_fornec')
const titulo_vendasxmes_excesso_fornec = document.getElementById('titulo_vendasxmes_excesso_fornec')


function GetNome_grafico_excesso(CodProd) {

    const filial_excesso_fornec = document.getElementById('input_excesso_fornec_filial_' + CodProd)
    const produtos_excesso_fornec = document.getElementById('input_excesso_fornec_idproduto_' + CodProd)

    const produto = produtos_excesso_fornec.value
    const filial = filial_excesso_fornec.value

    graficoExcesso(filial, produto)
}


const graficoExcesso = (filial, produto) => {
    $.ajax({
        type: 'POST',
        url: '/painel/request/fornecedor/graf/',
        data: {
            'csrfmiddlewaretoken': csrf_,
            'filial': filial,
            'produto': produto,
        },
        success: (response) => {
            const dados = response.data
            const graficos = dados[0]
            const totais = dados[1]


            if (graficos.periodo <= 60) {
                area_graf_um_fornec_excesso.style.width = "auto";
                area_graf_dois_fornec_excesso.style.width = "auto";
            } else if (graficos.periodo > 60) {
                area_graf_um_fornec_excesso.style.width = "2000px";
                area_graf_dois_fornec_excesso.style.width = "2000px";
            }

            $("canvas#ChartSerieHistFornecExcesso").remove();
            $("canvas#ChartCoberturaFornecExcesso").remove();
            $("div#div-grafico-umFornecExcesso").append('<canvas id="ChartSerieHistFornecExcesso"></canvas>')
            $("div#div-grafico-doisFornecExcesso").append('<canvas id="ChartCoberturaFornecExcesso"></canvas>')

            //GRAFICO 01
            var ctxFornecExcesso = document.getElementById("ChartSerieHistFornecExcesso");
            var ChartSerieHistFornecExcesso = new Chart(ctxFornecExcesso, {
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
            var ctxdoisFornecExcesso = document.getElementById("ChartCoberturaFornecExcesso");
            var ChartCoberturaFornecExcesso = new Chart(ctxdoisFornecExcesso, {

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

            th_tabela_totais_excesso_fornec.innerHTML = ''
            td_tabela_totais_excesso_fornec.innerHTML = ''

            if (Array.isArray(totais)) {
                totais.forEach(t_mes => {
                    th_tabela_totais_excesso_fornec.innerHTML += `
                            <th class="th_totais">${t_mes.mes} de ${t_mes.ano}</th>

                            `
                    td_tabela_totais_excesso_fornec.innerHTML += `
                            <td class="td_totais">${t_mes.quantidade}</td>
                            
                            `
                })
            }
        }
        ,
        error: function (error) {

        }
    });
}
