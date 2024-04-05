<script lang="ts">
    import {onMount, createEventDispatcher} from "svelte";

    import {Button, Modal, Helper, Fileupload, Label, Select} from 'flowbite-svelte';
    import {setCurrentFile, setFiles, addFile} from "../../stores/files";
    import axios from "axios";

    let uploaded_file_value:FileList;
    let uploaded_file_name:string;
    let selected_file:any ;

    let file_names:Flowbite_Select[] = [];
    let open = true ;

    const dispatch = createEventDispatcher();

    onMount(async () => {
        const fetchFiles = await axios.get('http://localhost:8000/api/files');
        setFiles(fetchFiles.data['files']);
        file_names = fetchFiles.data['files'].map((filename:string) => ({
            name: filename,
            value: filename
        }));
    });
    async function handleFileSubmit(event:Event) {
        uploaded_file_name = uploaded_file_name.replace('C:\\fakepath\\','');
        if (selected_file === '' && uploaded_file_value){
            await axios.put('http://localhost:8000/api/files', uploaded_file_value);
            setCurrentFile(uploaded_file_name);
            addFile(uploaded_file_name);
        }
        else if (selected_file){
            setCurrentFile(selected_file);
        }
        // dispatch('close', {})
    }
</script>

<Modal bind:open={open} size="xs"  class="w-full">
    <form class="flex flex-col space-y-6" on:submit|preventDefault={handleFileSubmit}>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Select File</h3>
        <Label>
            Select existing file
            <Select class="mt-2" items={file_names}  bind:value={selected_file}/>
        </Label>
        <Label class="space-y-2 mb-2">
            <span>Or Upload file</span>
            <Fileupload bind:files={uploaded_file_value} bind:value={uploaded_file_name}/>
            <Helper>CSV, XLSX, JSON.</Helper>
        </Label>
        <Button type="submit" class="w-full1">Start Training</Button>
    </form>
</Modal>