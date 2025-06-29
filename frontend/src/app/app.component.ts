import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

// Angular Material Imports
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';

// Components
import { NewsArticlesComponent } from './components/news-articles/news-articles.component';
import { UrlSummarizerComponent } from './components/url-summarizer/url-summarizer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatCardModule,
    MatTabsModule,
    MatIconModule,
    NewsArticlesComponent,
    UrlSummarizerComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent { }
