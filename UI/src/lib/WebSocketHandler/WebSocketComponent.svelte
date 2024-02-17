<script lang="ts">
    import { createEventDispatcher, onMount, onDestroy } from 'svelte';
    export let url: string;
    import type {WebSocketEvents} from "vitest";
    
    const dispatch = createEventDispatcher();
    let websocket: WebSocket;

    onMount(() => {
        websocket = new WebSocket(url);

        websocket.onopen = () => {
            console.log('WebSocket connection established');
            dispatch('open', {});
        };

        websocket.onmessage = (event: WebSocketEvents) => {
            console.log('WebSocket message received:', event.data)
            dispatch('message', event.data);
        };

        websocket.onerror = (error: WebSocketEvents) => {
            console.error('WebSocket error:', error);
            dispatch('error', error);
        };

        websocket.onclose = (event: WebSocketEvents) => {
            console.log('WebSocket connection closed:', event);
            dispatch('close', event);
        };
    });
    

    export const sendMessage = (message: string) => {
        if (websocket && websocket.readyState === WebSocket.OPEN) {
            websocket.send(message);
        }
        else{
            alert("Websocket is not connected")
        }
    }
</script>