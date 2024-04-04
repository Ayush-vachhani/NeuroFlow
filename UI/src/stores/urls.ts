import {readable} from "svelte/store";
import type {Readable} from "svelte/store";
export const urls: Readable<{ scikitlearn_socket: string; torch_socket: string; }> = readable({
	scikitlearn_socket: "ws://localhost:8000/ws/scikit_learn_socket",
	torch_socket: "ws://localhost:8000/ws/NeuralNetworks_socket",
});
