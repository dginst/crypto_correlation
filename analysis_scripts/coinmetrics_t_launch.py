# from coinmetrics.base import Base as coin

# coin.__init__(api_key='')

# query = {
#     "metricData": {
#         "metrics": [
#             "TxCnt",
#             "PriceUSD",
#             "BlkCnt"
#         ],
#     }
# }

# x = coin.metrics("BlkCnt")
# print(x)

from btc_analysis.calc import last_quarter_end

print(last_quarter_end())
