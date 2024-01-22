<script lang="ts">
    import { onMount, getContext } from "svelte";
    import * as echarts from 'echarts';
    import  WebSocketComponent  from "$lib/WebSocketHandler/WebSocketComponent.svelte";
    import { urls } from "$lib/stores/urls.js";

    let chartContainer1, chartContainer2;
    let chartInstance1, chartInstance2;
    let data = { epochs: [], trainAccuracy: [], testAccuracy: [], loss: [] };

    let socket;

    onMount(() => {
        chartInstance1 = echarts.init(chartContainer1);
        chartInstance2 = echarts.init(chartContainer2);
    });
    function handleMessage(event) {
        const updatedMessage = JSON.parse(event.detail)
        console.log(updatedMessage)
        console.log(typeof updatedMessage)
        updateData(updatedMessage);
        updateChart();
    }
    function updateData(message) {
        if (message && typeof message === 'object') {
            if (message["Epoch"] !== undefined) {
                data.epochs.push(message["Epoch"]);
            }
            if (message["Train_Accuracy"] !== undefined) {
                data.trainAccuracy.push(message["Train_Accuracy"]);
            }
            if (message["Test_Accuracy"] !== undefined) {
                data.testAccuracy.push(message["Test_Accuracy"]);
            }
            if (message["Loss"] !== undefined) {
                data.loss.push(message["Loss"]);
            }
        } else {
            console.error("Invalid message format:", message);
        }
    }


    function updateChart() {
        chartInstance1.setOption({
            xAxis: {
                type: 'category',
                data: data.epochs
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 1,
                axisLabel: {
                    formatter: '{value}'
                }
            },
            series: [{
                data: data.trainAccuracy,
                type: 'line',
                name: 'Train Accuracy',
                itemStyle: { color: 'blue' }
            }, {
                data: data.testAccuracy,
                type: 'line',
                name: 'Test Accuracy',
                itemStyle: { color: 'yellow' }
            }],
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Train Accuracy', 'Test Accuracy']
            }
        });

        chartInstance2.setOption({
            xAxis: {
                type: 'category',
                data: data.epochs
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            },
            series: [{
                data: data.loss,
                type: 'line',
                name: 'Loss',
                itemStyle: { color: 'red' }
            }],
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Loss']
            }
        });
    }
    function resetGraph() {
        data = { epochs: [], trainAccuracy: [], testAccuracy: [], loss: [] };
        updateChart();
    }
    function startTraining() {
        socket.sendMessage(JSON.stringify({ action: 'start_training', dataset: 'Titanic' }));
    }
</script>
<main>
    <h1>Test</h1>
    <WebSocketComponent url={$urls.torch_socket}  bind:this={socket} on:message={handleMessage}/>
    <button on:click={startTraining} class="btn btn-primary">Start Training</button>
    <button on:click={resetGraph} class="btn btn-secondary">Reset Graph</button>
    <div bind:this={chartContainer1} class="chart-container"></div>
    <div bind:this={chartContainer2} class="chart-container"></div>
</main>

<style>
    .chart-container {
        width: 600px;
        height: 400px;
    }
</style>
