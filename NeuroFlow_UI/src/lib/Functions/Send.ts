export function trainAndTestModel(websocket: WebSocket, command: string, parameters: object, classifier:string):void {
    console.log('Sending command to train and test model');
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({command, parameters, classifier}));
    } else {
        console.error('WebSocket is not connected');
    }
}
