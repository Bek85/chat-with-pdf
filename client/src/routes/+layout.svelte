<script lang="ts">
	import '../app.css';
	import 'material-icons/iconfont/material-icons.css';
	import { onMount } from 'svelte';
	import Navbar from '$c/Navbar.svelte';
	import ErrorModal from '$c/ErrorModal.svelte';
	import { getUser, auth } from '$s/auth';
	import { theme } from '$s/theme';

	export const ssr = false;

	$: user = $auth.user;

	onMount(() => {
		if (user === null) {
			getUser();
		}
		theme.init();
	});
</script>

<ErrorModal />
<div class="container mx-auto h-screen bg-white dark:bg-gray-900 transition-colors">
	<Navbar />
	<slot />
</div>
