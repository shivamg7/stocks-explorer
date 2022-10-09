import { Component } from '@angular/core';
import { Stock } from './shared/stocks';
import {StocksService} from "./shared/stocks.service";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import * as moment from "moment";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  selectedStock: string;
  title: string;
  stocks: Stock[];

  formGroup: FormGroup = new FormGroup({
    symbolControl: new FormControl(null, [
      Validators.required,
    ]),
    startDate: new FormControl<Date | null>(null),
    endDate: new FormControl<Date | null>(null),
  })
  yesterdayDate: Date | undefined;
  closingPrice: number | undefined;
  noStockData: boolean;
  displayedColumns: string[] = ['date', 'closing_price'];
  stocksTable: Stock[];

  constructor(
    private stockService: StocksService
  ) {
    this.title = 'stocks-component';
    this.selectedStock = '';
    this.stocks = [];
    this.stocksTable = [];
    this.noStockData = false;
  }

  ngOnInit(): void {
    this.stockService.getStockList().subscribe((resp) => {
      this.stocks = resp;
    });
    this.yesterdayDate = this._getYesterdayDate();
    this.formGroup.valueChanges.subscribe(() => {
      this.noStockData = false;
      this.closingPrice = undefined;
    })
  }

  onSubmit(): void {
    const symbol = this.formGroup.get("symbolControl")?.value;
    const startDate = moment(this.formGroup.get("startDate")?.value).format('YYYY-MM-DD');
    const endDate = moment(this.formGroup.get("endDate")?.value).format('YYYY-MM-DD');
    this.stockService.getStock(symbol, startDate, endDate).subscribe((resp: Stock[]) => {
      this.stocksTable = [];
      for (const item of resp) {
        this.stocksTable.push({
          symbol: symbol,
          date: item.date,
          closing_price: item.closing_price
        });
      }
    },
      () => {
      this.noStockData = true;
      });
  }

  private _getYesterdayDate(): Date {
    const dt = new Date();
    dt.setDate(dt.getDate() - 1);
    return dt
  }
}
