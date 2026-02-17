import pandas as pd


if __name__ == '__main__':
    # Read the csv-file
    products = pd.read_csv("products.csv", sep=";")

    # -----------------------#
    ####### TRANSFORM #######
    # -----------------------#

    # clean the column names
    products.columns = products.columns.str.strip()
    # remove withespace before and after
    # uppercase in the id
    # titles in the names
    # Replacing spaces and -

    products["id"] = products["id"].str.strip().replace(
        " ", "").replace("_", "-").str.upper()

    products["currency"] = products["currency"].str.strip()

    products["name"] = products["name"].str.strip(
    ).str.title().replace(r"\s+", " ", regex=True)

    # Date to the right format
    products["created_at"] = pd.to_datetime(
        products["created_at"], errors="coerce", format="mixed")

    # -----------------------#
    ####### REJECT   #######
    # -----------------------#

    # price that is 0 or negative

    # -----------------------#
    ####### FLAGGING   #######
    # -----------------------#

    # flag for missing currency
    products["missing_currency"] = products["currency"].isna()

    # flag for missing created at
    products["missing_date"] = products["created_at"].isna()

    # flag for missing price
    products["missing_price"] = products["price"].isna()

    print(products.head(20))
