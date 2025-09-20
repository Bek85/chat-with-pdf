<script lang="ts">
	import type { PageData } from './$types';
	import AuthGuard from '$c/AuthGuard.svelte';
	import Icon from '$c/Icon.svelte';
	import { deleteDocument } from '$s/documents';

	export let data: PageData;

	const documents = data.documents || [];

	const handleDelete = async (id: string) => {
		if (confirm('Are you sure you want to delete this document?')) {
			await deleteDocument(id);
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
							<tr class="hover:bg-gray-100 dark:hover:bg-gray-700">
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
											class="text-blue-500 hover:text-blue-700 p-1"
											href="/documents/{document.id}"
											title="View document"
										>
											<Icon name="visibility" size="20px" />
										</a>
										<button
											class="text-red-500 hover:text-red-700 p-1"
											on:click={() => handleDelete(document.id)}
											title="Delete document"
										>
											<Icon name="delete" size="20px" />
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
