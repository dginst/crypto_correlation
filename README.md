# crypto_correlation

The repository allows to compute various statistics related to Bitcoin such as correlations with altcoins, correlations with asset classes, market capitalization, price comparison and creation of Excel files containing graphs and values related to both dynamic and static correlations.

The data storage is managed through MongoDB uploading different collections in the "btc_analysis" database. All cryptocurrencies values, especially prices and volumes, derive from another MongoDB database named "index".

Install the repository and its prerequisites into a
python virtual environment; e.g. from the root folder:

Bash shell

    python -m venv venv
    source venv/bin/activate
    pip install --upgrade -r requirements.txt
    pip install --upgrade -e ./

Windows CMD or PowerShell:

    python -m venv venv
    .\venv\Scripts\activate
    pip install --upgrade -r requirements.txt
    pip install --upgrade -e ./

Windows Git bash shell:

    python -m venv venv
    cd ./venv/Scripts
    . activate
    cd ../..
    pip install --upgrade -r requirements.txt
    pip install --upgrade -e ./


The repository has the following structure:

CRYPTO_CORRELATION
|
|--- btc_analysis --> folder containing all the functions needed in the repository
|
|--- analysis scripts --> contains the scripts that upload the data into MongoDB collections
|
|--- dashboard --> folder containing the scripts that launch the dashbopard app
|
|--- excel creator
    |--- input
    |--- output

# ---- analysis scripts ----

In order to properly run all the scripts without errors 
the order is relevant. More specifically:

# 1) yahoo_series_daily_launcher.py

    The script downloads the updated financial data from Yahoo Finance using the API and retrieves daily
    crypto's prices and volumes from the "index" database; then computes returns and logreturns.

    RELEVANT: In order to work locally the MongoDB database "index" has to exist along with the collections "crypto_price", "crypto_volume" and "index_data_feed". 

    Once launched, the script updates the MongoDB collection:
    - "all_prices_y"
    - "all_returns_y"
    - "all_logreturns_y"
    - "all_volume_y"

    Moreover the script updates the collections:
    - "market_cap" 
    - "btc_supply"

    Specifically, the supply update leverages on the API of blockchain.info website.


# 2) series_volatility_launcher.py

    The script computes the historical volatility for the stocks, bonds, commodity, currencies and cryptos contained in the "all_logreturns_y" collection.
    The historical volatility is computed with a rolling window of 252, 90 and 30 days.
    Once finished the collections:

    - volatility_252
    - volatility_90
    - volatility_30

    will be updated.

# 3) usd_denominated_launcher.py

    The script computes the price series of the stocks, bonds, commodity, currencies and cryptos contained in the "all_returns_y" collection each denominated in USD and starting at the normalized value 1.

    Different time windows are computed computed, specifically 5, 3, 2, 1 year and 6, 3, 1 month, and the following collections updated:

    - normalized_prices_5Y
    - normalized_prices_3Y
    - normalized_prices_2Y
    - normalized_prices_1Y
    - normalized_prices_6M
    - normalized_prices_3M
    - normalized_prices_1M


# 4) btc_denominated_launcher.py

    The script computes the price series of the stocks, bonds, commodity, currencies and cryptos contained in the "all_returns_y" collection each denominated in BTC and all the altcoin prices still BTC denoiminated. Each series starts at the normalized value 1.

    Different time windows are computed computed, specifically 5, 3, 2, 1 year and 6, 3, 1 month, and the following collections updated:

    - yahoo_btc_denominated_5Y
    - yahoo_btc_denominated_3Y
    - yahoo_btc_denominated_2Y
    - yahoo_btc_denominated_1Y
    - yahoo_btc_denominated_6M
    - yahoo_btc_denominated_3M
    - yahoo_btc_denominated_1M

    - altcoin_btc_denominated_5Y
    - altcoin_btc_denominated_3Y
    - altcoin_btc_denominated_2Y
    - altcoin_btc_denominated_1Y
    - altcoin_btc_denominated_6M
    - altcoin_btc_denominated_3M
    - altcoin_btc_denominated_1M


# 5) btc_correlation_launcher.py

    The script computes both dynamic and static correlations between Bitcoin and differents assets. The correlations results are divided into two main streams: one related to the stocks, bonds, commodity, currencies downloaded from Yahoo Finance and the other related to all the altcoins retrieved from the "index" database.

    RELEVANT: In order to work locally the MongoDB database "index" has to exist along with the collections "crypto_price" and "crypto_price_return".

    Dynamic Correlations

        The script computes dynamic correlations for different rolling time windows, specifically: 3 year, 1 year, 1 quarter and 1 month.
        Once launched it will update the following collections on MongoDB:

        - dyn_yahoo_correlation_3Y
        - dyn_yahoo_correlation_1Y
        - dyn_yahoo_correlation_1Q
        - dyn_yahoo_correlation_1M

        - dyn_alt_correlation_3Y
        - dyn_alt_correlation_1Y
        - dyn_alt_correlation_1Q
        - dyn_alt_correlation_1M
    

    Static Correlations

        The script computes static correlations, namely considering only the data releated to a specific time window and not a rolling time window, for all the available time series, 3 year, 1 year, 1 quarter and 1 month.
        Once launched it will update the following collections on MongoDB:

        - stat_yahoo_correlation_all
        - stat_yahoo_correlation_3Y
        - stat_yahoo_correlation_1Y
        - stat_yahoo_correlation_1Q
        - stat_yahoo_correlation_1M

        - stat_alt_correlation_all
        - stat_alt_correlation_3Y
        - stat_alt_correlation_1Y
        - stat_alt_correlation_1Q
        - stat_alt_correlation_1M

# 6) markovitz_launcher.py

    Startimg from a given set of assets, chosen in the list YAHOO_TO_CAPM in config.py file, the script computes:
    - the efficient frontier with and without bitcoin in the portfolio
    - the and the optimal weights, using the Capital Asset Pricing Model, of each assets at different   level of risk

# 7) stock2flow_launcher.py

    This script aims to reproduce the Stock to Flow model and applying it to the Bitcoin Market Capitalization in order to reverse enginering the BTC price for the future.
    Two CSV files, contained in the folder "source_data" are used for the initial information:
    - BTC_price.csv that contains the entire price history of BTC and is updated evry day
    - initial_data_S2F.csv that contains BTC price and Supply for each 1st of the months starting from 2009 until now. Each row is an observation point used to define the S2F model.

    There are two different typologies of S2F implemented:

    7.1) Standard Stock to Flow

        Firstly is computed the Stock to Flow ratio at each observation point leveraging on the known Market Capitalization and the inferable Flow, then a linear regression is applied in order to find the value of slope and intercept of the function:
        ln(Market Cap) = slope * ln(S2F ratio) + intercept

        Knowing slope and intercept is thus possible to built the model price series using the inferable future S2F ratios and computing the Market Cap using the previously found slope and intecept.


    7.2) Stock to Flow Cross Asset Model

        This model uses a different approach from the above one. The main difference is that now the observation points are not used to compute slope and intecept through a linear regression but they are used to find k clusters of aggregation for the observation points themselves.
        The chosen methodology to find the cluster in the "k-mean clustering".

        Once the cluster has been defined and the points (S2F ratio, Market Cap) for Gold and Silver computed, they are all used for a linear regression in order to find slope and intecept using the above mentioned: ln(Market Cap) = slope * ln(S2F ratio) + intercept

        Knowing slope and intercept is thus possible to built the model price series using the inferable future S2F ratios and computing the Market Cap using the previously found slope and intecept.
        

# 8) btc_supply_launcher.py





# ---- excel creator ----

# excel_corr_creator.py

    The script creates two excel files contaioning data and graphs regardind the correlations, both dynamic and static, of altcoins and various assets with Bitcoin.

    Each file is created inside the sub-folder "output" of the main folder "excel creator".


# ---- dashboard ----

# 0) link_dashboard.py

# 1) btc_stats_dashboard.py

# 2) crypto_asset_dashboard.py

    The script creates a dashboard app running on port 4000 (and online on http://18.221.143.32:4000/) that displays:

    - Altcoins performances denominated in BTC
    - Stocks, bonds, commodity, currencies from Yahoo Finance performances denominated in BTC
    - Apple, Netflix, Amazon, Tesla and Bitcoin peformances denominated in USD
    - Historical Volatility of Apple, Netflix, Amazon, Tesla and Bitcoin
    - Volumes of Apple, Netflix, Amazon, Tesla and Bitcoin and Bitcoin without stablecoins transactions' volumes

    The Dashboard updates autonomously on daily basis and each graph gives the possibility to select differents time windows.


# 3) asset_class_dashboard.py

    The script creates a dashboard app running on http://18.221.143.32:4500/ that displays:

    - Altcoins correlation with Bitcoin
    - Stocks, bonds, commodity, currencies from Yahoo Finance correlations with Bitcoin

    The Dashboard updates autonomously on daily basis and each graph gives the possibility to select differents time windows.

# 4) best_perf_dashboard.py

    WIP

# 4) markovitz_dashboard.py

# 5) stock2flow_dashboard.py

# 6) stock2flow_cross_dashboard.py

# 7) market_cap_dashboard.py

# 8) btc_static_corr_dashboard.py


