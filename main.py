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
    missing_currency = products["currency"].isna()

    # flag for missing created_at
    missing_date = products["created_at"].isna()

    # flag for missing_price
    missing_price = products["price"].isna()

    # flag for low_price 0 or less
    low_price = products["price"] == 0

    # flag for luxury product where price is more than 4000
    luxury_product = products["price"] > 4000

    flag_columns = (
        missing_currency |
        missing_date |
        low_price |
        missing_price |
        luxury_product
    )

    flagged_products = products[flag_columns].copy()

    # add columns for the flagging in the copy of the products

    flagged_products["missing_currency"] = products["currency"].isna()

    flagged_products["missing_date"] = products["created_at"].isna()

    flagged_products["missing_price"] = products["price"].isna()

    flagged_products["low_price"] = products["price"] == 0

    flagged_products["luxury_product"] = products["price"] > 4000

    # -----------------------#
    #######   REJECT   #######
    # -----------------------#

    # Define the rejected data values
    rejected_data = (
        products["id"].isna() |
        products["price"].isna() |
        products["currency"].isna() |
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

    # extract and calculate the top 10 expensive products
    top_10_products = df_valid.sort_values("price", ascending=False).head(10)

    negative_prices = df_rejected[df_rejected["price"] < 0]
    cheap_products = df_valid[df_valid["price"] < 10]
    expensive_products = df_valid[df_valid["price"] > 20000]
    missing_price = products[products["price"].isna()]

    # Slå ihop alla
    deviant_prices = pd.concat([
        negative_prices,
        cheap_products,
        expensive_products,
        missing_price
    ])

    # -----------------------#
    ######   LOAD  ###########
    # -----------------------#

    # to a new csv - file for analytics summary
    analytics_summary.to_csv("analytics_summary.csv", index=False)

    # flagged products csv-file
    flagged_products.to_csv("flagged_products.csv", index=False)

    # Rejected products in a seperate csv file
    rejected_products = df_rejected.to_csv("rejected_products.csv")

    top_10_products.to_csv("top_10_products.csv", index=False)

    deviant_prices.to_csv("deviant_prices.csv", index=False)
