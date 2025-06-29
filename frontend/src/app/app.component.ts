import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';

// Angular Material Imports
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';

// Components
import { NewsArticlesComponent } from './components/news-articles/news-articles.component';
import { UrlSummarizerComponent } from './components/url-summarizer/url-summarizer.component';

// Services
import { Theme, ThemeService } from './services/theme.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatCardModule,
    MatTabsModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule,
    NewsArticlesComponent,
    UrlSummarizerComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit, OnDestroy {
  public currentTheme: Theme = 'dark';
  private readonly destroy$ = new Subject<void>();

  constructor(private themeService: ThemeService) { }

  ngOnInit(): void {
    this.themeService.theme$
      .pipe(takeUntil(this.destroy$))
      .subscribe(theme => {
        this.currentTheme = theme;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  public toggleTheme(): void {
    this.themeService.toggleTheme();
  }

  public getThemeIcon(): string {
    return this.currentTheme === 'light' ? 'dark_mode' : 'light_mode';
  }

  public getThemeTooltip(): string {
    return this.currentTheme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode';
  }
}
