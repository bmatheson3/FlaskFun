 <script lang="ts">
    import { onMount } from 'svelte';
    let loading = false;

    const fetch_template = async () => {
        try{
            console.log("fetching template");
            const response = await fetch('http://127.0.0.1:5000/email_template', {
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
        const response = await fetch('http://127.0.0.1:5000/test_session', {
            credentials: 'include'
        });
        const data = await response.json();
        console.log('Session test:', data);
    }   

    onMount(async () => {
        loading = true;
        await testSession();
        let data = await fetch_template()
        loading = false;
  });
</script>