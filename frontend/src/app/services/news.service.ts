import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Article, Topic } from '../models/article';

@Injectable({
  providedIn: 'root'
})
export class NewsService {
  private apiBaseUrl = 'https://briefnews.onrender.com';

  constructor(private http: HttpClient) { }

  getArticles(topic?: string): Observable<Article[]> {
    let url = `${this.apiBaseUrl}/articles`;
    if (topic) {
      url += `?topic=${topic}`;
    }

    console.log('NewsService: Making request to:', url);
    console.log('NewsService: Topic:', topic);

    return this.http.get<Article[]>(url).pipe(
      tap(response => {
        console.log('NewsService: Response received:', response);
      }),
      catchError(this.handleError)
    );
  }

  getTopics(): Topic[] {
    return [
      { value: 'business', label: 'Business' },
      { value: 'technology', label: 'Technology' },
      { value: 'science', label: 'Science' },
      { value: 'health', label: 'Health' },
      { value: 'politics', label: 'Politics' }
    ];
  }

  private handleError(error: HttpErrorResponse) {
    console.error('News service error:', error);
    console.error('Error status:', error.status);
    console.error('Error message:', error.message);
    console.error('Error URL:', error.url);

    let errorMessage = 'An error occurred while loading articles.';

    if (error.status === 0) {
      errorMessage = 'Unable to connect to the server. Please check your internet connection and try again.';
    } else if (error.status === 404) {
      errorMessage = 'No articles found for the selected topic.';
    } else if (error.status === 503) {
      errorMessage = 'The server is temporarily unavailable. Please try again later.';
    } else if (error.status >= 500) {
      errorMessage = 'Server error. Please try again later.';
    } else if (error.status >= 400) {
      errorMessage = 'Invalid request. Please check your input and try again.';
    }

    return throwError(() => new Error(errorMessage));
  }
}
