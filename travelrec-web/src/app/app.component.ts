import { Component, ViewChild, ElementRef } from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';
import { HttpClient } from '@angular/common/http';
import { environment } from './../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'travelrec-web';

  @ViewChild('queryInput') queryInput: ElementRef;

  recommendations = [];
  query: string;

  constructor(
    private spinner: NgxSpinnerService,
    private http: HttpClient
  ) { }

  search() {
    this.spinner.show();
    if (this.query !== '') {
      this.http.get(environment.apiUrl + 'recommendations/' + this.query).subscribe((res: any[]) => {
        this.recommendations = res;
      },
        () => { },
        () => this.spinner.hide());
    }
  }
}
