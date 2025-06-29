import { CommonModule } from '@angular/common';
import { Component, computed, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

// Angular Material Imports
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';

import { SummarizerService } from '../../services/summarizer.service';

@Component({
  selector: 'app-url-summarizer',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatTooltipModule
  ],
  templateUrl: './url-summarizer.component.html',
  styleUrl: './url-summarizer.component.css'
})
export class UrlSummarizerComponent {
  urlForm: FormGroup;

  // Signals for reactive state management
  summaryResult = signal<string>('');
  error = signal<string>('');
  summarizing = signal<boolean>(false);

  // Computed values
  showResult = computed(() => this.summaryResult().length > 0 && !this.error());
  showError = computed(() => this.error().length > 0);
  showInitialState = computed(() =>
    !this.summarizing() &&
    this.summaryResult().length === 0 &&
    !this.error()
  );

  constructor(
    private fb: FormBuilder,
    private summarizerService: SummarizerService,
    private snackBar: MatSnackBar
  ) {
    this.urlForm = this.fb.group({
      url: ['', [Validators.required, Validators.pattern('https?://.+')]]
    });
  }

  summarizeUrl(): void {
    if (this.urlForm.invalid) {
      return;
    }

    this.summarizing.set(true);
    this.summaryResult.set('');
    this.error.set('');

    const url = this.urlForm.get('url')?.value;

    this.summarizerService.summarizeUrl(url).subscribe({
      next: (summary) => {
        this.summaryResult.set(summary);
        this.summarizing.set(false);
        this.showSnackBar('Article summarized successfully!', 'success');
      },
      error: (error) => {
        this.summarizing.set(false);

        // Handle different types of errors
        if (error.status === 0 || error.status === 503) {
          this.error.set('Unable to connect to the server. Please check your internet connection and try again.');
        } else if (error.status === 400) {
          this.error.set('Unable to crawl this article. Please check the URL and try again.');
        } else if (error.status === 404) {
          this.error.set('The requested URL could not be found.');
        } else {
          this.error.set(error.message || 'An unexpected error occurred while summarizing the article.');
        }

        this.showSnackBar('Error summarizing article', 'error');
      }
    });
  }

  clearForm(): void {
    this.urlForm.reset();
    this.summaryResult.set('');
    this.error.set('');
  }

  clearSummary(): void {
    this.summaryResult.set('');
    this.error.set('');
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
}
