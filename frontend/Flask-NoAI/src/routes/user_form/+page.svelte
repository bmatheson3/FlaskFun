<script lang="ts">
    import { Button } from "$lib/components/ui/button/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import convergintLogo from '$lib/assets/convergint.png';
   import { goto } from '$app/navigation';

   let errorMessage = false;
    let firstName = ''; 
    let phNumber = '';  
    let email = '';
    let company = '';

    const handleSubmit = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/user_form', {
                method: 'POST', 
                headers: {      
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    firstName: firstName,
                    phNumber: phNumber,
                    email: email,
                    company: company
                })
            });
            
            const data = await response.json();
            console.log("Response:", data);
            
            if (data.success) {
                goto('/dashboard'); // need to change
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
    <Card.Root class="justify-center w-full max-w-sm h-200">
        <Card.Header>
            <img class="mb-3 w-40 h-auto" alt="company" src={convergintLogo} />
            {#if errorMessage}
                <div>
                    <p class="text-red-500 text-center">Please enter the email that you're invitation was sent to</p>
                </div>
            {/if}
            <Card.Title>Rsvp Form</Card.Title>
                <Card.Description
                    >Please enter your details to recieve your pass!</Card.Description
                >
        </Card.Header>
        <Card.Content>
            <form on:submit|preventDefault={handleSubmit}>
                <div class="flex flex-col gap-6">
                    <div class="grid gap-2">
                    <Label for="firstName">First Name</Label>
                    <Input bind:value={firstName} id="firstName" name="firstName" type="text" placeholder="John" />
                    </div>
                    <div class="grid gap-2">
                    <Label for="company">Company</Label>
                    <Input bind:value={company} id="company" name="company" type="text" placeholder="Convergint" />
                    </div>
                    <div class="grid gap-2">
                    <Label for="phNumber">Phone Number</Label>
                    <Input bind:value={phNumber} id="phNumber" name="phNumber" type="text" placeholder="+61XXXXXXXXX" />
                    </div>
                    <div class="grid gap-2">
                    <Label for="email">Email</Label>
                    <Input bind:value={email} id="email" name="email" type="text" placeholder="john@doe.com" />
                    </div>
                    <Button type="submit" class="w-full convergint-bg mt-2 shadow-[2px_2px_1px_0px_#030708]">Submit</Button>
                </div>
            </form>
        </Card.Content>
        <Card.Footer class="flex-col gap-2">
       
        </Card.Footer>
    </Card.Root>
</div>
