import { writable } from 'svelte/store';
import { browser } from '$app/environment';

type Theme = 'light' | 'dark';

function createThemeStore() {
	const { subscribe, set, update } = writable<Theme>('light');

	return {
		subscribe,
		set,
		toggle: () => update(theme => theme === 'light' ? 'dark' : 'light'),
		init: () => {
			if (browser) {
				const stored = localStorage.getItem('theme') as Theme;
				const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
				const initialTheme = stored || systemPreference;

				set(initialTheme);
				applyTheme(initialTheme);
			}
		}
	};
}

function applyTheme(theme: Theme) {
	if (browser) {
		const root = document.documentElement;
		if (theme === 'dark') {
			root.classList.add('dark');
		} else {
			root.classList.remove('dark');
		}
		localStorage.setItem('theme', theme);
	}
}

export const theme = createThemeStore();

// Apply theme when it changes
theme.subscribe(applyTheme);