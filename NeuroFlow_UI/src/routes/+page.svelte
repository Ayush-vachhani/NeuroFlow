<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import {urls} from "../stores/urls.ts";
    import type {WebSocketEvents} from "vitest"
    import {trainAndTestModel} from "../Functions/Send";

    let websocket: WebSocket;
    let message:string = null;
    let isConnected:boolean = false;

    let classificationTask = 'RandomForest';

    const classifiers = {
        LogisticRegression: {
            params: ['C', 'max_iter'], // 'C' for regularization strength, 'solver' for the algorithm
        },
        SupportVectorMachine: {
            params: ['C', 'gamma'], // 'C' for regularization strength, 'kernel' for the kernel type
        },
        DecisionTrees: {
            params: ['max_depth', 'min_samples_split'], // 'max_depth' of the tree, 'min_samples_split' for the minimum number of samples required to split
        },
        RandomForest: {
            params: ['n_estimators', 'max_depth'], // 'n_estimators' for the number of trees, 'max_depth' of the tree
        },
    };

    function handleSelection(classifier) {
        classificationTask = classifier;
    }
    onMount(() => {
        websocket = new WebSocket($urls.scikitlearn_socket);

        websocket.onopen = () => {
            console.log('WebSocket connection established');
            isConnected = true;
        };

        websocket.onmessage = (event:WebSocketEvents) => {
            console.log(event.data)
            const data = JSON.parse(event.data);
            message = data.message;
        };

        websocket.onerror = (error:WebSocketEvents) => {
            console.error('WebSocket error:', error);
            isConnected = false;
        };

        websocket.onclose = (event:WebSocketEvents) => {
            console.log('WebSocket connection closed:', event);
            isConnected = false;
        };
    });

    function handleTrainAndTest(event: Event) {
        const formData = new FormData(event.target as HTMLFormElement);
        const parameters = {};
        for (let [key, value] of formData.entries()) {
            parameters[key] = isNaN(Number(value)) ? value : Number(value);
        }
        console.log(parameters)
        trainAndTestModel(websocket, 'Train and Test', parameters, classificationTask);
    }

    onDestroy(() => {
        if (websocket) {
            websocket.close();
        }
    });
</script>

<div class="flex h-screen">
    <!-- Enhanced Side Menu -->
    <div class="w-1/4 bg-blue-700 text-white p-4">
        <ul>
            {#each Object.keys(classifiers) as classifier}
                <li class="mb-2">
                    <button
                        on:click={() => handleSelection(classifier)}
                        class="w-full text-left py-2 px-4 rounded hover:bg-blue-800">
                        {classifier.replace(/([A-Z])/g, ' $1').trim()}
                    </button>
                </li>
            {/each}
        </ul>
    </div>

    <!-- Main Content -->
    <div class="w-3/4 p-4">
        <h2 class="text-xl font-bold mb-4">{classificationTask.replace(/([A-Z])/g, ' $1').trim()}</h2>
        <form on:submit|preventDefault={handleTrainAndTest}>
            {#each classifiers[classificationTask].params as param}
                <div class="mb-4">
                    <label class="block mb-2">{param}</label>
                    <input type="text" class="border rounded p-2 w-full" name={param}/>
                </div>
            {/each}
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Submit</button>
        </form>
        {#if message}
            <div class="alert alert-info mt-4">{message}</div>
        {/if}
    </div>
</div>