import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SummarizerService {
  private apiBaseUrl = 'https://briefnews.onrender.com';

  constructor(private http: HttpClient) { }

  summarizeUrl(url: string): Observable<string> {
    return this.http.post(`${this.apiBaseUrl}/summarize`, { url }, { responseType: 'text' }).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    console.error('Summarizer service error:', error);

    let errorMessage = 'An error occurred while summarizing the article.';

    if (error.status === 0) {
      errorMessage = 'Unable to connect to the server. Please check your internet connection and try again.';
    } else if (error.status === 400) {
      errorMessage = 'Unable to crawl this article. Please check the URL and try again.';
    } else if (error.status === 404) {
      errorMessage = 'The requested URL could not be found.';
    } else if (error.status === 503) {
      errorMessage = 'The server is temporarily unavailable. Please try again later.';
    } else if (error.status >= 500) {
      errorMessage = 'Server error. Please try again later.';
    } else if (error.status >= 400) {
      errorMessage = 'Invalid request. Please check the URL and try again.';
    }

    return throwError(() => new Error(errorMessage));
  }
}
