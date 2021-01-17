from btc_analysis.mongo_func import (
    mongo_coll_drop
)
from btc_analysis.calc import (
    normalized_price_op
)

mongo_coll_drop("norm")

normalized_price_op()
