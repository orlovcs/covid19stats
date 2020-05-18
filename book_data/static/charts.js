console.log(month_list)
console.log(months)
console.log(days)
console.log(daily_reported)
console.log(daily_total)

Highcharts.chart('infectionsbymonth', {

    title: {
      text: 'American Infections Reported per Month'
    },
  
    xAxis: {
      categories: months,
      tickInterval: 1,
     
      accessibility: {
        rangeDescription: 'Range: 1 to 10'
      }
    },
  
    yAxis: {
    
      minorTickInterval: 0.1,
      accessibility: {
        rangeDescription: 'Range: 0.1 to 1000'
      }
    },
  
    tooltip: {
      headerFormat: '<b>{series.name}</b><br />',
      pointFormat: 'x = {point.x}, y = {point.y}'
    },
  
    series: [{
      data:  month_list,
    }]
  });


  Highcharts.getJSON(
    'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/usdeur.json',
    function (data) {
  
      Highcharts.chart('container', {
        chart: {
          zoomType: 'x'
        },
        title: {
          text: 'USD to EUR exchange rate over time'
        },
        subtitle: {
          text: document.ontouchstart === undefined ?
            'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: 'Exchange rate'
          }
        },
        legend: {
          enabled: false
        },
        plotOptions: {
          area: {
            fillColor: {
              linearGradient: {
                x1: 0,
                y1: 0,
                x2: 0,
                y2: 1
              },
              stops: [
                [0, Highcharts.getOptions().colors[0]],
                [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
              ]
            },
            marker: {
              radius: 2
            },
            lineWidth: 1,
            states: {
              hover: {
                lineWidth: 1
              }
            },
            threshold: null
          }
        },
  
        series: [{
          type: 'area',
          name: 'USD to EUR',
          data: data
        }]
      });
    }
  );


  Highcharts.chart('infectionsbyday', {

    title: {
      text: 'American Infections Reported per Month'
    },
  
    xAxis: {
      categories: months,
      tickInterval: 1,
     
      accessibility: {
        rangeDescription: 'Range: 1 to 10'
      }
    },
  
    yAxis: {
    
      minorTickInterval: 0.1,
      accessibility: {
        rangeDescription: 'Range: 0.1 to 1000'
      }
    },
  
    tooltip: {
      headerFormat: '<b>{series.name}</b><br />',
      pointFormat: 'x = {point.x}, y = {point.y}'
    },
  
    series: [{
      data:  [[01/22/20]],
    }]
  });

 