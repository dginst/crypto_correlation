import seaborn as sns
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
from efficient_frontier import (sharpe_simulation, efficient_frontier,
                                ret_vol_sharpe_from_w, optmization_single,
                                min_max_ret, eff_front_op

                                )
# from analysis.mongo_func import (
#     query_mongo
# )
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import seaborn as sns
from scipy.stats import (norm, t, jarque_bera)


# connecting to mongo in local
connection = MongoClient("localhost", 27017)
# creating the database called index
db = connection.btc_analysis


def date_gen(start_date, end_date, holiday="Y"):

    if holiday == "N":

        date_index = pd.bdate_range(start_date, end_date)
        date_list = [datetime.strftime(
            date, "%Y-%m-%d") for date in date_index]

    else:

        date_index = pd.date_range(start_date, end_date)
        date_list = [datetime.strftime(date, "%Y-%m-%d")
                     for date in date_index]

    return date_list


def single_series_download(series_code, start_period, end_period):

    # creatre object
    series_obj = yf.Ticker(series_code)

    # create the complete array of date
    date_arr = np.array(date_gen(start_period, end_period, holiday="N"))
    date_df = pd.DataFrame(columns=["Date"])
    date_df["Date"] = date_arr

    # get historical market data
    df = series_obj.history(start=start_period, end=end_period)
    df.reset_index(inplace=True)

    # modifying date format
    df["Date"] = [x.strftime("%Y-%m-%d") for x in df["Date"]]
    # df["Date"] = [datetime.strptime(
    #    x, "%Y-%m-%d") for x in df["Date"]]

    df = df[["Date", "Close"]]
    # print(df)
    merged = pd.merge(date_df, df, how="left", on="Date")

    return merged


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


first = single_series_download("AMZN", "2019-01-01", "2020-09-30")
first["amazon"] = first["Close"]
second = single_series_download("TSLA", "2019-01-01", "2020-09-30")
second["tesla"] = second["Close"]
third = single_series_download("BTC-USD", "2019-01-01", "2020-09-30")
third["BTC"] = third["Close"]
fourth = single_series_download("^IXIC", "2019-01-01", "2020-09-30")
fourth["Nasdaq"] = fourth["Close"]

prices = pd.concat([first["amazon"], second["tesla"],
                    third["BTC"], fourth["Nasdaq"]], axis=1)
print(prices)
log_ret_df = np.log(prices / prices.shift(1))
print(log_ret_df)


# ret_arr, vol_arr, sharpe_arr, all_weights = sharpe_simulation(log_ret_df, prices)
# x = ret_vol_sharpe_from_w([0.2, 0.2, 0.6], log_ret_df)
# print(x)
# print(sharpe)
##
# d = optmization_single(prices, log_ret_df)
# print(d)
##

all_price_df = query_mongo("btc_analysis", "all_prices")
prices = all_price_df.drop(columns=["Date"])
log_ret_df = query_mongo("btc_analysis", "all_logreturns")

# gold = single_series_download("GC=F", "2010-07-01", "2018-09-01")
# price = pd.DataFrame(columns=["Gold"])
# price["Gold"] = gold["Close"]
# log_ret_df = np.log(price / price.shift(1))

# print(log_ret_df)

# eff_front_op(prices, log_ret_df)

# Computing historic annualized volatility
# The rolling function uses a window of 252 trading days.
# Each of the days in the selected lookback period is assigned
# The user can choose a longer or a shorter period as per his need.


def annualized_std(log_ret_df, year_days=252):

    y_sigma = log_ret_df.std() * (year_days ** 0.5)

    return y_sigma


# Note that this test only works for a large enough number of data samples
# ( > 2000) as the test statistic asymptotically has a Chi-squared distribution
#  with 2 degrees of freedom
def JB_test(log_ret_df):

    n = len(log_ret_df.iloc[:, 1])
    exc_kurt = log_ret_df.kurtosis()
    exc_skew = log_ret_df.skew()

    jb = n * ((exc_skew ** 2) / 6 + (exc_kurt ** 2) / 24)

    return jb


def JB_result(log_ret_df, p_val=0.05):

    _, JBpv = jarque_bera(log_ret_df)

    if JBpv > 0.05:

        return False

    else:

        return True


def hist_std_dev(log_ret_df, window=252):

    std_dev = log_ret_df.rolling(window=window).std() * np.sqrt(window)

    return std_dev


# histogram of daily returns vs the normal curve
def normal_check_chart(log_ret_df):

    mu = log_ret_df["BTC"].mean()
    sigma = log_ret_df["BTC"].std()

    plt.hist(
        log_ret_df["BTC"], 40, facecolor='blue', alpha=0.5)
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
    y = norm.pdf(x, mu, sigma)
    plt.plot(x, y, 'r')
    plt.show()


def VaR_n(ret_df, confidence=0.99, holding_period=1, year_days=252):

    holding_f = holding_period/year_days

    # find the average of daily returns
    mu = ret_df.mean()
    # find the volatility related to the holding period, starting
    # from the annualized volatility of the daily returns
    sigma = annualized_std(ret_df, year_days=year_days)
    sigma_h = sigma * np.sqrt(holding_f)

    VaR_ = norm.ppf(confidence) * sigma_h - mu

    VaR_ = norm.ppf(confidence, sigma_h, mu)

    return VaR_


def CVaR_n(ret_df, confidence=0.99, holding_period=1, year_days=252):

    alpha = 1 - confidence

    holding_f = holding_period/year_days

    # find the average of daily returns
    mu = ret_df.mean()
    # find the volatility related to the holding period, starting
    # from the annualized volatility of the daily returns
    sigma = annualized_std(ret_df, year_days=year_days)
    sigma_h = sigma * np.sqrt(holding_f)

    CVaR_ = (alpha ** -1) * (norm.pdf(norm.ppf(alpha)) * sigma_h) - mu

    return CVaR_


# degree of freedom, the larger, the closer to normal distribution

def VaR_t(ret_df, confidence=0.99, degree_of_freedom=10,
          holding_period=1, year_days=252):

    alpha = 1 - confidence

    holding_f = holding_period/year_days

    # find the average of daily returns
    mu = ret_df.mean()
    # find the volatility related to the holding period, starting
    # from the annualized volatility of the daily returns
    sigma = annualized_std(ret_df, year_days=year_days)
    sigma_h = sigma * np.sqrt(holding_f)

    t_val = t.ppf(alpha, degree_of_freedom)
    freed_val = (degree_of_freedom - 2) / degree_of_freedom

    VaR_ = np.sqrt(holding_f * freed_val) * t_val * sigma_h - mu

    return VaR_


def CVaR_t(ret_df, confidence=0.99, degree_of_freedom=10,
           holding_period=1, year_days=252):

    alpha = 1 - confidence

    holding_f = holding_period/year_days

    # find the average of daily returns
    mu = ret_df.mean()
    # find the volatility related to the holding period, starting
    # from the annualized volatility of the daily returns
    sigma = annualized_std(ret_df, year_days=year_days)
    sigma_h = sigma * np.sqrt(holding_f)

    t_val = t.ppf(alpha, degree_of_freedom)
    first_comp = -1 / alpha * (1 - degree_of_freedom)**(-1)
    second_comp = (degree_of_freedom - 2 + t_val ** 2)

    VaR_ = first_comp * second_comp * t.pdf(t_val, nu) * sigma_h - mu

    return VaR_


# standard deviation
# normal_check_chart(log_ret_df)
print(annualized_std(log_ret_df))
# print(JB_result(log_ret_df))
# print(JB_test(log_ret_df))
print(log_ret_df.std())
print(t.ppf(0.01, 2))
# # variance
# print(log_ret_df.var())
# # minimum
# print(log_ret_df.min())
# # maximum
# print(log_ret_df.max())
# # mean
# print(log_ret_df.mean())
# # kurtosis
# print(log_ret_df.kurtosis())
# # skewness
# print(log_ret_df.skew())
# # VaR
# print(VaR(log_ret_df))
# print(VaR(log_ret_df, holding_period=30))
# # CVar
# print(CVaR(log_ret_df))
# print(CVaR(log_ret_df, holding_period=30))

returns = log_ret_df["BTC"]
returns = returns.dropna().values
print(returns)

mu_norm, sig_norm = norm.fit(returns)
dx = 0.0001  # resolution of the distribution
x = np.arange(-1, 1, dx)
pdf_n = norm.pdf(x, mu_norm, sig_norm)

nu, mu_t, sig_t = t.fit(returns)
nu = np.round(nu)
print("Student T mean is {0:.8f}, sigma is {1:.8f}, nu is {2}".format(
    mu_t, sig_t, nu))
pdf_t = t.pdf(x, nu, mu_t, sig_t)

h = 1
alpha = 0.01
xanu = t.ppf(alpha, nu)

CVaR_n = alpha**-1 * norm.pdf(norm.ppf(alpha))*sig_norm - mu_norm
VaR_n = norm.ppf(1-alpha)*sig_norm - mu_norm

VaR_t = np.sqrt((nu-2)/nu) * t.ppf(1-alpha, nu)*sig_norm - h*mu_norm
CVaR_t = -1/alpha * (1-nu)**(-1) * (nu-2+xanu**2) * \
    t.pdf(xanu, nu)*sig_norm - h*mu_norm

plt.figure(num=1, figsize=(11, 6))
# main figure
plt.hist(returns, bins=100, density=True, color='pink', edgecolor='white')

plt.axis("tight")
plt.plot(x, pdf_n, 'steelblue', label="Normal PDF fit")

plt.axis("tight")
plt.plot(x, pdf_t, 'red', label="Student t PDF fit")
plt.xlim([min(returns)/2, max(returns)])
plt.ylim([0, 100])
plt.legend(loc="best")
plt.xlabel("Daily Returns of BTC")
plt.ylabel("Return Distribution")
plt.show()

# inset
#a = plt.axes([.22, .35, .3, .4])
plt.hist(returns, bins=100, density=True, color='pink', edgecolor='white')

plt.plot(x, pdf_n, 'steelblue')

plt.plot(x, pdf_t, 'red')

# Student VaR line
plt.plot([-CVaR_t, -CVaR_t], [0, 1.2], c='red')
# Normal VaR line
plt.plot([-CVaR_n, -CVaR_n], [0, 1.6], c='steelblue')
plt.text(-CVaR_n-0.015, 1.6, "Norm CVaR", color='steelblue')
plt.text(-CVaR_t-0.0171, 1.2, "Student t CVaR", color='red')
plt.xlim([-0.2, -0.01])
plt.ylim([0, 10])
plt.show()
