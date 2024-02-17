<script lang="ts">
    import { urls } from "$lib/stores/urls";
    import {onMount} from "svelte";
    import Rectangle from "$lib/SVG/Shapes/Rectangle.svelte";
    import WebSocketComponent from "$lib/WebSocketHandler/WebSocketComponent.svelte";
    import LinePlot from "$lib/Plots/LinePlot.svelte";

    let HiddenLayers = [{ No_of_Circles: 4 }, { No_of_Circles: 4 }];
    let data = { epochs: [], trainAccuracy: [], testAccuracy: [], loss: [] };
    let plotDataLoss = { x: data.epochs, main: data.loss };
    let plotDataTrainAccuracy = { x: data.epochs, main: data.trainAccuracy };
    let plotDataTestAccuracy = { x: data.epochs, main: data.testAccuracy };
    
    interface Socket {
        sendMessage: (message: string) => object;
    }
    let socket: Socket;
    
    let trainTestSplit = 80;
    let numEpochs = 10;
    function handleMessage(event) {
        const message = JSON.parse(event.detail);
        data.epochs.push(message["Epoch"]);
        data.trainAccuracy.push(message["Train_Accuracy"] * 100);
        data.testAccuracy.push(message["Test_Accuracy"] * 100);
        data.loss.push(message["Loss"]);
        
        plotDataLoss = { ...plotDataLoss };
        plotDataTrainAccuracy = { ...plotDataTrainAccuracy };
        plotDataTestAccuracy = { ...plotDataTestAccuracy };
        console.log(plotDataLoss)
    }
    
    function startTraining() {
        socket.sendMessage(JSON.stringify({ type: "start_training", hidden_layers: HiddenLayers, split: trainTestSplit, epochs: numEpochs }));
    }
</script>
<WebSocketComponent bind:this={socket} on:message={handleMessage} url={$urls.torch_socket} />
<div class="controls">
    <button class="btn btn-info" on:click={() => HiddenLayers = [...HiddenLayers, { No_of_Circles: 4 }]}>Add Layer
    </button>
</div>
<div class="flex items-center">
    {#each HiddenLayers as layer, i (i)}
        <div class="flex flex-col items-center mr-12">
            <Rectangle No_of_Circles={layer.No_of_Circles} />
            <input type="number" min="1" max="10" class="mt-2" bind:value={layer.No_of_Circles} />
        </div>
    {/each}
</div>

<div class="flex">
    <LinePlot bind:data={plotDataLoss} lineColor="red" lineName="Loss" />
    <LinePlot bind:data={plotDataTrainAccuracy} lineColor="yellow" lineName="Train Accuracy" />
    <LinePlot bind:data={plotDataTestAccuracy} lineColor="blue" lineName="Test Accuracy" />
</div>

<div class="slider-container py-4">
    <label class="block text-sm font-medium text-gray-700" for="trainTestSplit">Train/Test Split</label>
    <input bind:value={trainTestSplit} class="slider" id="trainTestSplit" max="90" min="10" type="range" />
    <div class="text-xs mt-1">Training: {trainTestSplit}% / Testing: {100 - trainTestSplit}%</div>
    
    <label class="block text-sm font-medium text-gray-700 mt-4" for="numEpochs">Number of Epochs</label>
    <input bind:value={numEpochs} class="slider" id="numEpochs" max="100" min="1" type="range" />
    <div class="text-xs mt-1">Epochs: {numEpochs}</div>
</div>
<button class="btn btn-accent" on:click={startTraining}>Start Training</button>
