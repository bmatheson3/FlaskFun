
<!-- o Create a landing page that displays the following reports:

§ Number of RSVP emails sent.

§ Number of Welcome emails sent.

§ Number of Secret Question SMS messages sent.

§ Number of Wallet Passes sent via email.

§ Number of Wallet Passes sent via SMS.

o Generate these reports by querying the database -->


<script lang="ts">

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "$lib/components/ui/card/index.js"

import { Button } from "$lib/components/ui/button/index.js";

import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import convergintLogo from '$lib/assets/convergint-logo.webp';
import Icon from "@iconify/svelte"
import calendar from '$lib/assets/calendar.webp';
import security from '$lib/assets/security.jpg';
import wallet from '$lib/assets/wallet-1.png';
import handshake from '$lib/assets/handshake.png';

let loading = true;
let rsvpsSent = '';
let welcomesSent = '';
let questionsSent = '';
let passesSent = '';

  const fetchRsvp = async (): Promise<any> => {
      try{
          console.log("fetching rvsp count");
          const response = await fetch('http://localhost:5000/get_rsvp_emails_sent', {
                credentials: 'include',
          });
          const data = await response.json();
          console.log(data);
          return data;
      } catch(error){
          console.error('Error fetching data', error);
      }
  }
  const fetchWelcome = async (): Promise<any> => {
      try{
          console.log("fetching welcome count");
          const response = await fetch('http://localhost:5000/get_welcome_emails_sent', {
            credentials: 'include',
          });
          const data = await response.json();
          console.log(data);
          return data;
      } catch(error){
          console.error('Error fetching data', error);
      }
  }
  const fetchQuestion = async (): Promise<any> => {
      try{
          console.log("fetching rvsp count");
          const response = await fetch('http://localhost:5000/get_security_sms_sent', {
                credentials: 'include',
          });
          const data = await response.json();
          console.log(data);
          return data;
      } catch(error){
          console.error('Error fetching data', error);
      }
  }
  const fetchPassSent = async (): Promise<any> => {
      try{
          console.log("fetching pass count");
          const response = await fetch('http://localhost:5000/get_links_sent', {
            credentials: 'include',
          });
          const data = await response.json();
          console.log(data);
          return data;
      } catch(error){
          console.error('Error fetching data', error);
      }
  }


    onMount(async () => {
        console.log("Mounting")
        loading = true;
        rsvpsSent = String(await fetchRsvp());
        welcomesSent = String(await fetchWelcome());
        questionsSent = String(await fetchQuestion());
        passesSent = String(await fetchPassSent());
        loading = false;
    });
 </script>




<svelte:head>
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
</svelte:head>


<div class="m-10">
    <h1 class="text-4xl font-bold">Your Insights</h1>
    <div class="my-5 grid grid-cols-4 gap-5">

        <Card>
            <CardHeader class="justify-items-center">
                <CardTitle class=" mt-3 mb-2 text-3xl">RSVP Emails</CardTitle>
                <CardTitle class="text-8xl">{rsvpsSent}</CardTitle>
                <CardDescription class="text-xl">emails sent</CardDescription>
                <div class="dashboard-icon">
                    <img src={calendar} alt='Calendar logo'>
                </div>
                
            </CardHeader>
        </Card>
         <Card>
            <CardHeader class="justify-items-center">
                <CardTitle class=" mt-3 mb-2 text-3xl">Welcome Emails</CardTitle>
                <CardTitle class="text-8xl">{welcomesSent}</CardTitle>
                <CardDescription class="text-xl">emails sent</CardDescription>
                <img src={handshake} alt='Calendar logo'>
            </CardHeader>
        </Card>
          <Card>
            <CardHeader class="justify-items-center">
                <CardTitle class=" mt-3 mb-2 text-3xl">Security Questions</CardTitle>
                <CardTitle class="text-8xl">{questionsSent}</CardTitle>
                <CardDescription class="text-xl">questions sent</CardDescription>
                <img src={security} alt='Calendar logo' class="w-80 h-auto">
            </CardHeader>

            <CardContent class="content-start">

            </CardContent>
        </Card>
          <Card>
            <CardHeader class="justify-items-center">
                <CardTitle class=" mt-3 mb-2 text-3xl">Wallet Passes</CardTitle>
                <CardTitle class="text-8xl">{passesSent}</CardTitle>
                <CardDescription class="text-xl">passes sent</CardDescription>
                <img src={wallet} alt='Calendar logo' class="w-65 h-auto">
            </CardHeader>

            <CardContent class="content-start">

            </CardContent>
        </Card>

        


    </div>
</div>