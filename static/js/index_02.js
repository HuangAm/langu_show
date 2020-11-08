// 参考：https://jshare.com.cn/highstock/hhhhvm
var rowId = 0;
Highcharts.setOptions({
    global: {
        useUTC: false
    },
    lang: {
        months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        shortMonths: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        weekdays: ["星期天", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
        rangeSelectorZoom: "",
        rangeSelectorFrom: "从",
        rangeSelectorTo: "到"
    }
});


function initChart(data){
    Highcharts.setOptions({
        global: {
            useUTC: false
        },
        lang: {
            months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
            shortMonths: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
            weekdays: ["星期天", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
            rangeSelectorZoom: "",
            rangeSelectorFrom: "从",
            rangeSelectorTo: "到"
        }
    });
    let chart = Highcharts.stockChart('container',{
        chart: {
            zoomType: "x",
            // events: {
            //     load: function () {
            //         // 每分钟更新一次
            //         var series = this.series[0];
            //         setInterval(function () {
            //             let p = [];
            //             $.ajax({
            //                 url: `/data/?rowId=${rowId}&freq=${fq}`,
            //                 type: "GET",
            //                 dataType: "json",
            //                 async: false,
            //                 success: function (data, statusText, xmlHttpRequest) {
            //                     console.log(data);
            //                     p = data.data;
            //                     rowId = data.rowId;
            //                 }
            //             });
            //             if (p.length >= 1) {
            //                 for (let i = 0; i < p.length; i++) {
            //                     series.addPoint(p[i], true, true);
            //                 }
            //             }
            //         }, 60 * 1000);
            //     }
            // }
        },
        mapNavigation: {
            enabled: true,
            enableButtons: false,
        },
        title: {
            text: "金吒净值"
        },
        tooltip: {
            split: false,
            xDateFormat: "%Y-%m-%d %H:%M %A",
            valueDecimals: 2,
            valueSuffix: " 元",
            shared: true
        },
        yAxis: {
            title: {
                text: "净值（元）"
            }
        },
        exporting: {
            enabled: false
        },
        series:data
    
    });
    return chart
}
let timer = null;
let chart = initChart();
function drawChart(rowId,fq){
    $.ajax({
        url: `/data/?rowId=${rowId}&freq=${fq}`,
        type: "GET",
        dataType: "json",
        async: false,
        success: function (data, statusText, xmlHttpRequest) {
           chart.series[0].setData(data)
        }
    });
    timer = setTimeout(()=>{
        drawChart(rowId,fq)
    },1000)
}

$(".freq").on('click', function () {
    clearTimeout(timer);
    let fq = $(this).prop('value');
    drawChart(rowId,fq)
});