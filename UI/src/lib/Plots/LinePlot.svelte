<script>
    import {onMount} from 'svelte';
    import * as echarts from "echarts";

    let chartContainer;
    let chartInstance;
    export let data = {};
    export let lineColor;
    export let lineName;

    onMount(async () => {
        chartInstance = echarts.init(chartContainer);
        updateChart();
    });

    function updateChart() {
        if (chartInstance) {
            chartInstance.setOption({
                xAxis: {
                    type: 'category',
                    data: data.x
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                series: [{
                    data: data.main,
                    type: 'line',
                    name: lineName,
                    smooth: true,
                    itemStyle: {color: lineColor},
                }],
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: [lineName]
                }
            });
        }
    }

    $: if (chartInstance) {
        updateChart();
    }
</script>
<div bind:this={chartContainer} class="chart-container"></div>
<style>
    .chart-container {
        width: 600px;
        height: 400px;
    }
</style>
