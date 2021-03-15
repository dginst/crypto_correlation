from btc_analysis.efficient_frontier import eff_front_op
from btc_analysis.mongo_func import mongo_coll_drop, mongo_upload, query_mongo

mongo_coll_drop("markovitz")

YAHOO_TO_CAPM = ['S&P500',
                 'BTC',
                 'GOLD',
                 'CRUDE OIL',
                 'EUR',
                 'GBP',
                 'EUROSTOXX50',
                 'US TREASURY',
                 'US index',
                 'TESLA',
                 'AMAZON',
                 'APPLE']

# retriving prices and logreturn from MongoDB
all_price_df = query_mongo("btc_analysis", "all_prices_y")
prices = all_price_df[YAHOO_TO_CAPM]

log_ret_df = query_mongo("btc_analysis", "all_logreturns_y")
log_ret = log_ret_df[YAHOO_TO_CAPM]

# computing the optimal allocation with and without BTC
tot_df, comp_tot_df = eff_front_op(
    prices, log_ret, stock_to_remove="BTC")

mongo_upload(tot_df, "collection_CAPM")
mongo_upload(comp_tot_df, "collection_CAPM_no_BTC")
