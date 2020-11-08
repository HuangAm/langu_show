$(function () {
    // 参考：https://jshare.com.cn/highstock/hhhhvm
    var rowId = 0;
    let timer = null;
    let chart = initChart();

    //初识化数据调用第一次
    drawChart(rowId, '1H');

    $(".flex").on("click", "button", function (e) {
        $('.freq').each(function (value) {
            // 这里的 this 是 flex 的子元素
            $(this).removeClass('red');
        });
        let value = $(this).val();
        $(this).addClass("red");
        clearTimeout(timer);
        drawChart(rowId, value)
    });

    function initChart() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            },
            lang: {
                months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                shortMonths: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
                weekdays: ["星期天", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
                // rangeSelectorZoom: "",
                // rangeSelectorFrom: "从",
                // rangeSelectorTo: "到",
                // resetZomm:'重置',
                // resetZoomTitle:'重置缩放比例'
            }
        });
        let chart = Highcharts.stockChart('container', {
            // chart: {
            //     zoomType: 'x',
            // },
            mapNavigation: {
                enabled: true,
                enableButtons: false,
            },
            rangeSelector: {
                // buttons: [{
                //     count: 1,
                //     type: 'minute',
                //     text: '1M'
                // }, {
                //     count: 5,
                //     type: 'minute',
                //     text: '5M'
                // }, {
                //     count: 1,
                //     type: 'hour',
                //     text: '1h'
                // }, {
                //     count: 4,
                //     type: 'hour',
                //     text: '4h'
                // }, {
                //     count: 1,
                //     type: 'day',
                //     text: '1d'
                // }, {
                //     count: 1,
                //     type: 'month',
                //     text: '1m'
                // }, {
                //     type: 'all',
                //     text: 'All'
                // }],
                buttons: [],
                inputEnabled: false,
                // selected: 2
            },
            title: {
                text: '金吒净值'
            },
            navigator: {
                enabled: false
            },
            scrollbar: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            tooltip: {
                split: false,
                xDateFormat: '%Y-%m-%d %H:%M %A',
                valueDecimals: 2,
                valueSuffix: " 元",
                shared: true
            },
            xAxis: {
                labels: {
                    formatter: function () {
                        return Highcharts.dateFormat('%m-%d %H:%M', this.value);
                    }
                },
            },
            yAxis: {
                title: {
                    text: '净值（元）'
                },
                labels: {
                    formatter: function () {
                        return (this.value / 1000).toFixed(2) + 'k'
                    },
                    align: "right",
                }
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: '金吒净值',
                data: []
            }]
        });
        return chart
    }

    function getData(rowId, type) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: "/data/?rowId=" + rowId + "&freq=" + type,
                async: false,
                dataType: "json",
                success: function (data) {
                    resolve(data)
                },
                error: function (err) {
                    reject(err)
                }
            })
        })
    }

    async function drawChart(rowId, value) {
        let result = await getData(rowId, value);
        let data = result.data;
        rowId = result.rowId;
        chart.series[0].setData(data);
        timer = setTimeout(() => {
            drawChart(rowId, value)
        }, 60 * 1000)
    }
});