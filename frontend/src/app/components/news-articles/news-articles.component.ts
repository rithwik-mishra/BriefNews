import { CommonModule } from '@angular/common';
import { Component, computed, OnInit, signal } from '@angular/core';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

// Angular Material Imports
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';

import { Article, Topic } from '../../models/article';
import { NewsService } from '../../services/news.service';

@Component({
  selector: 'app-news-articles',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatFormFieldModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatMenuModule,
    MatSnackBarModule
  ],
  templateUrl: './news-articles.component.html',
  styleUrl: './news-articles.component.css'
})
export class NewsArticlesComponent implements OnInit {
  // Signals for reactive state management
  articles = signal<Article[]>([]);
  topics = signal<Topic[]>([]);
  selectedTopic = signal<string>('');
  loading = signal<boolean>(false);
  error = signal<string>('');
  hasLoadedOnce = signal<boolean>(false);
  selectedArticle = signal<Article | null>(null);

  // Computed values
  showEmptyState = computed(() =>
    !this.loading() &&
    this.articles().length === 0 &&
    !this.error() &&
    this.hasLoadedOnce()
  );

  showInitialState = computed(() =>
    !this.loading() &&
    this.articles().length === 0 &&
    !this.error() &&
    !this.hasLoadedOnce()
  );

  constructor(
    private newsService: NewsService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.topics.set(this.newsService.getTopics());
  }

  loadArticles(): void {
    console.log('NewsArticlesComponent: loadArticles() called');
    console.log('NewsArticlesComponent: selectedTopic =', this.selectedTopic());

    this.loading.set(true);
    this.articles.set([]);
    this.error.set('');

    this.newsService.getArticles(this.selectedTopic()).subscribe({
      next: (articles) => {
        console.log('NewsArticlesComponent: Articles loaded successfully:', articles);
        this.articles.set(articles);
        this.loading.set(false);
        this.hasLoadedOnce.set(true);
        this.showSnackBar('Articles loaded successfully!', 'success');
      },
      error: (error) => {
        console.error('NewsArticlesComponent: Error loading articles:', error);
        this.loading.set(false);
        this.hasLoadedOnce.set(true);

        // Handle different types of errors
        if (error.status === 0 || error.status === 503) {
          this.error.set('Unable to connect to the server. Please check your internet connection and try again.');
        } else if (error.status === 404) {
          this.error.set('No articles found for the selected topic.');
        } else {
          this.error.set(error.message || 'An unexpected error occurred while loading articles.');
        }

        this.showSnackBar('Error loading articles. Please try again.', 'error');
      }
    });
  }

  onTopicChange(): void {
    // Don't automatically load articles when topic changes
    // User must click the load button
    this.articles.set([]);
    this.error.set('');
    this.hasLoadedOnce.set(false);
  }

  copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(() => {
      this.showSnackBar('Copied to clipboard!', 'success');
    }).catch(() => {
      this.showSnackBar('Failed to copy to clipboard', 'error');
    });
  }

  private showSnackBar(message: string, type: 'success' | 'error'): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'bottom',
      panelClass: type === 'success' ? ['success-snackbar'] : ['error-snackbar']
    });
  }

  openArticlePopup(article: Article): void {
    this.selectedArticle.set(article);
  }

  closeArticlePopup(): void {
    this.selectedArticle.set(null);
  }
}
