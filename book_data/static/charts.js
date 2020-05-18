month_list = null;
console.log(month_list)

Highcharts.chart('container', {

    title: {
      text: 'American Infections by Month'
    },
  
    xAxis: {
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
      data:  [[5, 2], [6, 3], [8, 2]],
      pointStart: 1
    }]
  });