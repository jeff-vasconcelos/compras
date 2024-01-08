// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


$.ajax({
    type: 'GET',
    url: '/painel/home-graficos/',
    success: function (response) {

        const dados = response.data

        if (dados[0] === 1) {
            console.log(dados)

        } else {
            const graficoCurva = dados[0]
            const graficoFaturamento = dados[1]

            const curvaA = graficoCurva[0]
            const curvaB = graficoCurva[1]
            const curvaC = graficoCurva[2]
            const curvaD = graficoCurva[3]
            const curvaE = graficoCurva[4]

            const curvaRuptura = graficoFaturamento[0]

            // CURVA A
            var ctx1 = document.getElementById("chartCurvaA");
            var ChartCurvaA = new Chart(ctx1, {
                type: 'doughnut',
                data: {
                    labels: ["Normal", "Parcial", "Excesso"],
                    datasets: [{
                        data: [curvaA.part_normal, curvaA.part_parcial, curvaA.part_excesso],
                        backgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBackgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                    },
                    legend: {
                        display: false
                    },
                    cutoutPercentage: 70,
                },
            });


            // CURVA B
            var ctx2 = document.getElementById("chartCurvaB");
            var ChartCurvaB = new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ["Normal", "Parcial", "Excesso"],
                    datasets: [{
                        data: [curvaB.part_normal, curvaB.part_parcial, curvaB.part_excesso],
                        backgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBackgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                    },
                    legend: {
                        display: false
                    },
                    cutoutPercentage: 70,
                },
            });

            // CURVA C
            var ctx3 = document.getElementById("chartCurvaC");
            var chartCurvaC = new Chart(ctx3, {
                type: 'doughnut',
                data: {
                    labels: ["Normal", "Parcial", "Excesso"],
                    datasets: [{
                        data: [curvaC.part_normal, curvaC.part_parcial, curvaC.part_excesso],
                        backgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBackgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                    },
                    legend: {
                        display: false
                    },
                    cutoutPercentage: 70,
                },
            });

            // CURVA D
            var ctx4 = document.getElementById("chartCurvaD");
            var chartCurvaD = new Chart(ctx4, {
                type: 'doughnut',
                data: {
                    labels: ["Normal", "Parcial", "Excesso"],
                    datasets: [{
                        data: [curvaD.part_normal, curvaD.part_parcial, curvaD.part_excesso],
                        backgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBackgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                    },
                    legend: {
                        display: false
                    },
                    cutoutPercentage: 70,
                },
            });

            // CURVA E
            var ctx5 = document.getElementById("chartCurvaE");
            var chartCurvaE = new Chart(ctx5, {
                type: 'doughnut',
                data: {
                    labels: ["Normal", "Parcial", "Excesso"],
                    datasets: [{
                        data: [curvaE.part_normal, curvaE.part_parcial, curvaE.part_excesso],
                        backgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBackgroundColor: ['#50c878', '#ffbc40', '#FC544B'],
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                    },
                    legend: {
                        display: false
                    },
                    cutoutPercentage: 70,
                },
            });


            // Bar Chart Example
            var ctx6 = document.getElementById("chartRupturaxCurva");
            var chartRupturaxCurva = new Chart(ctx6, {
                type: 'bar',
                data: {
                    labels: curvaRuptura.curva,
                    datasets: [
                        {
                            label: "R$",
                            yAxisID: 'A',
                            backgroundColor: "#4e73df",
                            hoverBackgroundColor: "#2e59d9",
                            borderColor: "#4e73df",
                            data: curvaRuptura.valor,
                            maxBarThickness: 45,
                        },
                        {
                            label: "%",
                            yAxisID: 'B',
                            backgroundColor: "#50c878",
                            hoverBackgroundColor: "#1D370A",
                            borderColor: "#1D370A",
                            data: curvaRuptura.porcentagem,
                            maxBarThickness: 35,
                        }

                    ],
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
                                unit: 'number'
                            },
                            gridLines: {
                                display: false,
                                drawBorder: false
                            },
                            ticks: {
                                maxTicksLimit: 5
                            },

                        }],
                        yAxes: [{
                            id: 'A',
                            ticks: {
                                min: 0,
                                maxTicksLimit: 5,
                                padding: 10,
                                // Include a dollar sign in the ticks
                                callback: function (value, index, values) {
                                    return value.toLocaleString('pt-br', {style: 'currency', currency: 'BRL'});
                                    // 'R$' + value;
                                }
                            },
                            gridLines: {
                                color: "rgb(234, 236, 244)",
                                zeroLineColor: "rgb(234, 236, 244)",
                                drawBorder: false,
                                borderDash: [2],
                                zeroLineBorderDash: [2]
                            }
                        },
                            {
                                id: 'B',
                                position: 'right',
                                ticks: {
                                    min: 0,
                                    maxTicksLimit: 5,
                                    padding: 10,
                                    // Include a dollar sign in the ticks
                                    callback: function (value, index, values) {
                                        // return value.toLocaleString('pt-br', {style: 'currency', currency: 'BRL'});
                                        return value + '%';
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
                        callbacks: {
                            label: function (tooltipItem, chart) {
                                var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                                return datasetLabel + " " + tooltipItem.yLabel.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&.');
                            }
                        },
                    },
                }
            });

        }
    },
    error: function (error) {
        console.log(error)
    }
})