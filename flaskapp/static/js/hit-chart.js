$(function () { 
    $('#hit-chart').highcharts({
        exporting: { enabled: false },
        credits: { enabled: false },
        chart: {
            type: 'scatter',
            marginTop: 100,
            spacingLeft: 0
        },
        title: {
            text: 'Batted-Ball Properties for '+player,
                style: {
                    fontSize: '20px',
                    color: 'black'
                }
        },
        legend: {
            y:40,
            backgroundColor: 'white',
            borderWidth: 1,
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            floating: true,
            itemStyle: {
                 fontSize:'14',
                 color: 'black'
             }
        },
        xAxis: {
            min: 20,
            max: 120,
            gridLineWidth: 1,
            title: {
                text: 'Hit speed',
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
        yAxis: {
            min: -100,
            max: 100,
            gridLineWidth: 1,
            title: {
                text: 'Hit angle',
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
            name: 'blast',
            data: hit_chart_data6
        }, {
            name: 'solid',
            data: hit_chart_data2
        }, {
            name: 'decent',
            data: hit_chart_data3
        }, {
            name: 'bloop',
            data: hit_chart_data7
        }, {
            name: 'grounder',
            data: hit_chart_data1         
        }, {
            name: 'dribbler',
            data: hit_chart_data5
        }, {
            name: 'pop/fly',
            data: hit_chart_data4
        }]
    });
});