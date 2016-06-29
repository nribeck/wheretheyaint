$(function () { 
    $('#luck-chart').highcharts({
        exporting: { enabled: false },
        credits: { enabled: false },
        chart: {
            type: 'line',
            zoomType: 'xy'
        },
        title: {
            text: ''
        },
        legend: {
            layout: 'horizontal',
            verticalAlign: 'top',
            itemStyle: {
                 fontSize:'20',
                 color: 'black'
             }
        },
        tooltip: {
            valueDecimals: 1,
            valueSuffix: ' bases'
        },
        xAxis: {
            gridLineWidth: 1,
            title: {
                text: 'Batted-Ball Events',
                    style: {
                        fontSize: '20px',
                        color: 'black'
                    }
            },
            labels: {
                style: {
                    fontSize:'16px',
                    color: 'black'
                }
            }
        },
        yAxis: {
            plotLines: [{
                color: 'black',
                width: 2,
                value: 0,
                dashStyle: 'dot'             
            }],
            gridLineWidth: 0,
            title: {
                text: 'Cumulative Total Bases',
                    style: {
                        fontSize: '20px',
                        color: 'black'
                    }
            },
            labels: {
                style: {
                    fontSize:'16px',
                    color: 'black'
                }
            }
        },
        series: [{
            name: 'actual',
            data: actual_bases
        }, {
            name: 'expected',
            data: exp_bases
        }, {
            name: 'luck',
            data: luck_bases
        }]
    });
});