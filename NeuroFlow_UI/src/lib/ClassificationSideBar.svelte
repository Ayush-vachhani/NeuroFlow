<script>
    export let classificationTask;
    import {classifiers} from "$lib/Shared/BinaryClassifiers";
    function handleSelection(classifier) {
        classificationTask = classifier;
    }
</script>

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