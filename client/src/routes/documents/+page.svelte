<script lang="ts">
	import type { PageData } from './$types';
	import AuthGuard from '$c/AuthGuard.svelte';
	import Icon from '$c/Icon.svelte';
	import ConfirmDialog from '$c/ConfirmDialog.svelte';
	import { deleteDocument, documents as documentsStore } from '$s/documents';

	export let data: PageData;

	let showDeleteDialog = false;
	let documentToDelete: { id: string; name: string } | null = null;

	// Use reactive store data, always prefer store data if available
	$: documents = $documentsStore.data;
	$: isDeleting = documentToDelete && $documentsStore.deletingIds.has(documentToDelete.id);

	// Initialize store with server data
	import { onMount } from 'svelte';
	onMount(() => {
		// Always update the store with the latest server data
		documentsStore.update(state => ({
			...state,
			data: data.documents || [],
			error: '',
			deletingIds: new Set()
		}));
	});

	const handleDeleteClick = (document: { id: string; name: string }) => {
		documentToDelete = document;
		showDeleteDialog = true;
	};

	const handleDeleteConfirm = async () => {
		if (!documentToDelete) return;

		// Close dialog immediately to unblock UI
		showDeleteDialog = false;
		const docToDelete = documentToDelete;
		documentToDelete = null;

		// Start deletion in background
		await deleteDocument(docToDelete.id);
		// User can see progress via table row loading state
		// Errors will be shown in the error toast at bottom of page
	};

	const handleDeleteCancel = () => {
		if (!isDeleting) {
			showDeleteDialog = false;
			documentToDelete = null;
		}
	};
</script>

<AuthGuard />
<div class="flex flex-row justify-between items-center my-4">
	<h2 class="text-3xl font-bold m-2 text-gray-900 dark:text-gray-100">Your Documents</h2>
	<div class="">
		<a
			href="/documents/new"
			class="py-2 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all dark:focus:ring-offset-gray-800"
			>New</a
		>
	</div>
</div>

<div class="flex flex-col">
	<div class="-m-1.5 overflow-x-auto">
		<div class="p-1.5 min-w-full inline-block align-middle">
			<div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
				<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
					<thead class="bg-gray-50 dark:bg-gray-800">
						<tr>
							<th
								scope="col"
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Name</th
							>
							<th
								scope="col"
								class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">ID</th
							>
							<th
								scope="col"
								class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Action</th
							>
						</tr>
					</thead>

					<tbody class="divide-y divide-gray-200 dark:divide-gray-700">
						{#each documents as document}
							{@const isDocumentDeleting = $documentsStore.deletingIds.has(document.id)}
							<tr class="hover:bg-gray-100 dark:hover:bg-gray-700" class:opacity-50={isDocumentDeleting}>
								<td
									class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-gray-200"
									>{document.name}</td
								>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-gray-200"
									>{document.id}</td
								>
								<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
									<div class="flex justify-end gap-2">
										<a
											class="text-blue-500 hover:text-blue-700 p-1 transition-colors"
											href="/documents/{document.id}"
											title="View document"
											class:pointer-events-none={isDocumentDeleting}
											class:opacity-50={isDocumentDeleting}
										>
											<Icon name="visibility" size="20px" />
										</a>
										<button
											class="text-red-500 hover:text-red-700 p-1 transition-colors relative"
											on:click={() => handleDeleteClick(document)}
											title="Delete document"
											disabled={isDocumentDeleting}
											class:opacity-50={isDocumentDeleting}
										>
											{#if isDocumentDeleting}
												<div class="w-5 h-5 border-2 border-red-500 border-t-transparent rounded-full animate-spin"></div>
											{:else}
												<Icon name="delete" size="20px" />
											{/if}
										</button>
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>

<!-- Delete Confirmation Dialog -->
<ConfirmDialog
	bind:show={showDeleteDialog}
	title="Delete Document"
	message={documentToDelete ? `Are you sure you want to delete "${documentToDelete.name}"? This action cannot be undone and will also remove all associated conversations.` : ''}
	confirmText="Delete"
	cancelText="Cancel"
	loading={false}
	on:confirm={handleDeleteConfirm}
	on:cancel={handleDeleteCancel}
/>

<!-- Error Display -->
{#if $documentsStore.error}
	<div class="fixed bottom-4 right-4 z-50">
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded shadow-lg max-w-md">
			<div class="flex items-center justify-between">
				<div class="flex items-center">
					<Icon name="error" size="20px" klass="mr-2" />
					<span class="text-sm">{$documentsStore.error}</span>
				</div>
				<button
					class="ml-4 text-red-500 hover:text-red-700"
					on:click={() => documentsStore.update(state => ({ ...state, error: '' }))}
				>
					<Icon name="close" size="16px" />
				</button>
			</div>
		</div>
	</div>
{/if}
