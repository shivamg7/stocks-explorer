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
    dateControl: new FormControl(null, [Validators.required])
  })
  yesterdayDate: Date | undefined;
  closingPrice: number | undefined;
  noStockData: boolean;

  constructor(
    private stockService: StocksService
  ) {
    this.title = 'stocks-component';
    this.selectedStock = '';
    this.stocks = [];
    this.closingPrice = undefined;
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
    const date = moment(this.formGroup.get("dateControl")?.value).format('YYYY-MM-DD');
    this.stockService.getStock(symbol, date).subscribe((resp: Stock) => {
      this.closingPrice = resp.closing_price;
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
