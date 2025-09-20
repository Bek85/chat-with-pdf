<script lang="ts">
	import { theme } from '$s/theme';
	import Icon from './Icon.svelte';

	$: currentTheme = $theme;
</script>

<button
	class="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 transition-colors"
	on:click={theme.toggle}
	title={currentTheme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
>
	{#if currentTheme === 'light'}
		<Icon name="dark_mode" klass="text-gray-600 dark:text-gray-300" />
	{:else}
		<Icon name="light_mode" klass="text-yellow-500" />
	{/if}
</button>