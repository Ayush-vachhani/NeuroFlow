<script lang="ts">
    import type { PageData } from '../../../../.svelte-kit/types/src/routes';
    export let data: PageData;
    const {files} = data
    console.log(files);
</script>