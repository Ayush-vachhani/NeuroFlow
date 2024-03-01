<script lang="ts">
    import {createEventDispatcher, onMount} from 'svelte';

    export let url: string;

    const dispatch = createEventDispatcher();
    let websocket: WebSocket;

    onMount(() => {
        websocket = new WebSocket(url);

        websocket.onopen = () => {
            console.log('WebSocket connection established');
            dispatch('open', {});
        };

        websocket.onmessage = (event) => {
            console.log('WebSocket message received:', event.data)
            dispatch('message', event.data);
        };

        websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
            dispatch('error', error);
        };

        websocket.onclose = (event) => {
            console.log('WebSocket connection closed:', event);
            dispatch('close', event);
        };
    });


    export const sendMessage = (message: string) => {
        if (websocket && websocket.readyState === WebSocket.OPEN) {
            websocket.send(message);
        } else {
            alert("Websocket is not connected")
        }
    }
</script>