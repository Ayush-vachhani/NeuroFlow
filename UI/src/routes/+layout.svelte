<script>
    import "../app.pcss";
    import MainNavbar from "$lib/Navbar/MainNavbar.svelte";
</script>

<main class="flex flex-col h-screen">
    <MainNavbar />
    <div class="flex-grow m-4 p-4 border-2">
        <slot/>
    </div>
</main>
