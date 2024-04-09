<script lang="ts">
    import {onMount} from "svelte";
    import {currentFile} from "../../../stores/files";
    import axios from "axios";
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
    import BarPlot from "$lib/Plots/BarPlot.svelte";

    let sample_data:object ;
    let column_sum_data:object ;
    let tableData: any[] = [];
    let loaded = false;

    async function fetch_data(){
        const response = await axios.post("http://localhost:8000/api/files/", {file_name:$currentFile})
        sample_data = response.data['sample_data']
        column_sum_data = response.data['column_sum_data']

        console.log(column_sum_data)
        if (typeof sample_data === 'string') {
            sample_data = JSON.parse(sample_data);
        }

        const columnNames = Object.keys(sample_data);
        const numRows = sample_data[columnNames[0]].length;

        for (let i = 0; i < numRows; i++) {
            const row = {};
            for (const columnName of columnNames) {
                row[columnName] = sample_data[columnName][i];
            }
            tableData.push(row);
        }

        loaded = true;

    }
    onMount(fetch_data);
    // for (const [key, value] of Object.entries(column_sum_data)) {
    //     console.log(`${key}: ${value}`);
    // }

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
    <div class="flex flex-wrap justify-around">
        {#each Object.entries(column_sum_data) as [columnName, data]}
            <BarPlot chartData={data} title={columnName}/>
        {/each}
    </div>
{/if}


