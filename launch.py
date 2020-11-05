from datetime import datetime
import time
from mongo_func import mongo_upload
import pandas as pd

df = pd.read_excel(r'C:\Projects\dginst\btc-analysis\file\return_3009.xlsx',
                   sheet_name='bloomberg')

df["Date"] = [x.strftime("%Y-%m-%d")
              for x in df["Date"]]

mongo_upload(df, "collection_ret_var")

df2 = pd.read_excel(r'C:\Projects\dginst\btc-analysis\file\return_3009.xlsx',
                    sheet_name='altcoin')

df2["Date"] = [x.strftime("%Y-%m-%d")
               for x in df2["Date"]]

mongo_upload(df2, "collection_ret_crypto")
