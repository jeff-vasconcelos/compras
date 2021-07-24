// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


// CURVA A
var ctx1 = document.getElementById("chartCurvaA");
var ChartCurvaA = new Chart(ctx1, {
    type: 'doughnut',
    data: {
        labels: ["Normal", "Parcial", "Excesso"],
        datasets: [{
            data: [50, 25, 25],
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
        cutoutPercentage: 90,
    },
});


// CURVA B
var ctx2 = document.getElementById("chartCurvaB");
var ChartCurvaB = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ["Normal", "Parcial", "Excesso"],
        datasets: [{
            data: [50, 25, 25],
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
        cutoutPercentage: 90,
    },
});

// CURVA C
var ctx3 = document.getElementById("chartCurvaC");
var chartCurvaC = new Chart(ctx3, {
    type: 'doughnut',
    data: {
        labels: ["Normal", "Parcial", "Excesso"],
        datasets: [{
            data: [50, 25, 25],
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
        cutoutPercentage: 90,
    },
});

// CURVA D
var ctx4 = document.getElementById("chartCurvaD");
var chartCurvaD = new Chart(ctx4, {
    type: 'doughnut',
    data: {
        labels: ["Normal", "Parcial", "Excesso"],
        datasets: [{
            data: [50, 25, 25],
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
        cutoutPercentage: 90,
    },
});

// CURVA E
var ctx5 = document.getElementById("chartCurvaE");
var chartCurvaE = new Chart(ctx5, {
    type: 'doughnut',
    data: {
        labels: ["Normal", "Parcial", "Excesso"],
        datasets: [{
            data: [50, 25, 25],
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
        cutoutPercentage:90,
    },
});


// Bar Chart Example
var ctx6 = document.getElementById("chartRupturaxCurva");
var chartRupturaxCurva = new Chart(ctx6, {
    type: 'bar',
    data: {
        labels: ["A", "B", "C", "D", "E"],
        datasets: [{
            label: "Revenue",
            backgroundColor: "#4e73df",
            hoverBackgroundColor: "#2e59d9",
            borderColor: "#4e73df",
            data: [4215, 5312, 6251, 7841, 9821],
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
                    max: 15000,
                    maxTicksLimit: 5,
                    padding: 10,
                    // Include a dollar sign in the ticks
                    // callback: function(value, index, values) {
                    //   return '$' + number_format(value);
                    // }
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
                // label: function(tooltipItem, chart) {
                //   var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                //   return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
                // }
            }
        },
    }
});