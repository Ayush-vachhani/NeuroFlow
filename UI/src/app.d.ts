// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {

		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
	interface Flowbite_Select {
		name: string;
		value: string;
	}
	interface DisplayData {
		sample_data: object;
		column_sum: object;
	}
}

export {Flowbite_Select};
