var ctx = document.getElementById('bar-chart').getContext('2d');
var data = {
  labels: ['Today', 'Last 7 days', 'Last 30 days'],
  datasets: [{
    label: 'Expense History',
    data: [
      document.getElementById('today-expense').value,
      document.getElementById('last-7-days-expense').value,
      document.getElementById('last-30-days-expense').value
    ],
    backgroundColor: [
      'SteelBlue',
      'paleturquoise',
      'Silver'
    ],
    borderColor: [
      'SteelBlue',
      'paleturquoise',
      'Silver'
    ],
    hoverBackgroundColor: [
      'SteelBlue',
      'paleturquoise',
      'Silver'
    ]
  }]
};

Chart.defaults.color = 'white';
Chart.defaults.font.color = 'white';

var options = {
  scales: {
    yAxes: [{
      ticks: {
        beginAtZero: true,
        stepSize: 500
      }
    }]
  }
};

var ctx = document.getElementById('bar-chart').getContext('2d');
var chart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: options
});
