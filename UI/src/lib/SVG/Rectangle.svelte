<script>
    import Circle from "$lib/SVG/Circle.svelte";
    //Child circle components
    export let No_of_Circles = 5;
    export let width = 120;
    let rectangle_height = 50 * No_of_Circles;
    //Reactive statements
    $:No_of_Circles;
    $:rectangle_height = 50 * No_of_Circles;

</script>

<svg height={rectangle_height + 20} width={width}>
    <rect fill="none" height={rectangle_height} stroke="black" stroke-width="1" width="100" x="10" y="15"/>
    {#each Array.from({length: No_of_Circles}) as _, i}
        <Circle cx={60} cy={40 + 50*i } r="20"/>
    {/each}
</svg>
