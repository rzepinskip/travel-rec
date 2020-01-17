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
  @ViewChild('lgModal') lgModal: any;

  recommendations = [];
  errorMessage = null;
  detailsList = [];
  modalName = '';
  query: string;

  constructor(
    private spinner: NgxSpinnerService,
    private http: HttpClient
  ) { }

  search() {
    this.spinner.show();
    this.recommendations = [];
    this.errorMessage = null;
    if (this.query !== '') {
      this.http.get(environment.apiUrl + 'recommendations/' + this.query).subscribe((res: any[]) => {
        if (!Array.isArray(res)) {
          this.errorMessage = res;
        } else {
          this.recommendations = res;
        }
      },
        () => { },
        () => this.spinner.hide());
    }
  }

  openDetailsList(city_name, rec: any[]) {
    this.modalName = city_name;
    this.detailsList = rec;
    this.lgModal.show();

    return false;
  }

  wktToGoogleMapsSearchString(wkt: string) {
    const coords = wkt.substring(wkt.indexOf('(') + 1, wkt.lastIndexOf(')'));
    const coordsTab = coords.split(' ');
    return coordsTab[1] + ' ' + coordsTab[0];
  }
}
