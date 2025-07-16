<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { goto } from '$app/navigation';
  import logo from '$lib/assets/splash.avif';
</script>

<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
	

<div class="w-screen h-screen mx-auto flex justify-center bg-[#030708]">
        
        <img class="object-contain brightness-40 shadow-[5px_5px_1000px_-1px_ #010101]" alt="The project logo" src={logo} />

		<div class="">
			<h1 class="indexHeading text-center sm:text-left sm:text-6xl absolute top-2/5 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white drop-shadow-[0_0_8px_rgba(0,0,0,1)]">Welcome to Convergint</h1>
		</div>
        <h2 class="text-center sm:text-left sm:text-2xl absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white drop-shadow-[0_0_8px_rgba(0,0,0,1)]">Manage your client's passes</h2>
		<div class="absolute top-3/5 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
			<Button class="bg-white px-6 py-6 rounded-xl shadow-[2px_2px_30px_0px_#030708]" onclick={() => goto('/login')}>
				<p class="text-black text-l">Login</p>
			</Button>
		</div>
</div>