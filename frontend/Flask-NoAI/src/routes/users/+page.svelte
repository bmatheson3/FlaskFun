<script lang="ts">
  import { Button } from "$lib/components/ui/button/index.js";
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import convergintLogo from '$lib/assets/convergint-logo.webp';

  type User = {
    id: number;
    first_name: string;
    last_name: string;
    company: string;
    email: string;
    ph_number: string;
    email_sent: boolean;
    link_sent: boolean;
    security_question: string;
    security_answer: string;
  }

  let loading = true;
  let usersArr: any[][] = [];

  const fetchUsers = async () => {
      try{
          console.log("fetching users");
          const response = await fetch('http://127.0.0.1:5000/get_users');
          const data = await response.json();
          return data;
      } catch(error){
          console.error('Error fetching data', error);
      }
  }

  

  onMount(async () => {
    loading = true;
    usersArr = await fetchUsers()
    loading = false;
  });
 
</script>

<head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>


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
</div>