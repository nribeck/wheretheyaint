$(function () { 
    $('#slg-bar-chart').highcharts({
        exporting: { enabled: false },
        credits: { enabled: false },
        chart: {
            type: 'bar'
        },
        title: {
            text: ''
        },
        legend: {
            layout: 'horizontal',
            verticalAlign: 'top',
            itemStyle: {
                 fontSize:'18',
                 color: 'black'
             }
        },
        tooltip: {
            valueDecimals: 3
        },
        xAxis: {
            gridLineWidth: 0,
            categories: [player],
            labels: {
                enabled: false
            }
        },
        yAxis: {
            plotLines: [{
                color: 'black',
                width: 2,
                value: 0             
            }],
            gridLineWidth: 1,
            title: {
                text: 'SLG (Total bases per batted ball)',
                    style: {
                        fontSize: '18px',
                        color: 'black'
                    }
            },
            labels: {
                style: {
                    fontSize:'14px',
                    color: 'black'
                }
            }
        },
        series: [{
            name: 'actual',
            data: [actual_slg]
        }, {
            name: 'expected',
            data: [expected_slg]
        }, {
            name: 'luck',
            data: [luck]
        }]
    });
});