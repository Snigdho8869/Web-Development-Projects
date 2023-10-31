var lifetime_balance = parseFloat(document.getElementById("lifetime_balance").innerHTML.replace("$", ""));
  var lifetime_spending = parseFloat(document.getElementById("lifetime_spending").innerHTML.replace("$", ""));
  var lifetime_ratio = lifetime_balance / (lifetime_balance + lifetime_spending);

  var ctx = document.getElementById("lifetime_chart").getContext("2d");

  var gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, "#36a2eb");
  gradient.addColorStop(1, "#ff6384");

  var chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Lifetime Balance", "Lifetime Spending"],
      datasets: [
        {
          label: "Lifetime Balance vs Lifetime Spending",
          data: [lifetime_ratio, 1 - lifetime_ratio],
          backgroundColor: gradient,
          borderWidth: 1,
          datalabels: {
            color: "#fff",
            font: {
              weight: "bold",
              color: "#fff"
            },
            anchor: "end",
            align: "end",
            formatter: function(value, context) {
              return Math.round(value * 100) + "%";
            }
          }
        }
      ]
    },

    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        datalabels: {
          backgroundColor: function(context) {
            return context.dataset.backgroundColor;
          },
          borderRadius: 4,
          color: "#fff",
          font: {
            size: 16,
            weight: "bold",
            color: "#fff"
          },
          padding: 8
        },
        wave: {
          amplitude: 20,
          animate: true,
          phase: 0,
          type: "liquid"
        },
        animateRotate: {
          rotateDegrees: 360,
          duration: 2000
        }
      },
      legend: {
        display: false
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              max: 1,
              callback: function(value) {
                return value * 100 + "%";
              },
              fontColor: "#fff"
            },
            scaleLabel: {
              display: true,
              labelString: "Percentage",
              fontColor: "#fff"
            }
          }
        ],
        xAxes: [
          {
            ticks: {
              fontColor: "#fff"
            },
          
          }
        ]
      }
    }
  });
