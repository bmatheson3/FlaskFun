<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import SearchIcon from "@lucide/svelte/icons/search";
    import UserIcon from "@lucide/svelte/icons/user";
    import Logout from "@lucide/svelte/icons/log-out";
    import { page } from '$app/stores';
    import { Button } from "$lib/components/ui/button/index.js";
    // Menu items.
    const items = [
        {
        title: "Insights",
        url: "/dashboard",
        icon: SearchIcon,
        },
        {
        title: "Users",
        url: "/users",
        icon: UserIcon,
        },
        {
        title: "Email template",
        url: "#",
        icon: UserIcon,
        }
    ];

    const logout = {       
      title: "Logout",
      url: "/",
      icon: Logout  
    }
    
    $: currentPath = $page.url.pathname;
  
    function isActive(url: string) {
        return currentPath === url || currentPath.startsWith(url + '/');
    }
    </script>
 
<Sidebar.Root collapsible="icon">
  <Sidebar.Content>
    <Sidebar.Group class="flex-1">
      <Sidebar.GroupContent class="flex-1">
        <Sidebar.Menu class="flex-1" >
         <Sidebar.Trigger class="mb-6 hover:bg-gray-200"/>
          {#each items as item (item.title)}
            <Sidebar.MenuItem>
              <Sidebar.MenuButton class="text-lg hover:p-4 hover:transparent" data-active={isActive(item.url)}>
                {#snippet child({ props })}
                  <a href={item.url} {...props}>
                    <item.icon/>
                    <span class="p-6">{item.title}</span>
                  </a>
                {/snippet}
              </Sidebar.MenuButton>
            </Sidebar.MenuItem>
          {/each} 
        </Sidebar.Menu>
      </Sidebar.GroupContent>
    </Sidebar.Group>

    <Sidebar.Group>
        <Sidebar.Menu>
            <Sidebar.MenuItem>
                <Sidebar.MenuButton class="text-lg hover:p-4 hover:transparent self-end">
                {#snippet child({ props })}
                    <a href={logout.url} {...props}>
                        <logout.icon/>
                        <span class="p-6">{logout.title}</span>
                    </a>
                {/snippet}
                </Sidebar.MenuButton>
            </Sidebar.MenuItem>
        </Sidebar.Menu>
    </Sidebar.Group>
    
   
  </Sidebar.Content>
</Sidebar.Root>