 <script lang="ts">
    import { onMount } from 'svelte';
    import { Button } from "$lib/components/ui/button/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import { Textarea } from "$lib/components/ui/textarea/index.js"

    let loading = false;
    let formSubmitted = false;
    let subject = '';
    let content= '';
    let banner_url = '';
    let errorMessage = false;
    let existing_subject = '';
    let existing_content = '';
    let existing_banner_url = '';
    

    const fetch_template = async () => {
        try{
            console.log("fetching template");
            const response = await fetch('http://localhost:5000/email_template', {
                credentials: 'include'
            });
            const data = await response.json();
            console.log(data)

            return data;
        } catch(error){
            console.error('Error fetching data', error);
        }
    }

    const testSession = async () => {
        const response = await fetch('http://localhost:5000/test_session', {
            credentials: 'include'
        });
        const data = await response.json();
        console.log('Session test:', data);
    }   

    const handleSubmit = async () => {
        try {
            const response = await fetch('http://localhost:5000/email_template', {
                method: 'POST', 
                headers: {      
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    subject: subject,
                    content: content,
                    banner_url: banner_url
                })
            });
            
            const data = await response.json();
            console.log("Response:", data);
            
            if (data.success) {
                formSubmitted = true;
                window.alert("Welcome email updated!")
            } else {
                errorMessage = true;
            }
        } catch(error) {
            console.error('Error fetching data', error);
            errorMessage = true;
        }
    }

    onMount(async () => {
        loading = true;
        await testSession();
        let data = await fetch_template()
        subject = data.subject;
        content = data.content;
        banner_url = data.banner_url;
        loading = false;
  });
</script>
<div class="m-10">
    <h1 class="text-4xl font-bold">Your Insights</h1>
    <div class="my-5 flex">
        <form on:submit|preventDefault={handleSubmit}>
            <div>
                <div class="grid gap-2">
                    <Label for="banner_url">Banner Url</Label>
                    <Input bind:value={banner_url} id="banner_url" name="banner_url" type="text" class="w-80"/>
                </div>
                <div class="grid gap-2 mt-3">
                    <Label for="subject">Email Subject</Label>
                    <Input bind:value={subject} id="subject" name="subject" type="text" class="w-300"></Input>
                </div>

                <div class="grid gap-2 mt-3">
                    <Label for="content">Email Content</Label>
                    <Textarea bind:value={content} id="content" name="content" class="w-300 h-40"></Textarea>
                </div>
                <div class="flex justify-end">
                    <Button type="submit" class="w-full convergint-bg mt-2 shadow-[2px_2px_1px_0px_#030708] mt-3 w-100">Submit</Button>
                </div>
            </div>
        </form>
    </div>
</div>