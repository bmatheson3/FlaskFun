<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { goto } from '$app/navigation';
  import logo from '$lib/assets/splash.avif'

</script>


<div class="mx-auto flex justify-center">
        
        <img class="object-cover" alt="The project logo" src={logo} />

		<div class="">
			<h1 class="text-6xl absolute top-2/5 left-1/2 transform -translate-x-1/2 -translate-y-1/2 ">Welcome to Convergint</h1>
		</div>

        
        <h2 class="text-4xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">Manage your client's passes</h2>
		<div class="absolute top-3/5 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
			<Button class="px-10 py-7 rounded-xl" onclick={() => goto('/users')}>
				<p class="text-xl">Login</p>
			</Button>
		</div>
</div>

