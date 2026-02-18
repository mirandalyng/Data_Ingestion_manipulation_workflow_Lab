import pandas as pd


if __name__ == '__main__':
    # Read the csv-file
    products = pd.read_csv("products.csv", sep=";")

    # -----------------------#
    ####### TRANSFORM #######
    # -----------------------#

    # clean the column names
    # remove withespace before and after
    # uppercase in the id
    # titles in the names
    # Replacing spaces and

    products.columns = products.columns.str.strip()

    products["id"] = products["id"].str.strip().replace(
        " ", "").replace("_", "-").str.upper()

    products["currency"] = products["currency"].str.strip()

    products["name"] = products["name"].str.strip(
    ).str.title().replace(r"\s+", " ", regex=True)

    # Date to the right format
    products["created_at"] = pd.to_datetime(
        products["created_at"], errors="coerce", format="mixed")

    # Price to numeric
    products["price"] = pd.to_numeric(products["price"], errors="coerce")

    # -----------------------#
    ####### FLAG  #######
    # -----------------------#

    # flag for missing currency
    products["missing_currency"] = products["currency"].isna()

    # flag for missing created_at
    products["missing_date"] = products["created_at"].isna()

    # flag for missing_price
    products["missing_price"] = products["price"].isna()

    # flag for low_price 0 or less
    products["low_price"] = products["price"] >= 0

    # flag for luxury product where price is more than 4000
    products["luxury_products"] = products["price"] > 4000

    # -----------------------#
    ####### REJECT   #######
    # -----------------------#

    # Define the rejected data values
    rejected_data = (
        products["id"].isna() |
        products["price"].isna() |
        (products["price"] < 0)
    )

    # copy and seperate the rejected and valid data based on T/F
    df_rejected = products[rejected_data].copy()
    df_valid = products[~rejected_data].copy()

    # calculate the data for the analytics summary
    mean_price = df_valid["price"].mean()
    median_price = df_valid["price"].median()
    num_of_products = len(df_valid)
    num_of_missing_price = len(df_rejected["price"])

    # create a dataframe for the analytics summary
    analytics_summary = pd.DataFrame({
        "mean_price": [mean_price],
        "median_price": [median_price],
        "num_of_products": [num_of_products],
        "num_of_missing_price": [num_of_missing_price]
    })

    # read to a new csv - file
    analytics_summary.to_csv("analytics_summary.csv", index=False)

    # extract and calculate the top 10 expensive products
    top_10_products = df_valid.sort_values("price", ascending=False).head(10)

    top_10_invalid_prices = df_rejected.sort_values(
        "price").head(10)

    # Rejected products in a seperate csv file
    rejected_products = df_rejected.to_csv("rejected_products.csv")
