import pandas as pd
from pymongo import MongoClient

# connecting to mongo in local
# connection = MongoClient("3.138.244.245", 27017)
connection = MongoClient("localhost", 27017)
# creating the database called index
db = connection.btc_analysis

# function that takes as arguments:
# database = database name [index_raw, index_cleaned, index_cleaned]
# collection = the name of the collection of interest
# query_dict = mongo db uses dictionary structure to do query ex:
# {"Exchange" : "kraken", "Pair" : "btcjpy", "Time" : { "$gte": 1580774400} },
#  this query call all the documents that contains kraken as exchange,
#  the pair btcjpy and the time value is greater than 1580774400


def query_mongo(database, collection, query_dict=None):

    # defining the variable that allows to work with MongoDB
    db = connection[database]
    coll = db[collection]

    if query_dict is None:

        df = pd.DataFrame(list(coll.find()))

        try:

            df = df.drop(columns="_id")

        except AttributeError:

            df = []

        except KeyError:

            df = []

    else:

        df = pd.DataFrame(list(coll.find(query_dict)))

        try:

            df = df.drop(columns="_id")

        except AttributeError:

            df = []

        except KeyError:

            df = []

    return df


def mongo_index_conn():

    # connecting to mongo in local
    # connection = MongoClient("3.138.244.245", 27017)
    connection = MongoClient("localhost", 27017)

    db = connection.btc_analysis

    return db


def mongo_indexing():

    db = mongo_index_conn()

    # historical series collections (yahoo)
    db.all_prices.create_index([("id", -1)])
    db.all_returns.create_index([("id", -1)])
    db.all_logreturns.create_index([("id", -1)])
    db.metal_prices.create_index([("id", -1)])
    db.metal_returns.create_index([("id", -1)])

    # return collections
    db.return_various.create_index([("id", -1)])
    db.return_crypto.create_index([("id", -1)])

    # dynamic altcoin correlation collections
    db.dyn_alt_correlation_YTD.create_index([("id", -1)])
    db.dyn_alt_correlation_3Y.create_index([("id", -1)])
    db.dyn_alt_correlation_1Y.create_index([("id", -1)])
    db.dyn_alt_correlation_1Q.create_index([("id", -1)])
    db.dyn_alt_correlation_1M.create_index([("id", -1)])

    # dynamic "Yahoo" correlation collections
    db.dyn_yahoo_correlation_YTD.create_index([("id", -1)])
    db.dyn_yahoo_correlation_3Y.create_index([("id", -1)])
    db.dyn_yahoo_correlation_1Y.create_index([("id", -1)])
    db.dyn_yahoo_correlation_1Q.create_index([("id", -1)])
    db.dyn_yahoo_correlation_1M.create_index([("id", -1)])

    # static altcoin correlation collections
    db.stat_alt_correlation_all.create_index([("id", -1)])
    db.stat_alt_correlation_3Y.create_index([("id", -1)])
    db.stat_alt_correlation_1Y.create_index([("id", -1)])
    db.stat_alt_correlation_1Q.create_index([("id", -1)])
    db.stat_alt_correlation_1M.create_index([("id", -1)])

    # static "yahoo" correlation collections
    db.stat_yahoo_correlation_all.create_index([("id", -1)])
    db.stat_yahoo_correlation_3Y.create_index([("id", -1)])
    db.stat_yahoo_correlation_1Y.create_index([("id", -1)])
    db.stat_yahoo_correlation_1Q.create_index([("id", -1)])
    db.stat_yahoo_correlation_1M.create_index([("id", -1)])

    # dynamic SP500 correlation collections
    db.dyn_SP500_correlation_3Y.create_index([("id", -1)])
    db.dyn_SP500_correlation_1Y.create_index([("id", -1)])
    db.dyn_SP500_correlation_1Q.create_index([("id", -1)])
    db.dyn_SP500_correlation_1M.create_index([("id", -1)])

    # series in BTC price
    db.yahoo_btc_denominated_5Y.create_index([("id", -1)])
    db.altcoin_btc_denominated_5Y.create_index([("id", -1)])
    db.yahoo_btc_denominated_3Y.create_index([("id", -1)])
    db.altcoin_btc_denominated_3Y.create_index([("id", -1)])
    db.yahoo_btc_denominated_2Y.create_index([("id", -1)])
    db.altcoin_btc_denominated_2Y.create_index([("id", -1)])
    db.yahoo_btc_denominated_1Y.create_index([("id", -1)])
    db.altcoin_btc_denominated_1Y.create_index([("id", -1)])
    db.yahoo_btc_denominated_6M.create_index([("id", -1)])
    db.altcoin_btc_denominated_6M.create_index([("id", -1)])
    db.yahoo_btc_denominated_3M.create_index([("id", -1)])
    db.altcoin_btc_denominated_3M.create_index([("id", -1)])
    db.yahoo_btc_denominated_1M.create_index([("id", -1)])
    db.altcoin_btc_denominated_1M.create_index([("id", -1)])
    db.yahoo_btc_denominated_1W.create_index([("id", -1)])
    db.altcoin_btc_denominated_1W.create_index([("id", -1)])
    db.yahoo_btc_denominated_YTD.create_index([("id", -1)])
    db.altcoin_btc_denominated_YTD.create_index([("id", -1)])

    # series USD prices
    db.normalized_prices_5Y.create_index([("id", -1)])
    db.normalized_prices_3Y.create_index([("id", -1)])
    db.normalized_prices_2Y.create_index([("id", -1)])
    db.normalized_prices_1Y.create_index([("id", -1)])
    db.normalized_prices_6M.create_index([("id", -1)])
    db.normalized_prices_3M.create_index([("id", -1)])
    db.normalized_prices_1M.create_index([("id", -1)])
    db.normalized_prices_1W.create_index([("id", -1)])
    db.normalized_prices_YTD.create_index([("id", -1)])

    # volatility
    db.volatility_30.create_index([("id", -1)])
    db.volatility_90.create_index([("id", -1)])
    db.volatility_252.create_index([("id", -1)])

    # market cap
    db.market_cap.create_index([("id", -1)])
    db.btc_supply.create_index([("id", -1)])

    # markovitz
    db.CAPM.create_index([("id", -1)])
    db.CAPM_no_BTC.create_index([("id", -1)])

    # stock to flow
    db.S2F_model.create_index([("id", -1)])


def mongo_coll():

    db = mongo_index_conn()

    dict_of_coll = {

        # yahoo collections
        "collection_prices_y": db.all_prices_y,
        "collection_returns_y": db.all_returns_y,
        "collection_logreturns_y": db.all_logreturns_y,
        "collection_volume_y": db.all_volume_y,


        # return collections
        "collection_ret_var": db.return_various,
        "collection_ret_crypto": db.return_crypto,

        # dynamic altcoins correlation collections
        "collection_YTD_dyn_alt": db.dyn_alt_correlation_YTD,
        "collection_3Y_dyn_alt": db.dyn_alt_correlation_3Y,
        "collection_1Y_dyn_alt": db.dyn_alt_correlation_1Y,
        "collection_1Q_dyn_alt": db.dyn_alt_correlation_1Q,
        "collection_1M_dyn_alt": db.dyn_alt_correlation_1M,

        # dynamic yahoo correlation collections
        "collection_YTD_dyn_yahoo": db.dyn_yahoo_correlation_YTD,
        "collection_3Y_dyn_yahoo": db.dyn_yahoo_correlation_3Y,
        "collection_1Y_dyn_yahoo": db.dyn_yahoo_correlation_1Y,
        "collection_1Q_dyn_yahoo": db.dyn_yahoo_correlation_1Q,
        "collection_1M_dyn_yahoo": db.dyn_yahoo_correlation_1M,

        # static yahoo correlation collections
        "collection_all_stat_yahoo": db.stat_yahoo_correlation_all,
        "collection_3Y_stat_yahoo": db.stat_yahoo_correlation_3Y,
        "collection_1Y_stat_yahoo": db.stat_yahoo_correlation_1Y,
        "collection_1Q_stat_yahoo": db.stat_yahoo_correlation_1Q,
        "collection_1M_stat_yahoo": db.stat_yahoo_correlation_1M,

        # static altcoins correlation collections
        "collection_all_stat_alt": db.stat_alt_correlation_all,
        "collection_3Y_stat_alt": db.stat_alt_correlation_3Y,
        "collection_1Y_stat_alt": db.stat_alt_correlation_1Y,
        "collection_1Q_stat_alt": db.stat_alt_correlation_1Q,
        "collection_1M_stat_alt": db.stat_alt_correlation_1M,

        # dynamic SP500 correlation collections
        "collection_3Y_dyn_SP500": db.dyn_SP500_correlation_3Y,
        "collection_1Y_dyn_SP500": db.dyn_SP500_correlation_1Y,
        "collection_1Q_dyn_SP500": db.dyn_SP500_correlation_1Q,
        "collection_1M_dyn_SP500": db.dyn_SP500_correlation_1M,

        # priced denominated in BTC collections
        "collection_yahoo_btc_den_5Y": db.yahoo_btc_denominated_5Y,
        "collection_alt_btc_den_5Y": db.altcoin_btc_denominated_5Y,
        "collection_yahoo_btc_den_3Y": db.yahoo_btc_denominated_3Y,
        "collection_alt_btc_den_2Y": db.altcoin_btc_denominated_2Y,
        "collection_yahoo_btc_den_2Y": db.yahoo_btc_denominated_2Y,
        "collection_alt_btc_den_3Y": db.altcoin_btc_denominated_3Y,
        "collection_yahoo_btc_den_1Y": db.yahoo_btc_denominated_1Y,
        "collection_alt_btc_den_1Y": db.altcoin_btc_denominated_1Y,
        "collection_yahoo_btc_den_6M": db.yahoo_btc_denominated_6M,
        "collection_alt_btc_den_6M": db.altcoin_btc_denominated_6M,
        "collection_yahoo_btc_den_3M": db.yahoo_btc_denominated_3M,
        "collection_alt_btc_den_3M": db.altcoin_btc_denominated_3M,
        "collection_yahoo_btc_den_1M": db.yahoo_btc_denominated_1M,
        "collection_alt_btc_den_1M": db.altcoin_btc_denominated_1M,
        "collection_yahoo_btc_den_1W": db.yahoo_btc_denominated_1W,
        "collection_alt_btc_den_1W": db.altcoin_btc_denominated_1W,
        "collection_yahoo_btc_den_YTD": db.yahoo_btc_denominated_YTD,
        "collection_alt_btc_den_YTD": db.altcoin_btc_denominated_YTD,

        # normalized prices
        "collection_normalized_prices_5Y": db.normalized_prices_5Y,
        "collection_normalized_prices_3Y": db.normalized_prices_3Y,
        "collection_normalized_prices_2Y": db.normalized_prices_2Y,
        "collection_normalized_prices_1Y": db.normalized_prices_1Y,
        "collection_normalized_prices_6M": db.normalized_prices_6M,
        "collection_normalized_prices_3M": db.normalized_prices_3M,
        "collection_normalized_prices_1M": db.normalized_prices_1M,
        "collection_normalized_prices_1W": db.normalized_prices_1W,
        "collection_normalized_prices_YTD": db.normalized_prices_YTD,

        # volatility
        "collection_volatility_252": db.volatility_252,
        "collection_volatility_90": db.volatility_90,
        "collection_volatility_30": db.volatility_30,

        # market cap
        "collection_market_cap": db.market_cap,
        "collection_btc_supply": db.btc_supply,

        # markovitz
        "collection_CAPM": db.CAPM,
        "collection_CAPM_no_BTC": db.CAPM_no_BTC,

        # stock to flow
        "collection_S2F": db.S2F_model,

    }

    return dict_of_coll


def mongo_coll_drop(corr_type):

    db = mongo_index_conn()

    if corr_type == "static_alt":

        db.stat_alt_correlation_all.drop()
        db.stat_alt_correlation_3Y.drop()
        db.stat_alt_correlation_1Y.drop()
        db.stat_alt_correlation_1Q.drop()
        db.stat_alt_correlation_1M.drop()

    elif corr_type == "static_var":

        db.stat_var_correlation_all.drop()
        db.stat_var_correlation_3Y.drop()
        db.stat_var_correlation_1Y.drop()
        db.stat_var_correlation_1Q.drop()
        db.stat_var_correlation_1M.drop()

    elif corr_type == "static_yahoo":

        db.stat_yahoo_correlation_all.drop()
        db.stat_yahoo_correlation_3Y.drop()
        db.stat_yahoo_correlation_1Y.drop()
        db.stat_yahoo_correlation_1Q.drop()
        db.stat_yahoo_correlation_1M.drop()

    elif corr_type == "dynamic_var":

        db.dyn_var_correlation_3Y.drop()
        db.dyn_var_correlation_1Y.drop()
        db.dyn_var_correlation_1Q.drop()
        db.dyn_var_correlation_1M.drop()

    elif corr_type == "dynamic_yahoo":

        db.dyn_yahoo_correlation_YTD.drop()
        db.dyn_yahoo_correlation_3Y.drop()
        db.dyn_yahoo_correlation_1Y.drop()
        db.dyn_yahoo_correlation_1Q.drop()
        db.dyn_yahoo_correlation_1M.drop()

    elif corr_type == "dynamic_SP500":

        db.dyn_SP500_correlation_3Y.drop()
        db.dyn_SP500_correlation_1Y.drop()
        db.dyn_SP500_correlation_1Q.drop()
        db.dyn_SP500_correlation_1M.drop()

    elif corr_type == "dynamic_alt":

        db.dyn_alt_correlation_YTD.drop()
        db.dyn_alt_correlation_3Y.drop()
        db.dyn_alt_correlation_1Y.drop()
        db.dyn_alt_correlation_1Q.drop()
        db.dyn_alt_correlation_1M.drop()

    elif corr_type == "return_alt":

        db.return_crypto.drop()

    elif corr_type == "return_var":

        db.return_various.drop()

    elif corr_type == "yahoo":

        db.all_returns_y.drop()
        db.all_prices_y.drop()
        db.all_logreturns_y.drop()
        db.all_volume_y.drop()

    elif corr_type == "bloom":

        db.all_returns.drop()
        db.all_prices.drop()
        db.all_logreturns.drop()

    elif corr_type == "yahoo_metal":

        db.metal_prices.drop()
        db.metal_returns.drop()

    elif corr_type == "metal":

        db.dyn_met_correlation_3Y.drop()
        db.dyn_met_correlation_1Y.drop()
        db.dyn_met_correlation_1Q.drop()
        db.dyn_met_correlation_1M.drop()

    elif corr_type == "btc_den":

        db.yahoo_btc_denominated_5Y.drop()
        db.altcoin_btc_denominated_5Y.drop()
        db.yahoo_btc_denominated_3Y.drop()
        db.altcoin_btc_denominated_3Y.drop()
        db.yahoo_btc_denominated_2Y.drop()
        db.altcoin_btc_denominated_2Y.drop()
        db.yahoo_btc_denominated_1Y.drop()
        db.altcoin_btc_denominated_1Y.drop()
        db.yahoo_btc_denominated_6M.drop()
        db.altcoin_btc_denominated_6M.drop()
        db.yahoo_btc_denominated_3M.drop()
        db.altcoin_btc_denominated_3M.drop()
        db.yahoo_btc_denominated_1M.drop()
        db.altcoin_btc_denominated_1M.drop()
        db.yahoo_btc_denominated_1W.drop()
        db.altcoin_btc_denominated_1W.drop()
        db.yahoo_btc_denominated_YTD.drop()
        db.altcoin_btc_denominated_YTD.drop()

    elif corr_type == "norm":

        db.normalized_prices_5Y.drop()
        db.normalized_prices_3Y.drop()
        db.normalized_prices_2Y.drop()
        db.normalized_prices_1Y.drop()
        db.normalized_prices_6M.drop()
        db.normalized_prices_3M.drop()
        db.normalized_prices_1M.drop()
        db.normalized_prices_1W.drop()
        db.normalized_prices_YTD.drop()

    elif corr_type == "vola":

        db.volatility_252.drop()
        db.volatility_90.drop()
        db.volatility_30.drop()

    elif corr_type == "market_cap":

        db.market_cap.drop()
        db.btc_supply.drop()

    elif corr_type == "markovitz":

        db.CAPM.drop()
        db.CAPM_no_BTC.drop()

    elif corr_type == "S2F":

        db.S2F_model.drop()


def mongo_correlation_drop():

    mongo_coll_drop("static_alt")
    mongo_coll_drop("static_var")
    mongo_coll_drop("dynamic_alt")
    mongo_coll_drop("dynamic_var")
    mongo_coll_drop("dynamic_SP500")


def mongo_upload(data_to_upload, where_to_upload,
                 column_set_val=None):

    collection_dict = mongo_coll()

    data_to_dict = data_to_upload.to_dict(orient="records")
    collection_dict.get(where_to_upload).insert_many(data_to_dict)
