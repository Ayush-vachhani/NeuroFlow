<script>
    import Circle from "$lib/SVG/Shapes/Circle.svelte";
    //Child circle components
    export let No_of_Circles = 5;
    export let width = 120;
    let rectangle_height = 50 * No_of_Circles;
    //Reactive statements
    $:No_of_Circles;
    $:rectangle_height = 50 * No_of_Circles;

</script>

<svg width={width} height={rectangle_height + 20}>
    <rect x="10" y="15" width="100" height={rectangle_height} stroke="black" fill="none" stroke-width="1"/>
    {#each Array.from({ length: No_of_Circles }) as _, i}
        <Circle cx={60} cy={40 + 50*i } r="20" />
    {/each}
</svg>
