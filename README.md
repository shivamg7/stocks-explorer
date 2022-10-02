# stocks-explorer

# Pre-requisite software
- Postgres 13
- Postgres command line tools *psql*
- Python 3.9

### Dev Environment setup
- Install all python dependencies (recommended to create a virtualenv) `pip install -r requirements.txt`
- Add postgres server configuration to `.env` file
- For all new shells load environment variables from `.env` using `source .env`

# Database setup
- Using psql
  - `CREATE DATABASE stocks;`
  - if stocks database already exits drop it `DROP DATABASE stocks;` and create afresh
  - connect to stocks database `\c stocks`
- Run: `python create-ddl.py`
- Using psql
  - Check if tables are created in the database by running `\d stocks` when connected to `stocks` db

# Load stock data
- command `python scripts/stock-data-fetched.py --start_date 09-09-2022`
- validate using `select count(1) from stocks;`
