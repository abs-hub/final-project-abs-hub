document.addEventListener('DOMContentLoaded', function () {
  let base_url = `${location.protocol}//${document.domain}:${location.port}`;
  let endpoint = base_url + "/dashboard/chartdata";
  let defaultData = []
  let labels = []

  const request = new XMLHttpRequest();
  request.open('GET', endpoint);
  request.send();

  request.onload = () => {
    const response = JSON.parse(request.responseText);
    console.log(response)
      labels = response.labels;
      defaultData = response.default;
      setchart();
  };

  function setchart() {
    let ctx = document.getElementById("myChart").getContext('2d');
    let myChart = new Chart(ctx, {
      type: 'bar', data: {
        labels: labels, datasets: [{
          label: '# of Task',
          data: defaultData,
          backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'],
          borderColor: ['rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'],
          borderWidth: 1
        }]
      }, options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    });
  }
});
