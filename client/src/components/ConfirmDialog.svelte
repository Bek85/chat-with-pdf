<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import Icon from './Icon.svelte';

	export let show = false;
	export let title = 'Confirm Action';
	export let message = 'Are you sure you want to proceed?';
	export let confirmText = 'Confirm';
	export let cancelText = 'Cancel';
	export let loading = false;

	const dispatch = createEventDispatcher();

	const handleConfirm = () => {
		if (!loading) {
			dispatch('confirm');
		}
	};

	const handleCancel = () => {
		if (!loading) {
			dispatch('cancel');
		}
	};

	const handleKeydown = (event: KeyboardEvent) => {
		if (event.key === 'Escape' && !loading) {
			handleCancel();
		}
	};

	onMount(() => {
		if (show) {
			window.addEventListener('keydown', handleKeydown);
			return () => window.removeEventListener('keydown', handleKeydown);
		}
	});

	$: if (show) {
		window.addEventListener('keydown', handleKeydown);
	} else {
		window.removeEventListener('keydown', handleKeydown);
	}
</script>

{#if show}
	<!-- Backdrop -->
	<div
		class="fixed inset-0 z-40 bg-black bg-opacity-50 flex items-center justify-center p-4"
		on:click={handleCancel}
		on:keydown={handleKeydown}
	>
		<!-- Dialog -->
		<div
			class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4 transform transition-all"
			on:click|stopPropagation
			on:keydown|stopPropagation
		>
			<!-- Header -->
			<div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
				<div class="flex items-center justify-between">
					<h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
						{title}
					</h3>
					{#if !loading}
						<button
							class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
							on:click={handleCancel}
						>
							<Icon name="close" size="24px" />
						</button>
					{/if}
				</div>
			</div>

			<!-- Content -->
			<div class="px-6 py-4">
				<p class="text-gray-700 dark:text-gray-300">
					{message}
				</p>
			</div>

			<!-- Actions -->
			<div class="px-6 py-4 bg-gray-50 dark:bg-gray-700 rounded-b-lg flex justify-end gap-3">
				<button
					class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-600 border border-gray-300 dark:border-gray-500 rounded-md hover:bg-gray-50 dark:hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
					on:click={handleCancel}
					disabled={loading}
				>
					{cancelText}
				</button>
				<button
					class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
					on:click={handleConfirm}
					disabled={loading}
				>
					{#if loading}
						<div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
					{/if}
					{confirmText}
				</button>
			</div>
		</div>
	</div>
{/if}