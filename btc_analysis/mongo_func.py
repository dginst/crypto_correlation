from datetime import datetime, timezone
# third party packages
import pandas as pd

from pymongo import MongoClient

from btc_analysis.config import (
    DB_NAME
)

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
    print(coll)
    print(connection)
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
    db.dyn_alt_correlation_3Y.create_index([("id", -1)])
    db.dyn_alt_correlation_1Y.create_index([("id", -1)])
    db.dyn_alt_correlation_1Q.create_index([("id", -1)])
    db.dyn_alt_correlation_1M.create_index([("id", -1)])

    # dynamic metal correlation collections
    db.dyn_met_correlation_3Y.create_index([("id", -1)])
    db.dyn_met_correlation_1Y.create_index([("id", -1)])
    db.dyn_met_correlation_1Q.create_index([("id", -1)])
    db.dyn_met_correlation_1M.create_index([("id", -1)])

    # dynamic various correlation collections
    db.dyn_var_correlation_3Y.create_index([("id", -1)])
    db.dyn_var_correlation_1Y.create_index([("id", -1)])
    db.dyn_var_correlation_1Q.create_index([("id", -1)])
    db.dyn_var_correlation_1M.create_index([("id", -1)])

    # dynamic SP500 correlation collections
    db.dyn_SP500_correlation_3Y.create_index([("id", -1)])
    db.dyn_SP500_correlation_1Y.create_index([("id", -1)])
    db.dyn_SP500_correlation_1Q.create_index([("id", -1)])
    db.dyn_SP500_correlation_1M.create_index([("id", -1)])

    # static altcoin correlation collections
    db.stat_alt_correlation_all.create_index([("id", -1)])
    db.stat_alt_correlation_3Y.create_index([("id", -1)])
    db.stat_alt_correlation_1Y.create_index([("id", -1)])
    db.stat_alt_correlation_1Q.create_index([("id", -1)])
    db.stat_alt_correlation_1M.create_index([("id", -1)])

    # static various correlation collections
    db.stat_var_correlation_all.create_index([("id", -1)])
    db.stat_var_correlation_3Y.create_index([("id", -1)])
    db.stat_var_correlation_1Y.create_index([("id", -1)])
    db.stat_var_correlation_1Q.create_index([("id", -1)])
    db.stat_var_correlation_1M.create_index([("id", -1)])

    # series in BTC price
    db.yahoo_btc_denominated_3Y.create_index([("id", -1)])
    db.altcoin_btc_denominated_3Y.create_index([("id", -1)])
    db.yahoo_btc_denominated_1Y.create_index([("id", -1)])
    db.altcoin_btc_denominated_1Y.create_index([("id", -1)])
    db.yahoo_btc_denominated_6M.create_index([("id", -1)])
    db.altcoin_btc_denominated_6M.create_index([("id", -1)])
    db.yahoo_btc_denominated_3M.create_index([("id", -1)])
    db.altcoin_btc_denominated_3M.create_index([("id", -1)])
    db.yahoo_btc_denominated_1M.create_index([("id", -1)])
    db.altcoin_btc_denominated_1M.create_index([("id", -1)])


def mongo_coll():

    db = mongo_index_conn()

    dict_of_coll = {

        # yahoo collections
        "collection_prices_y": db.all_prices_y,
        "collection_returns_y": db.all_returns_y,
        "collection_logreturns_y": db.all_logreturns_y,

        # bloomberg
        "collection_prices": db.all_prices,
        "collection_returns": db.all_returns,
        "collection_logreturns": db.all_logreturns,

        # metal only collections (yahoo)
        "collection_metal_price": db.metal_prices,
        "collection_metal_ret": db.metal_returns,

        # return collections
        "collection_ret_var": db.return_various,
        "collection_ret_crypto": db.return_crypto,

        # dynamic altcoins correlation collections
        "collection_3Y_dyn_alt": db.dyn_alt_correlation_3Y,
        "collection_1Y_dyn_alt": db.dyn_alt_correlation_1Y,
        "collection_1Q_dyn_alt": db.dyn_alt_correlation_1Q,
        "collection_1M_dyn_alt": db.dyn_alt_correlation_1M,

        # dynamic metal correlation collections
        "collection_3Y_dyn_met": db.dyn_met_correlation_3Y,
        "collection_1Y_dyn_met": db.dyn_met_correlation_1Y,
        "collection_1Q_dyn_met": db.dyn_met_correlation_1Q,
        "collection_1M_dyn_met": db.dyn_met_correlation_1M,

        # dynamic various correlation collections
        "collection_3Y_dyn_var": db.dyn_var_correlation_3Y,
        "collection_1Y_dyn_var": db.dyn_var_correlation_1Y,
        "collection_1Q_dyn_var": db.dyn_var_correlation_1Q,
        "collection_1M_dyn_var": db.dyn_var_correlation_1M,

        # dynamic yahoo correlation collections
        "collection_3Y_dyn_yahoo": db.dyn_yahoo_correlation_3Y,
        "collection_1Y_dyn_yahoo": db.dyn_yahoo_correlation_1Y,
        "collection_1Q_dyn_yahoo": db.dyn_yahoo_correlation_1Q,
        "collection_1M_dyn_yahoo": db.dyn_yahoo_correlation_1M,

        # dynamic SP500 correlation collections
        "collection_3Y_dyn_SP500": db.dyn_SP500_correlation_3Y,
        "collection_1Y_dyn_SP500": db.dyn_SP500_correlation_1Y,
        "collection_1Q_dyn_SP500": db.dyn_SP500_correlation_1Q,
        "collection_1M_dyn_SP500": db.dyn_SP500_correlation_1M,

        # static various correlation collections
        "collection_all_stat_var": db.stat_var_correlation_all,
        "collection_3Y_stat_var": db.stat_var_correlation_3Y,
        "collection_1Y_stat_var": db.stat_var_correlation_1Y,
        "collection_1Q_stat_var": db.stat_var_correlation_1Q,
        "collection_1M_stat_var": db.stat_var_correlation_1M,

        # static yahoo correlation collections
        "collection_all_stat_yahoo": db.stat_yahoo_correlation_all,
        "collection_3Y_stat_yahoo": db.stat_yahoo_correlation_3Y,
        "collection_1Y_stat_yahoo": db.stat_yahoo_correlation_1Y,
        "collection_1Q_stat_yahoo": db.stat_yahoo_correlation_1Q,
        "collection_1M_stat_yahoo": db.stat_yahoo_correlation_1M,

        # static crypto correlation collections
        "collection_all_stat_alt": db.stat_alt_correlation_all,
        "collection_3Y_stat_alt": db.stat_alt_correlation_3Y,
        "collection_1Y_stat_alt": db.stat_alt_correlation_1Y,
        "collection_1Q_stat_alt": db.stat_alt_correlation_1Q,
        "collection_1M_stat_alt": db.stat_alt_correlation_1M,

        # priced denominated in BTC collections
        "collection_yahoo_btc_den_3Y": db.yahoo_btc_denominated_3Y,
        "collection_alt_btc_den_3Y": db.altcoin_btc_denominated_3Y,
        "collection_yahoo_btc_den_1Y": db.yahoo_btc_denominated_1Y,
        "collection_alt_btc_den_1Y": db.altcoin_btc_denominated_1Y,
        "collection_yahoo_btc_den_6M": db.yahoo_btc_denominated_6M,
        "collection_alt_btc_den_6M": db.altcoin_btc_denominated_6M,
        "collection_yahoo_btc_den_3M": db.yahoo_btc_denominated_3M,
        "collection_alt_btc_den_3M": db.altcoin_btc_denominated_3M,
        "collection_yahoo_btc_den_1M": db.yahoo_btc_denominated_1M,
        "collection_alt_btc_den_1M": db.altcoin_btc_denominated_1M,

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

        db.yahoo_btc_denominated_3Y.drop()
        db.altcoin_btc_denominated_3Y.drop()
        db.yahoo_btc_denominated_1Y.drop()
        db.altcoin_btc_denominated_1Y.drop()
        db.yahoo_btc_denominated_6M.drop()
        db.altcoin_btc_denominated_6M.drop()
        db.yahoo_btc_denominated_3M.drop()
        db.altcoin_btc_denominated_3M.drop()
        db.yahoo_btc_denominated_1M.drop()
        db.altcoin_btc_denominated_1M.drop()


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
