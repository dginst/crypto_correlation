import yfinance as yf

msft = yf.Ticker("GC=F")

# get stock info
print(msft.info)

# get historical market data
hist = msft.history(start="2020-10-01", end="2020-10-10")
print(hist)
