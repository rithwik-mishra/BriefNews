import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Article } from '../models/article';
import { NewsService } from './news.service';

describe('NewsService', () => {
    let service: NewsService;
    let httpMock: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
            providers: [NewsService]
        });
        service = TestBed.inject(NewsService);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should return topics', () => {
        const topics = service.getTopics();
        expect(topics).toBeDefined();
        expect(topics.length).toBeGreaterThan(0);
        expect(topics[0].value).toBeDefined();
        expect(topics[0].label).toBeDefined();
    });

    it('should get articles without topic', () => {
        const mockArticles: Article[] = [
            {
                title: 'Test Article',
                summary: 'Test Summary',
                url: 'https://example.com',
                date: '2024-01-01'
            }
        ];

        service.getArticles().subscribe(articles => {
            expect(articles).toEqual(mockArticles);
        });

        const req = httpMock.expectOne('https://briefnews.onrender.com//articles');
        expect(req.request.method).toBe('GET');
        req.flush(mockArticles);
    });

    it('should get articles with topic', () => {
        const mockArticles: Article[] = [
            {
                title: 'Test Article',
                summary: 'Test Summary',
                url: 'https://example.com',
                date: '2024-01-01'
            }
        ];

        service.getArticles('technology').subscribe(articles => {
            expect(articles).toEqual(mockArticles);
        });

        const req = httpMock.expectOne('https://briefnews.onrender.com//articles?topic=technology');
        expect(req.request.method).toBe('GET');
        req.flush(mockArticles);
    });
}); 