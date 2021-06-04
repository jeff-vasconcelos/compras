// Set new default font family and font color to mimic Bootstrap's default styling
// Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
//
//
// function number_format(number, decimals, dec_point, thousands_sep) {
//     // *     example: number_format(1234.56, 2, ',', ' ');
//     // *     return: '1 234,56'
//     number = (number + '').replace(',', '').replace(' ', '');
//     var n = !isFinite(+number) ? 0 : +number,
//         prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
//         sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
//         dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
//         s = '',
//         toFixedFix = function (n, prec) {
//             var k = Math.pow(10, prec);
//             return '' + Math.round(n * k) / k;
//         };
//     // Fix for IE parseFloat(0.55).toFixed(0) = 0;
//     s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
//     if (s[0].length > 3) {
//         s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
//     }
//     if ((s[1] || '').length < prec) {
//         s[1] = s[1] || '';
//         s[1] += new Array(prec - s[1].length + 1).join('0');
//     }
//     return s.join(dec);
// }

// Bar Chart Example
const leadtime = document.getElementById('leadtime')
const t_reposicao = document.getElementById('tempo_reposicao')
const listaProdutosSelecionarG = document.getElementById('results-produtos')


const sendSelectProdGraf = (prod) => {
    $.ajax({
        type: 'POST',
        url: '/painel/graficos-prod-selec/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'produto': prod
        },
        success: (data) => {
            const graficos = data.data
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
            //
            //ChartSerieHist.destroy();
            ChartSerieHist.update();
            // graficos.update();
            // graficos.destroy();

            console.log(graficos, "apagando arry")
            console.log(ChartSerieHist, "apagando arry")
        }

    })
}

listaProdutosSelecionarG.addEventListener('change', e => {
    // PEGANDO PRODUTO SELECIONADO
    const produtoSelecionado = e.target.value

    console.log(produtoSelecionado)
    console.log("Selecionando para grafico")


    sendSelectProdGraf(produtoSelecionado)
})




