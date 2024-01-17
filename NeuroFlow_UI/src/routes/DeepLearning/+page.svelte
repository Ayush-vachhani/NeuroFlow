<script lang="ts">
    import {onMount} from "svelte";
    import {urls} from "../../stores/urls.js";
    import type {WebSocketEvents} from "vitest";

    let websocket:WebSocket;
    onMount(() => {
        websocket = new WebSocket($urls.torch_socket);
        // while (websocket.readyState !== 1) {
        //     websocket = new WebSocket($urls.torch_socket);
        //     setInterval(1000);
        // }
        websocket.onopen = () => {
            console.log('WebSocket connection established');
        };

        websocket.onmessage = (event:WebSocketEvents) => {
            console.log('WebSocket message received:', event.data);
        };

        websocket.onerror = (error:WebSocketEvents) => {
            console.error('WebSocket error:', error);
        };

        websocket.onclose = (event:WebSocketEvents) => {
            console.log('WebSocket connection closed:', event);
        };
    });
</script>