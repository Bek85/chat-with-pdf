// import axios from 'axios';
import { writable } from 'svelte/store';
import { api, getErrorMessage } from '$api';

export interface Document {
	id: string;
	file_id: string;
	name: string;
}

interface UploadStore {
	data: Document[];
	error: string;
	uploadProgress: number;
	deletingIds: Set<string>;
}

const INITIAL_STATE = {
	data: [],
	error: '',
	uploadProgress: 0,
	deletingIds: new Set<string>()
};

const documents = writable<UploadStore>(INITIAL_STATE);

const set = (val: Partial<UploadStore>) => {
	documents.update((state) => ({ ...state, ...val }));
};

const setUploadProgress = (event: ProgressEvent) => {
	const progress = Math.round((event.loaded / event.total) * 100);

	set({ uploadProgress: progress });
};

const upload = async (file: File) => {
	set({ error: '' });

	try {
		const formData = new FormData();
		formData.append('file', file);

		await api.post('/pdfs', formData, {
			onUploadProgress: setUploadProgress
		});
	} catch (error) {
		return set({ error: getErrorMessage(error) });
	}
};

const getDocuments = async () => {
	const { data } = await api.get('/pdfs');
	set({ data });
};

const deleteDocument = async (id: string) => {
	// Add to deleting set
	documents.update((state) => ({
		...state,
		deletingIds: new Set([...state.deletingIds, id]),
		error: ''
	}));

	try {
		await api.delete(`/pdfs/${id}`);
		// Remove the document from the store and clear deleting state
		documents.update((state) => {
			const newDeletingIds = new Set(state.deletingIds);
			newDeletingIds.delete(id);
			return {
				...state,
				data: state.data.filter((doc) => doc.id !== id),
				deletingIds: newDeletingIds
			};
		});
		return { success: true };
	} catch (error) {
		// Remove from deleting set and set error
		documents.update((state) => {
			const newDeletingIds = new Set(state.deletingIds);
			newDeletingIds.delete(id);
			return {
				...state,
				deletingIds: newDeletingIds,
				error: getErrorMessage(error)
			};
		});
		return { success: false, error: getErrorMessage(error) };
	}
};

const clearErrors = () => {
	set({ error: '', uploadProgress: 0 });
};

export { upload, getDocuments, documents, clearErrors, deleteDocument };
