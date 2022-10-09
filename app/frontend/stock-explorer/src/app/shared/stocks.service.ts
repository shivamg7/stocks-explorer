import { Injectable } from '@angular/core';
import { Stock } from "./stocks";
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class StocksService {

  private _baseUrl: string = "http://localhost:8000";

  constructor(private httpClient: HttpClient) { }

  getStockList(): Observable<Stock[]> {
    const url = `${this._baseUrl}/stocks`;
    return this.httpClient.get<Stock[]>(url);
  }

  getStock(series: string, date: string): Observable<Stock> {
    const url = `${this._baseUrl}/stocks/series`;
    return this.httpClient.get<Stock>(url, {
    params: {
      series: series,
        date: date
    }
    });
  }
}
