console.log(month_list)
console.log(months)
Highcharts.chart('infectionsbymonth', {

    title: {
      text: 'American Infections by Month'
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