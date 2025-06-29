import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NewsService } from '../../services/news.service';
import { NewsArticlesComponent } from './news-articles.component';

describe('NewsArticlesComponent', () => {
    let component: NewsArticlesComponent;
    let fixture: ComponentFixture<NewsArticlesComponent>;
    let newsService: NewsService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [
                NewsArticlesComponent,
                HttpClientTestingModule,
                MatSnackBarModule,
                BrowserAnimationsModule
            ],
            providers: [NewsService]
        })
            .compileComponents();

        fixture = TestBed.createComponent(NewsArticlesComponent);
        component = fixture.componentInstance;
        newsService = TestBed.inject(NewsService);
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should initialize with empty articles', () => {
        expect(component.articles()).toEqual([]);
    });

    it('should initialize with topics', () => {
        expect(component.topics().length).toBeGreaterThan(0);
    });

    it('should have initial loading state as false', () => {
        expect(component.loading()).toBeFalse();
    });

    it('should have initial error state as empty', () => {
        expect(component.error()).toBe('');
    });
}); 