import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { SummarizerService } from './summarizer.service';

describe('SummarizerService', () => {
    let service: SummarizerService;
    let httpMock: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
            providers: [SummarizerService]
        });
        service = TestBed.inject(SummarizerService);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should summarize URL', () => {
        const testUrl = 'https://example.com/article';
        const mockSummary = 'This is a test summary of the article.';

        service.summarizeUrl(testUrl).subscribe(summary => {
            expect(summary).toEqual(mockSummary);
        });

        const req = httpMock.expectOne('https://briefnews.onrender.com//summarize');
        expect(req.request.method).toBe('POST');
        expect(req.request.body).toEqual({ url: testUrl });
        req.flush(mockSummary);
    });
}); 