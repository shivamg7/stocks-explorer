# stocks-explorer

# Pre-requisite software
- Postgres 13
- Postgres command line tools *psql*
- Python 3.9
- Node & npm installed

### Dev Environment setup
- Install all python dependencies (recommended to create a virtualenv) `pip install -r requirements.txt`
- Add/Change postgres server configuration to `.env` file
#### Mandatory pre-request for all later steps
- load environment variables from `.env` using `source .env`
- load the virtual environment where python dependecies were installed `source .vent/scripts/activate`

# Database setup
- Using psql
  - `CREATE DATABASE stocks;`
  - if stocks database already exits drop it `DROP DATABASE stocks;` and create afresh
  - connect to stocks database `\c stocks`
- Run: `python app/scripts/create-ddl.py`
- Using psql
  - Check if tables are created in the database by running `\d stocks` when connected to `stocks` db

# Load stock data
- command `python app/scripts/stock-data-fetcher.py --start_date 09-09-2022`
- validate using `select count(1) from stocks;`


# Start webserver
- At project root `python -m uvicorn app.backend.main:app`
- Navigate to `http://localhost:8000/` on any webbrowser


### Notes:
- Both frontend & backend are served using a single app
- To start the frontend using angular (for development changes)
  - At frontend root `cd app/frontend/stock-explorer`
  - Use command `npm run start`
  - When done making changes publish changes to production app using `npm run build`
  - Be sure to add new files generated to git using `git add`