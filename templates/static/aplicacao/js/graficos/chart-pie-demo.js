// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Curva A", "Curva B", "Curva C", "Curva C", "Curva D", "Curva E", "Curva X"],
    datasets: [{
      data: [40, 25, 15, 10, 6.5, 3.5],
      backgroundColor: ['#02e591', '#4791ff', '#54d8ff', '#a3a0fb', '#ffd950', '#ec6666'],
      hoverBackgroundColor: ['#02e591', '#4791ff', '#54d8ff', '#a3a0fb', '#ffd950', '#ec6666'],
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
    cutoutPercentage: 80,
  },
});
