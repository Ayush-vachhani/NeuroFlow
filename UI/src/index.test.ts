import {describe, it, expect} from "vitest";
// Assuming handleMessage updates some visible text or state in the component
import {render} from '@testing-library/svelte';
import Page from './+page.svelte';

describe('Page Component', () => {
	it('updates data correctly', async () => {
		const {component, getByText} = render(Page);
		
		// Assuming updateData can be called directly for the sake of this example
		component.updateData({
			epoch: 1,
			trainAccuracy: 90,
			testAccuracy: 85,
			loss: 0.1
		});
		
		// Attempt to get the text, will throw an error if not present
		const updatedText = getByText('Epoch: 1, Train Accuracy: 90');
		
		// If getByText does not throw, the text is in the document
		expect(updatedText).toBeTruthy();
	});
});

