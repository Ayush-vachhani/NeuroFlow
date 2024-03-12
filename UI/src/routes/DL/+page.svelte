<script lang="ts">
    import {urls} from "$lib/stores/urls";
    import Rectangle from "$lib/SVG/Rectangle.svelte";
    import WebSocketComponent from "$lib/WebSocketHandler/WebSocketComponent.svelte";
    import LinePlot from "$lib/Plots/LinePlot.svelte";

    let HiddenLayers = [{No_of_Circles: 4}, {No_of_Circles: 4}];
    let data = {epochs: [], trainAccuracy: [], testAccuracy: [], loss: [], Precision: [], Recall: [], F1Score: []};
    let plotDataLoss = {x: data.epochs, main: data.loss};
    let plotDataTrainAccuracy = {x: data.epochs, main: data.trainAccuracy};
    let plotDataTestAccuracy = {x: data.epochs, main: data.testAccuracy};
    let plotPrecision = {x: data.epochs, main: data.Precision};
    let plotRecall = {x: data.epochs, main: data.Recall};
    let plotF1Score = {x: data.epochs, main: data.F1Score};
    let selectedLossFunction = 'BCELoss';

    interface Socket {
        sendMessage: (message: string) => void;
    }

    let socket: Socket;

    let trainTestSplit = 80;
    let numEpochs = 5;

    function handleMessage(event) {
        const message = JSON.parse(event.detail);
        data.epochs.push(message["Epoch"]);
        data.trainAccuracy.push(message["Train_Accuracy"] * 100);
        data.testAccuracy.push(message["Test_Accuracy"] * 100);
        data.loss.push(message["Loss"]);
        data.Precision.push(message["Precision"] * 100);
        data.Recall.push(message["Recall"] * 100);
        data.F1Score.push(message["F1_Score"] * 100);

        data = {...data};
        plotDataLoss = {...plotDataLoss};
        plotDataTrainAccuracy = {...plotDataTrainAccuracy};
        plotDataTestAccuracy = {...plotDataTestAccuracy};
        plotPrecision = {...plotPrecision};
        plotRecall = {...plotRecall};
        plotF1Score = {...plotF1Score};
    }

    function startTraining() {
        socket.sendMessage(JSON.stringify({
            type: "start_training",
            hidden_layers: HiddenLayers,
            split: trainTestSplit,
            epochs: numEpochs,
            loss_function: selectedLossFunction
        }));
    }
</script>
<WebSocketComponent bind:this={socket} on:message={handleMessage} url={$urls.torch_socket}/>
<div class="controls">
    <button class="btn btn-info" on:click={() => HiddenLayers = [...HiddenLayers, { No_of_Circles: 4 }]}>Add Layer
    </button>
</div>
<div class="flex items-center">
    {#each HiddenLayers as layer, i (i)}
        <div class="flex flex-col items-center mr-12">
            <Rectangle No_of_Circles={layer.No_of_Circles}/>
            <input type="number" min="1" max="10" class="mt-2" bind:value={layer.No_of_Circles}/>
        </div>
    {/each}
</div>

<div class="flex">
    <LinePlot bind:data={plotDataLoss} lineColor="red" lineName="Loss"/>
    <LinePlot bind:data={plotDataTrainAccuracy} lineColor="yellow" lineName="Train Accuracy"/>
    <LinePlot bind:data={plotDataTestAccuracy} lineColor="blue" lineName="Test Accuracy"/>
    <LinePlot bind:data={plotPrecision} lineColor="green" lineName="Precision"/>
    <LinePlot bind:data={plotRecall} lineColor="purple" lineName="Recall"/>
    <LinePlot bind:data={plotF1Score} lineColor="orange" lineName="F1 Score"/>
</div>

<div class="slider-container py-4">
    <label class="block text-sm font-medium text-gray-700" for="trainTestSplit">Train/Test Split</label>
    <input bind:value={trainTestSplit} class="slider" id="trainTestSplit" max="90" min="10" type="range"/>
    <div class="text-xs mt-1">Training: {trainTestSplit}% / Testing: {100 - trainTestSplit}%</div>

    <label class="block text-sm font-medium text-gray-700 mt-4" for="numEpochs">Number of Epochs</label>
    <input bind:value={numEpochs} class="slider" id="numEpochs" max="100" min="1" type="range"/>
    <div class="text-xs mt-1">Epochs: {numEpochs}</div>
</div>
<button class="btn btn-accent" on:click={startTraining}>Start Training</button>
<div class="form-control">
    <label class="label">
        <span class="label-text">Select Loss Function</span>
    </label>
    <select bind:value={selectedLossFunction} class="select select-bordered w-full max-w-xs">
        <option value="BCELoss">BCE Loss</option>
        <option value="CrossEntropyLoss">Cross Entropy Loss</option>
    </select>

</div>
