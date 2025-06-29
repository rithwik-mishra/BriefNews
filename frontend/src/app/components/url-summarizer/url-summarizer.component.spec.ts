import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SummarizerService } from '../../services/summarizer.service';
import { UrlSummarizerComponent } from './url-summarizer.component';

describe('UrlSummarizerComponent', () => {
    let component: UrlSummarizerComponent;
    let fixture: ComponentFixture<UrlSummarizerComponent>;
    let summarizerService: SummarizerService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [
                UrlSummarizerComponent,
                HttpClientTestingModule,
                MatSnackBarModule,
                BrowserAnimationsModule,
                ReactiveFormsModule
            ],
            providers: [SummarizerService]
        })
            .compileComponents();

        fixture = TestBed.createComponent(UrlSummarizerComponent);
        component = fixture.componentInstance;
        summarizerService = TestBed.inject(SummarizerService);
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should initialize with empty summary result', () => {
        expect(component.summaryResult()).toBe('');
    });

    it('should initialize with empty error', () => {
        expect(component.error()).toBe('');
    });

    it('should initialize with summarizing as false', () => {
        expect(component.summarizing()).toBeFalse();
    });

    it('should have a form with url control', () => {
        expect(component.urlForm.get('url')).toBeTruthy();
    });

    it('should validate required url field', () => {
        const urlControl = component.urlForm.get('url');
        expect(urlControl?.errors?.['required']).toBeTruthy();
    });
}); 