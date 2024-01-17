<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import {urls} from "../stores/urls.ts";
    import type {WebSocketEvents} from "vitest"
    import {trainAndTestModel} from "../Functions/Send";

    let websocket: WebSocket;
    let message:string = null;

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
        };

        websocket.onmessage = (event:WebSocketEvents) => {
            const data = JSON.parse(event.data);
            message = data.message;
        };

        websocket.onerror = (error:WebSocketEvents) => {
            console.error('WebSocket error:', error);
        };

        websocket.onclose = (event:WebSocketEvents) => {
            console.log('WebSocket connection closed:', event);
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
    <div class="sidebar bg-base-200 w-1/4">
        <ul class="menu p-4 overflow-y-auto w-full bg-base-100 text-base-content">
            {#each Object.keys(classifiers) as classifier}
                <li>
                    <button
                        on:click={() => handleSelection(classifier)}
                        class="btn btn-ghost w-full justify-start">
                        {classifier.replace(/([A-Z])/g, ' $1').trim()}
                    </button>
                </li>
            {/each}
        </ul>
    </div>

    <!-- Main Content -->
    <div class="w-3/4 p-4">
        <h2 class="text-xl font-bold mb-4">{classificationTask.replace(/([A-Z])/g, ' $1').trim()}</h2>
        <form on:submit|preventDefault={handleTrainAndTest} class="form-control">
            {#each classifiers[classificationTask].params as param}
                <div class="mb-4 form-control">
                    <label class="label">
                        <span class="label-text">{param}</span>
                    </label>
                    <input type="text" class="input input-bordered w-full" name={param}/>
                </div>
            {/each}
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        {#if message}
            <div class="alert alert-info mt-4">{message}</div>
        {/if}
    </div>
</div>
