
console.log(days)
console.log(numbers)


  Highcharts.chart('infectionsbyday', {

    title: {
      text: 'American Infections Reported per Day'
    },
  
    xAxis: {
      categories: days,
     
      accessibility: {
        rangeDescription: 'Range: 1 to 10'
      }
    },
  
    yAxis: {
    
      accessibility: {
        rangeDescription: 'Range: 0.1 to 1000'
      }
    },
  
    tooltip: {
      headerFormat: '<b>{series.name}</b><br />',
      pointFormat: 'x = {point.x}, y = {point.y}'
    },
  
    series: [{
      data:  numbers
    }]
  });

   Highcharts.chart('infectionsbymonth', {

    title: {
      text: 'American Infections Reported per Day'
    },
  
    xAxis: {
      categories: months,
     
      accessibility: {
        rangeDescription: 'Range: 1 to 10'
      }
    },
  
    yAxis: {
    
      accessibility: {
        rangeDescription: 'Range: 0.1 to 1000'
      }
    },
  
    tooltip: {
      headerFormat: '<b>{series.name}</b><br />',
      pointFormat: 'x = {point.x}, y = {point.y}'
    },
  
    series: [{
      data:  mnumbers
    }]
  });
   