# Data_Ingestion_manipulation_workflow_Lab

## Setup

```
$ uv init
$ uv sync
```

## Data Quality Checks Rules

**Accept**

- Correct data is accepted.

**Transform**

- Incorrect data in forms of datatype, space e.g is transformed without changing the _meaning_ of the data.

**Flag**

- The data that _could_ be wrong is flagged.
- It is excludet from the calculations

**Reject**

- Invalid data (e.g where obligated fields are missing) is rejeted and stored in a file: _rejected_products.csv_

## CSV - File Structure

### products_csv

- Contains the original raw product data

### analytics_summary.csv

- After transforming the data the file includes these conditions:
  - mean_price
  - median_price
  - num_of_products
  - num_of_missing_price

### flagged_products.csv

- Contains the products that has been flagged
- Flags:
  - missing_currency (has no currency)
  - missing_date (has no date)
  - missing_price (has no price)
  - low_price (Price = 0)
  - luxury_products (over 4000 SEK)

### rejected_producs.csv

- Contains invalid data based on conditions:
  - missing id
  - missing price
  - negative price
  - missing currency

### top_10_products

- Contains the top 10 expensive products from the valid dataset.

### deciant_prices.csv

- Contains the deviant prices based on conditions:
  - negative_prices (below 0)
  - cheap_products (under 10 SEK)
  - expensive products (products over 20.000 SEK)
  - missing_price (products without a price - NaN)

## Data Pipeline Theory

### 1.Ingest

Importation, transfer and loading of raw data from external sources (e.g. app, databse, API) for further analytics.

**My project**:

- ingested through pandas in python with read_csv

```python
products = pd.read_csv("products.csv", sep=";")
```

### 2.Storage

Saves data in a place where is it possible to use several times. The data can be housed in lakes, warehouses and lakehouses.

**Exampel:** Save in postgreSQL

**My project**:

- Stored the data through pandas to_csv

```python
top_10_products.to_csv("top_10_products.csv", index=False)
```

### 3.Transform

Transoformation of the data includes cleaning, convert and analysis to be able to use it for analytical purpuse such as BI.

```python
products["currency"] = products["currency"].str.strip()

```

**My project**:

- Through converting, tonumeric(), isna(), replace(), strip() and other methods I have cleaned and transformed the data.

### 4.Acesss

The data is delivered for usage such as - as raports, dashboards or files (Open the file to see the result and use it).

## Technologies

### PsycoPg3

Psycopg3 works as a bridge between Python and PostgreSQL. It is used to translate Python-code and PostgreSQL-databse so they are able to communicate with each other.

### Pandas

Pandas is a Python libary for working with data sets. Functions for analysing, cleaning, converting, exporting, reading and more is avalible.

### Pydantic

Pydantic is a Python libary used for data validation (define and structure data).

Exampel of this is BaseModel.

## ETL Process Theory

### 1.Extract

- Retrieves the data from different sources - this is the rawdata without changes.

### 2.Transform

- clean, reshape, standardize data so that it can be trusted and used / analyzed.

### 3.Load

- Save the data after the transformatio. The calculation is the load and resultes in the cleaned data.
