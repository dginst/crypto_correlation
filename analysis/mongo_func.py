from datetime import datetime, timezone
# third party packages
import pandas as pd

from pymongo import MongoClient

from config import (
    DB_NAME
)


# connecting to mongo in local
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
    connection = MongoClient("localhost", 27017)

    db = connection.btc_analysis

    return db


def mongo_indexing():

    db = mongo_index_conn()

    # return collections
    db.return_various.create_index([("id", -1)])
    db.return_crypto.create_index([("id", -1)])

    # dynamic altcoin correlation collections
    db.dyn_alt_correlation_3Y.create_index([("id", -1)])
    db.dyn_alt_correlation_1Y.create_index([("id", -1)])
    db.dyn_alt_correlation_1Q.create_index([("id", -1)])
    db.dyn_alt_correlation_1M.create_index([("id", -1)])

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


def mongo_coll():

    db = mongo_index_conn()

    dict_of_coll = {

        # return collections
        "collection_ret_var": db.return_various,
        "collection_ret_crypto": db.return_crypto,

        # dynamic altcoins correlation collections
        "collection_3Y_dyn_alt": db.dyn_alt_correlation_3Y,
        "collection_1Y_dyn_alt": db.dyn_alt_correlation_1Y,
        "collection_1Q_dyn_alt": db.dyn_alt_correlation_1Q,
        "collection_1M_dyn_alt": db.dyn_alt_correlation_1M,

        # dynamic various correlation collections
        "collection_3Y_dyn_var": db.dyn_var_correlation_3Y,
        "collection_1Y_dyn_var": db.dyn_var_correlation_1Y,
        "collection_1Q_dyn_var": db.dyn_var_correlation_1Q,
        "collection_1M_dyn_var": db.dyn_var_correlation_1M,

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

        # static crypto correlation collections
        "collection_all_stat_alt": db.stat_alt_correlation_all,
        "collection_3Y_stat_alt": db.stat_alt_correlation_3Y,
        "collection_1Y_stat_alt": db.stat_alt_correlation_1Y,
        "collection_1Q_stat_alt": db.stat_alt_correlation_1Q,
        "collection_1M_stat_alt": db.stat_alt_correlation_1M,

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

    elif corr_type == "dynamic_var":

        db.dyn_var_correlation_3Y.drop()
        db.dyn_var_correlation_1Y.drop()
        db.dyn_var_correlation_1Q.drop()
        db.dyn_var_correlation_1M.drop()

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


# def mongo_delete(coll_where_del, query_to_del):

#     collection_dict = mongo_coll()
#     collection_dict.get(coll_where_del).delete_many(query_to_del)

#     return None


# def mongo_daily_delete(day_to_del, op_set):
#     '''
#     @param day_to_del has to be in "YY-mm-dd" string format
#     @param op_set can be "ecb", "cw", "index"
#     '''

#     day_to_del_TS, _ = days_variable(day_to_del)

#     if op_set == "ecb":

#         mongo_delete("collection_ecb_raw", {"TIME_PERIOD": str(day_to_del_TS)})
#         mongo_delete("collection_ecb_clean", {"Date": str(day_to_del_TS)})

#     elif op_set == "cw":

#         mongo_delete("collection_cw_raw", {"Time": day_to_del_TS})
#         mongo_delete("collection_cw_clean", {"Time": day_to_del_TS})
#         mongo_delete("collection_cw_vol_check", {"Time": day_to_del_TS})
#         mongo_delete("collection_cw_converted", {"Time": day_to_del_TS})
#         mongo_delete("collection_cw_final_data", {"Time": day_to_del_TS})

#         mongo_delete("collection_stable_rate", {"Time": day_to_del_TS})

#     # elif op_set == "data_feed":

#     #     mongo_delete("collection_data_feed")

#     elif op_set == "index":

#         mongo_delete("collection_price", {"Time": day_to_del_TS})
#         mongo_delete("collection_volume", {"Time": day_to_del_TS})
#         mongo_delete("collection_price_ret", {"Time": day_to_del_TS})
#         mongo_delete("collection_EWMA", {"Time": day_to_del_TS})
#         mongo_delete("collection_divisor_reshaped", {"Time": day_to_del_TS})
#         mongo_delete("collection_EWMA_check", {"Time": day_to_del_TS})
#         mongo_delete("collection_synth", {"Time": day_to_del_TS})
#         mongo_delete("collection_relative_synth", {"Time": day_to_del_TS})
#         mongo_delete("collection_index_level_raw", {"Time": day_to_del_TS})
#         mongo_delete("collection_index_level_1000", {"Time": day_to_del_TS})
#         mongo_delete("collection_all_exc_vol", {"Time": day_to_del_TS})
#         mongo_delete("collection_cw_raw", {"Time": day_to_del_TS})

#     return None


# def df_reorder(df_to_reorder, column_set):

#     if column_set == "complete":

#         reordered_df = df_to_reorder[
#             [
#                 "Date",
#                 "Time",
#                 "BTC",
#                 "ETH",
#                 "XRP",
#                 "LTC",
#                 "BCH",
#                 "EOS",
#                 "ETC",
#                 "ZEC",
#                 "ADA",
#                 "XLM",
#                 "XMR",
#                 "BSV",
#             ]
#         ]

#     elif column_set == "divisor":

#         reordered_df = df_to_reorder[
#             [
#                 "Date",
#                 "Time",
#                 "Divisor Value"
#             ]
#         ]

#     elif column_set == "index":

#         reordered_df = df_to_reorder[
#             [
#                 "Date",
#                 "Time",
#                 "Index Value"
#             ]
#         ]

#     elif column_set == "conversion":

#         reordered_df = df_to_reorder[
#             [
#                 "Time",
#                 "Close Price",
#                 "Crypto Volume",
#                 "Pair Volume",
#                 "Exchange",
#                 "Pair"
#             ]
#         ]

#     return reordered_df
