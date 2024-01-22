<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import {urls} from "$lib/stores/urls.ts";
    import type {WebSocketEvents} from "vitest"
    import {trainAndTestModel} from "$lib/Functions/Send";
    import ClassificationSideBar from "$lib/ClassificationSideBar.svelte";
    import {classifiers} from "$lib/Shared/BinaryClassifiers";
    import WebSocketComponent from "$lib/WebSocketHandler/WebSocketComponent.svelte";
    let websocket: WebSocket;
    let message:string = null;

    let classificationTask = 'RandomForest';


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
<!--<WebSocketComponent bind:websocket={websocket} url={$urls.scikitlearn_socket}/>-->
<div class="flex h-screen">
    <ClassificationSideBar bind:{classificationTask} = {classificationTask}/>
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
