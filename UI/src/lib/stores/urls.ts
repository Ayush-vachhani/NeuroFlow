import {writable, type Writable} from "svelte/store";

export const urls: Writable<{
	scikitlearn_socket: string;
	torch_socket: string;
}> = writable({
	scikitlearn_socket: "ws://localhost:8000/ws/scikit_learn_socket",
	torch_socket: "ws://localhost:8000/ws/NeuralNetworks_socket",
});
