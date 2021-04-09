from btc_analysis.calc import (
    btc_denominated_total, price_retrieve,
    yahoo_price_fix
)
from btc_analysis.mongo_func import (
    query_mongo, mongo_coll_drop
)
from btc_analysis.config import (
    INDEX_DB_NAME, DB_NAME, WINDOW_LIST)
from btc_analysis.dashboard_func import dash_btc_den_df

# ----------------------------------------------
# price denominated in btc computation

mongo_coll_drop("btc_den")

all_yahoo_price = query_mongo(DB_NAME, "all_prices_y")
yahoo_price_df = yahoo_price_fix(all_yahoo_price)

alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)

btc_denominated_total(yahoo_price_df, alt_price_df)

# --------------
# total btc denominated dataframes for dashboard

dash_btc_den_df(WINDOW_LIST)
