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

# analysis scripts

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

# 4) btc_denominated_launcher.py

# 5) btc_correlation_launcher.py

# 6) 
