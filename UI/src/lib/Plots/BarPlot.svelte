<script>
    import { onMount } from 'svelte';
    import * as echarts from "echarts";

    export let chartData = {
        categories: [],
        values: []
    };
    export let title;
    let chartContainer = null;
    let myChart = null;

    onMount(() => {
        initializeChart();
    });

    function initializeChart() {
        myChart = echarts.init(chartContainer);

        const options = {
            title: {
                text: title
            },
            xAxis: {
                type: 'category',
                data: chartData.categories
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: chartData.values,
                type: 'bar',
                color: 'violet'

            }],
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            }
        };

        myChart.setOption(options);
    }

    $:console.log("Logging chart data from component", chartData);
</script>

<div bind:this={chartContainer} class="chart-container"></div>
<style>
    .chart-container {
        width: 600px;
        height: 400px;
    }
</style>
