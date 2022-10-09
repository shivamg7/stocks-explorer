# stocks-explorer

# Pre-requisite software
- Postgres 13
- Postgres command line tools *psql*
- Python 3.9
- Node & npm installed

### Dev Environment setup
- Install all python dependencies (recommended to create a virtualenv) `pip install -r requirements.txt`
- Add postgres server configuration to `.env` file
#### Mandatory pre-request for all later steps
- load environment variables from `.env` using `source .env`
- load the virtual environment where python dependecies were installed `source .vent/scripts/activate`

# Database setup
- Using psql
  - `CREATE DATABASE stocks;`
  - if stocks database already exits drop it `DROP DATABASE stocks;` and create afresh
  - connect to stocks database `\c stocks`
- Run: `python scripts/create-ddl.py`
- Using psql
  - Check if tables are created in the database by running `\d stocks` when connected to `stocks` db

# Load stock data
- command `python scripts/stock-data-fetched.py --start_date 09-09-2022`
- validate using `select count(1) from stocks;`


# Start backend
- At project root `python -m uvicorn app.backend.main:app`

# Start the frontend
- Switch to frontend root `cd app/frontend/stock-explorer`
- Start using command `npm run serve`