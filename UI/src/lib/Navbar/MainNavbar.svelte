<script>
    import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
    import { DarkMode } from 'flowbite-svelte';
    import Drawer from "$lib/Drawer.svelte";
</script>

<Navbar let:NavContainer color="gray">
    <NavContainer class="border px-5 py-2 rounded-lg bg-white dark:bg-gray-600">
        <NavBrand>
            <Drawer/>
            <img src="/Neural-Flow-logo.webp" class="me-3 h-6 sm:h-9" alt="NeuroFlow" />
            <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">MetaData</span>
        </NavBrand>
        <NavHamburger/>
        <NavUl>
            <NavLi href="/">Home</NavLi>
        </NavUl>
            <DarkMode class="text-primary-500 dark:text-primary-600 border dark:border-gray-800"/>
    </NavContainer>
</Navbar>
<slot/>