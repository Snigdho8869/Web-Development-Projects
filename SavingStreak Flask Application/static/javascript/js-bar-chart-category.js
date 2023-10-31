
  document.addEventListener('DOMContentLoaded', function() {
    fetch('/expenses_by_category')
      .then(response => response.json())
      .then(data => {
        var ctx = document.getElementById('bar-chart-category').getContext('2d');
        var myPieChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: data.labels,
    datasets: [{
      label: 'Expense By Category',
      data: data.values,
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#6A4E4D', '#C9CBFF', '#9FB3C8', '#FFD3B5', '#D5E5FF', '#A7A7A7']
    }]
  },
  options: {
  responsive: true,
}

});

      })
      .catch(error => console.error(error));
  });