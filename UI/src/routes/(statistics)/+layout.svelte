<script>
    import FileUpload from "$lib/Modals/FileUpload.svelte";
    import {currentFile} from "../../stores/files";
    import axios from "axios";
    async function sample(){
        const response = await axios.post("http://localhost:8000/api/files", {file_name:$currentFile})
        console.log(response.data)
    }
</script>
{#if !$currentFile}
    <FileUpload on:close={sample}/>
{/if}
<slot/>