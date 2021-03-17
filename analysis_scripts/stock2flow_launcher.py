from btc_analysis.stock2flow_func import complete_model, S2F_definition
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from btc_analysis.mongo_func import mongo_coll_drop, mongo_upload

mongo_coll_drop("S2F")

initial_data = pd.read_csv(
    Path("source_data", "initial_data_S2F.csv"), sep="|")


slope, intercept = S2F_definition(initial_data)


final_df = complete_model(slope, intercept)

mongo_upload(final_df, "collection_S2F")

print(final_df)

# _x = final_df["Date"]
# _y = final_df["S2F price"]

# plt.figure(figsize=(12, 8))
# plt.title('stock to Flow')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.plot(_x, _y, 'steelblue', linewidth=3)

# plt.show()
