// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';


function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function (n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

// Bar Chart Example
var ctx = document.getElementById("ChartSerieHist");
var ChartSerieHist = new Chart(ctx, {

    data: {
        datasets: [{
            type: 'bar',
            label: 'Quantidade vendida',
            backgroundColor: "#54d8ff",
            hoverBackgroundColor: "#54d8ff",
            borderColor: "#54d8ff",
            data: [14984, 9821, 7841, 5312, 6251, 5781]
        }, {
            type: 'line',
            label: 'Máxima',
            lineTension: 0,
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            pointRadius: 2,
            borderWidth: 1,
            pointBackgroundColor: "#ec6666",
            pointBorderColor: "#ec6666",
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "#ec6666",
            pointHoverBorderColor: "#ec6666",
            pointHitRadius: 10,
            pointBorderWidth: 1,
            borderColor: "#ec6666",
            data: [13000, 13000, 13000, 13000, 13000, 13000,
                13000, 13000, 13000, 13000, 13000, 13000,
                13000, 13000, 13000, 13000, 13000, 13000,
                13000, 13000, 13000, 13000, 13000, 13000,
                13000, 13000, 13000, 13000, 13000, 13000,
                13000, 13000, 13000, 13000, 13000, 13000,
            ],
        }, {
            type: 'line',
            label: 'Média',
            lineTension: 0,
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            pointRadius: 2,
            borderWidth: 1,
            pointBackgroundColor: "#ffd950",
            pointBorderColor: "#ffd950",
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "#ffd950",
            pointHoverBorderColor: "#ffd950",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            borderColor: "#ffd950",
            data: [4000, 4000, 4000, 4000, 4000, 4000,
                4000, 4000, 4000, 4000, 4000, 4000,
                4000, 4000, 4000, 4000, 4000, 4000,
                4000, 4000, 4000, 4000, 4000, 4000,
                4000, 4000, 4000, 4000, 4000, 4000,
                4000, 4000, 4000, 4000, 4000, 4000,
            ],
        }, {
            type: 'line',
            label: 'Minímo',
            lineTension: 0,
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            pointRadius: 2,
            borderWidth: 1,
            pointBackgroundColor: "#f99600",
            pointBorderColor: "#f99600",
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "#f99600",
            pointHoverBorderColor: "#f99600",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            borderColor: "#f99600",
            data: [0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
            ],
        }, {
            type: 'line',
            label: 'Preço unitário',
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
            data: [1567, 3689, 8756, 2354, 4556, 3333],
        }, {
            type: 'line',
            label: 'Custo unitário',
            lineTension: 0,
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            borderColor: "#02bc77",
            pointRadius: 2,
            borderWidth: 1,
            pointBackgroundColor: "#02bc77",
            pointBorderColor: "#02bc77",
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "#02bc77",
            pointHoverBorderColor: "#02bc77",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: [16032, 25364, 8452, 3654, 9687, 12023],
        }],

        labels: ["January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
            "January", "February", "March", "April", "May", "June",
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
                    return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
                }
            }
        },
    }
});
