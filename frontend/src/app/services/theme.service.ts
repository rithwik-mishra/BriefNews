import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export type Theme = 'light' | 'dark';

@Injectable({
    providedIn: 'root'
})
export class ThemeService {
    private readonly THEME_KEY = 'briefnews-theme';
    private readonly themeSubject = new BehaviorSubject<Theme>('dark');

    public readonly theme$: Observable<Theme> = this.themeSubject.asObservable();

    constructor() {
        this.initializeTheme();
    }

    private initializeTheme(): void {
        const savedTheme = localStorage.getItem(this.THEME_KEY) as Theme;
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        const initialTheme: Theme = savedTheme || (prefersDark ? 'dark' : 'light');
        this.setTheme(initialTheme);
    }

    public getCurrentTheme(): Theme {
        return this.themeSubject.value;
    }

    public toggleTheme(): void {
        const currentTheme = this.getCurrentTheme();
        const newTheme: Theme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    public setTheme(theme: Theme): void {
        this.themeSubject.next(theme);
        localStorage.setItem(this.THEME_KEY, theme);
        this.applyTheme(theme);
    }

    private applyTheme(theme: Theme): void {
        const root = document.documentElement;
        root.setAttribute('data-theme', theme);

        // Update Material theme based on mode
        const materialTheme = this.getMaterialTheme(theme);
        this.loadMaterialTheme(materialTheme);
    }

    private getMaterialTheme(theme: Theme): string {
        // Use different Material themes for light and dark modes
        switch (theme) {
            case 'light':
                return 'indigo-pink'; // Light theme with indigo-pink palette
            case 'dark':
                return 'rose-red'; // Dark theme with rose-red palette
            default:
                return 'indigo-pink';
        }
    }

    private loadMaterialTheme(theme: string): void {
        const existingLink = document.getElementById('material-theme-link');
        if (existingLink) {
            existingLink.remove();
        }

        const link = document.createElement('link');
        link.id = 'material-theme-link';
        link.rel = 'stylesheet';
        link.href = `@angular/material/prebuilt-themes/${theme}.css`;
        document.head.appendChild(link);
    }
} 