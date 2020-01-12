import { Component } from '@angular/core';
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

  constructor(
    private spinner: NgxSpinnerService,
    private http: HttpClient
    ) {}

  search() {
    this.spinner.show();
    console.log(environment.apiUrl);
    this.http.get(environment.apiUrl + 'recommendations/Paris').subscribe((res) => {
      console.log(res);
    },
    () => {},
    () => this.spinner.hide());
  }
}
