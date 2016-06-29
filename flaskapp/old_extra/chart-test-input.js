$(function () { 
    $('#chart-test-input').highcharts({
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
            data: janedata
        }, {
            name: 'John',
            data: johndata
        }]
    });
});