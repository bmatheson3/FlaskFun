<script lang="ts">
    import { Button } from "$lib/components/ui/button/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import convergintLogo from '$lib/assets/convergint.png';
   import { goto } from '$app/navigation';

   let errorMessage = false;
    let username = ''; 
    let password = '';  

    const handleSubmit = async () => {
        try {
            console.log("Attempting login with:", { username, password });
            
            const response = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST', 
                headers: {      
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const data = await response.json();
            console.log("Response:", data);
            
            if (data.success) {
                goto('/dashboard');
            } else {
                errorMessage = true;
            }
        } catch(error) {
            console.error('Error fetching data', error);
            errorMessage = true;
        }
    }
</script>
 

<div class="flex justify-center w-full h-screen items-center bg-[#001430]">
    <Card.Root class="justify-center w-full max-w-sm h-100">
        <Card.Header>
            <img class="mb-3 w-40 h-auto" alt="company" src={convergintLogo} />
            {#if errorMessage}
                <div>
                    <p class="text-red-500 text-center">Incorrect login credentials. Please try again.</p>
                </div>
            {/if}
            <Card.Title>Login to your account</Card.Title>
                <Card.Description
                    >Enter your email below to login to your account</Card.Description
                >
        </Card.Header>
        <Card.Content>
            <form on:submit|preventDefault={handleSubmit}>
                <div class="flex flex-col gap-6">
                    <div class="grid gap-2">
                    <Label for="username">Username</Label>
                    <Input bind:value={username} id="username" name="username" type="text" placeholder="user" />
                    </div>
                    <div class="grid gap-2">
                    <div class="flex items-center">
                    <Label for="password" >Password</Label>
                    </div>
                    <Input bind:value={password} id="password" name="password" type="password" required />
                    </div>
                    <Button type="submit" class="w-full convergint-bg mt-2 shadow-[2px_2px_1px_0px_#030708]">Login</Button>
                </div>
            </form>
        </Card.Content>
        <Card.Footer class="flex-col gap-2">
       
        </Card.Footer>
    </Card.Root>
</div>
