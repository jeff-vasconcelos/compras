// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


$.ajax({
    type: 'GET',
    url: '/painel/home-graficos/',
    success: function (response) {
        const dados = response.data

        const graficoUm = dados[0]
        const graficoDois = dados[1]

        const curvaA = graficoUm[0]
        const curvaB = graficoUm[1]
        const curvaC = graficoUm[2]
        const curvaD = graficoUm[3]
        const curvaE = graficoUm[4]

        const curvaRuptura = graficoDois[0]

        console.log(curvaRuptura)


        // CURVA A
        var ctx1 = document.getElementById("chartCurvaA");
        var ChartCurvaA = new Chart(ctx1, {
            type: 'doughnut',
            data: {
                labels: ["Normal", "Parcial", "Excesso"],
                datasets: [{
                    data: [curvaA.p_normal, curvaA.p_parcial, curvaA.p_excesso],
                    backgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
                    hoverBackgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
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
                    data: [curvaB.p_normal, curvaB.p_parcial, curvaB.p_excesso],
                    backgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
                    hoverBackgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
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
                    data: [curvaC.p_normal, curvaC.p_parcial, curvaC.p_excesso],
                    backgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
                    hoverBackgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
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
                    data: [curvaD.p_normal, curvaD.p_parcial, curvaD.p_excesso],
                    backgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
                    hoverBackgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
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
                    data: [curvaE.p_normal, curvaE.p_parcial, curvaE.p_excesso],
                    backgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
                    hoverBackgroundColor: ['#50c878', '#ffbc40', '#e32f1c'],
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
                datasets: [{
                    label: "R$ ",
                    backgroundColor: "#4e73df",
                    hoverBackgroundColor: "#2e59d9",
                    borderColor: "#4e73df",
                    data: curvaRuptura.valor,
                }],
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
                            maxTicksLimit: 6
                        },
                        maxBarThickness: 25,
                    }],
                    yAxes: [{
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
                    }],
                },
                legend: {
                    display: false
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
                            return datasetLabel + ": " + tooltipItem.yLabel.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                        }
                    },
                },
            }
        });


    },
    error: function (error) {
        console.log(error)
    }
})