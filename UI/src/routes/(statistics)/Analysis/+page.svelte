<script lang="ts">
    import {onMount} from "svelte";
    import {currentFile} from "../../../stores/files";
    import axios from "axios";
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';

    let data: any= {}
    let tableData: any[] = [];
    let loaded = false;

    async function fetch_data(){
        const response = await axios.post("http://localhost:8000/api/files/", {file_name:$currentFile})
        data = response.data;
        console.log(data)
        if (typeof data === 'string') {
            data = JSON.parse(data);
        }

        const columnNames = Object.keys(data);
        const numRows = data[columnNames[0]].length;

        for (let i = 0; i < numRows; i++) {
            const row = {};
            for (const columnName of columnNames) {
                row[columnName] = data[columnName][i];
            }
            tableData.push(row);
        }

        loaded = true;

    }
    onMount(fetch_data);

</script>


{#if loaded}
    <Table>
        <TableHead>
            {#each Object.keys(tableData[0]) as column}
                <TableHeadCell>{column}</TableHeadCell>
            {/each}
        </TableHead>
        <TableBody>
            {#each tableData as row}
                <TableBodyRow>
                    {#each Object.values(row) as cell}
                        <TableBodyCell>{cell}</TableBodyCell>
                    {/each}
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
{/if}