# crypto_correlation

The repository allows to compute various statistics related to Bitcoin such as correlations with altcoins, correlations with asset classes, market capitalization, price comparison and creation of Excel file containing graph and values relòated to both dynamic and static correlations.

The data storage is managed through MongoDB uploading different collections in the "btc_analysis" database. All cryptocurrencies values, especially prices and volumes, derive from another MongoDB database named "index".

In order to properly use the repository two main actions are needed:
1) install the requirements.txt file "pip install -U -r requirements.txt"
2) install the setup.py file that allows to use the functions contained in "btc_analysis" folder 

The repository has the following structure:

CRYPTO_CORRELATION
|
|--- btc_analysis --> folder containing all the functions needed in the repository
|
|--- analysis scripts -->contains the scripts that upload the data into MongoDB collections
|
|--- dashboard --> folder containing the scripts that launch the dashbopard app
|
|--- excel creator

# ---- analysis scripts ----

In order to effectively run the scripts the order of running is relevant. More specifically:

# 1) yahoo_series_update_launcher.py

    The script downloads the updated financial data from Yahoo Finance using the API and retrieves crypto's prices and volumes from the "index" database; then compiutes returns and logreturns.

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


# ---- excel creator ----




# ---- dashboard ----

# 1) btc_analysis_dashboard.py

    The script creates a dashboard app running on http://18.221.143.32:4000/ that displays:

    - Altcoins performances denominated in BTC
    - Stocks, bonds, commodity, currencies from Yahoo Finance performances denominated in BTC
    - Apple, Netflix, Amazon, Tesla and Bitcoin peformances denominated in USD
    - Historical Volatility of Apple, Netflix, Amazon, Tesla and Bitcoin
    - Volumes of Apple, Netflix, Amazon, Tesla and Bitcoin and Bitcoin without stablecoins transactions' volumes

    The Dashboard updates autonomously on daily basis and each graph gives the possibility to select differents time windows.


# 2) btc_correlation_dashboard.py

    The script creates a dashboard app running on http://18.221.143.32:4500/ that displays:

    - Altcoins correlation with Bitcoin
    - Stocks, bonds, commodity, currencies from Yahoo Finance correlations with Bitcoin

    The Dashboard updates autonomously on daily basis and each graph gives the possibility to select differents time windows.

# 3) btc_static_corr_dashboard.py

    WIP