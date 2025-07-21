<script lang="ts">
  import { Button } from "$lib/components/ui/button/index.js";
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import convergintLogo from '$lib/assets/convergint-logo.webp';
  import { Input } from '$lib/components/ui/input/index.js';

  let loading = true;
  let usersArr: any[][] = $state([]);

  const fetchUsers = async () => {
      try{
          console.log("fetching users");
          const response = await fetch('http://localhost:5000/get_users', {
            credentials: 'include',
          });
          const data = await response.json();
          return data;
      } catch(error){
          console.error('Error fetching data', error);
      }
  }

  let files: FileList | undefined = $state();
    
    const handleSubmit = async (event: Event) => {
        event.preventDefault();
        if (!files || files.length === 0) return;
        
        const formData = new FormData();
        formData.append('fileToUpload', files[0]);
        
        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });
            
            if (response.ok) {
                console.log('Upload successful!');
            } else {
                console.error('Upload failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
      
      usersArr = await fetchUsers()
    };


  onMount(async () => {
    loading = true;
    usersArr = await fetchUsers()
    loading = false;
  });
 
</script>

<svelte:head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
</svelte:head>


<div class="m-10 flex-row">
  <h1 class="text-4xl font-bold">Users</h1>
  <h2 class="my-4 text-xl">View the information and status of your users</h2>
  <table class="min-w-full divide-y divide-gray-200 overflow-x-auto border border-gray-300" >
    <thead class="bg-gray-50">
      <tr>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">First Name</th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Name</th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RSVP Email Sent</th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Welcome Email Sent</th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SMS Sent</th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      {#each usersArr as user}
      <tr>
        <td class="px-6 py-4 whitespace-nowrap">{user[1]}</td>
        <td class="px-6 py-4 whitespace-nowrap">{user[2]}</td>
        <td class="px-6 py-4 whitespace-nowrap">{user[3]}</td>
        <td class="px-6 py-4 whitespace-nowrap">{user[4]}</td>
        <td class="px-6 py-4 whitespace-nowrap">{user[5]}</td>
        <td class="px-6 py-4 whitespace-nowrap">{user[6]}</td>
        <td class="px-6 py-4 whitespace-nowrap">{user[7]}</td>
        <td class="px-6 py-4 whitespace-nowrap">{user[8]}</td>
      </tr>
      {/each}
    </tbody>
  </table>
  <div class="grid justify-items-center justify-center mt-8">
    <h1>Upload a file to send out invites!</h1>
        <form onsubmit={handleSubmit} class="grid justify-items-center justify-center">
            <Input
              type="file"
              bind:files
              accept=".xlsx, .xls"
              required
              class="mt-5"
            />
          <Button type="submit" class="mt-4 convergint-bg">Upload</Button>
        </form>
  </div>
</div>