  document.addEventListener('DOMContentLoaded', function() {
    fetch('/expenses_by_category')
      .then(response => response.json())
      .then(data => {
        var ctx = document.getElementById('pie-chart').getContext('2d');
        var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: data.labels,
    datasets: [{
      data: data.values,
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#6A4E4D', '#C9CBFF', '#9FB3C8', '#FFD3B5', '#D5E5FF', '#A7A7A7']
    }]
  },
  options: {
  responsive: true,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        color: 'white'
      }
    }
  }
}


});

      })
      .catch(error => console.error(error));
  });






