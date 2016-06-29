$(function () { 
    $('#chart-test').highcharts({
        chart: {
            type: 'scatter'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            title: {
                text: 'Day'
            }
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [[5, 2], [6, 3], [8, 2]]
        }, {
            name: 'John',
            data: [[4, 3], [5, 4], [7, 1]]
        }]
    });
});