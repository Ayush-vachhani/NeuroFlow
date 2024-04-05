<script lang="ts">
    import FileUpload from "$lib/Modals/FileUpload.svelte";
    import {currentFile} from "../../stores/files";


</script>
{#if !$currentFile}
    <FileUpload/>
{:else }
    <slot/>
{/if}
