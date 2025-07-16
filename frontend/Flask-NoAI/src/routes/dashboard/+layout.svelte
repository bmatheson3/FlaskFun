<script lang="ts">
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import AppSidebar from "$lib/components/app-sidebar.svelte";
  import convergintLogo from '$lib/assets/convergint-logo.webp';
  import { Button } from "$lib/components/ui/button/index.js"

 
  let { children } = $props();
</script>
 
<Sidebar.Provider>
  <AppSidebar />
   <Sidebar.Inset>

    <header class="bg-[#0e2b49] px-5 flex flex-row justify-center items-center">
      
        <img class="w-30" alt="company" src={convergintLogo} />
        
    </header>
    <main>
        {@render children?.()}
    </main>
   </Sidebar.Inset>


</Sidebar.Provider>