import seaborn as sns
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import (norm, t, jarque_bera)
from btc_analysis.config import (
    STATISTICS
)
from btc_analysis.calc import (
    window_period_back
)


def annualized_std(log_ret_df, year_days=252):

    y_sigma = log_ret_df.std() * (year_days ** 0.5)

    return y_sigma


def annualized_mean(log_ret_df, year_days=252):

    y_mu = log_ret_df.mean() * (year_days ** 0.5)

    return y_mu


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

    VaR_ = first_comp * second_comp * \
        t.pdf(t_val, degree_of_freedom) * sigma_h - mu

    return VaR_


# calculates the Maximum Rolling Drawdown for a window of 250 days
# which is essentially the largest percentage loss a hypothetical
# investor could have incurred on the investment over a period of 250 days
# It also calculates the recovery period and finally highlights the maximum
# drawdown period and recovery period, along with the plots for maximum
# rolling drawdown and index closing levels

def worst_drawdown(single_price_series):

    # removing the NaN values
    single_price_series = single_price_series.dropna()

    # separate date series from prices series
    date = pd.DataFrame(columns=["Date"])
    date["Date"] = single_price_series["Date"]
    date["Date"] = [datetime.strptime(x, "%Y-%m-%d") for x in date["Date"]]
    single_price_series = single_price_series.drop(columns="Date")

    # find the negative peak and the start period of the worst drawdown
    num = (np.maximum.accumulate(single_price_series) - single_price_series)
    den = np.maximum.accumulate(single_price_series)
    max_drawdown_peak_i = (num / den).values.argmax()
    max_drawdown_peak_val = single_price_series.iloc[[max_drawdown_peak_i]]

    # worst drowdawn start period
    max_drawdown_start_j = single_price_series[:max_drawdown_peak_i].values.argmax(
    )
    max_drawdown_start_val = single_price_series.iloc[[max_drawdown_start_j]]

    # worst drawndown percentage
    max_DD_perc = float(max_drawdown_peak_val.to_numpy()) / \
        float(max_drawdown_start_val.to_numpy()) - 1

    max_drawdown_peak_date = date.iloc[[max_drawdown_peak_i]]
    max_drawdown_start_date = date.iloc[[max_drawdown_start_j]]

    # find Timstamp values of peak and start of drawdown period
    peak_date_TS = int(datetime.timestamp(
        list(max_drawdown_peak_date["Date"])[0]))
    start_date_TS = int(datetime.timestamp(
        list(max_drawdown_start_date["Date"])[0]))

    # find the lenght of the max drawdown in days
    DD_period_days = int(round((peak_date_TS - start_date_TS) / 86400))

    # try to find the recovery time in days, if the series had actually
    # recovered from the max drawdown
    post_peak_series = single_price_series[max_drawdown_peak_i:]

    recovery_arr = post_peak_series.where(
        post_peak_series > max_drawdown_start_val.to_numpy())

    # worst drowdawn recovery period position
    recovery_date_pos = recovery_arr.first_valid_index()

    if recovery_date_pos is not None:

        recovery_date = date.iloc[[recovery_date_pos]]
        recovery_TS = int(datetime.timestamp(list(recovery_date["Date"])[0]))
        recovery_period_days = round((recovery_TS - peak_date_TS) / 86400)

    else:

        recovery_period_days = 0

    stat_list = np.array(
        [max_DD_perc, int(DD_period_days), int(recovery_period_days)])
    header = single_price_series.columns
    df_stat = pd.DataFrame(stat_list, columns=header)

    return df_stat


# Sharpe Ratio
def sharpe_r(returns, risk_free=None, days=252):

    if risk_free is None:

        risk_free = 0

    annualized_std = returns.std() * np.sqrt(days)
    annualized_ret = returns.mean() * np.sqrt(days)
    sharpe_ratio = (annualized_ret - risk_free) / annualized_std

    return sharpe_ratio


def statistics_calc(prices_df, element):

    prices_df = prices_df[["Date", element]]
    only_prices = prices_df.drop(columns="Date")
    log_ret_df = np.log(only_prices / only_prices.shift(1))

    # creating a DF containing all the statistics
    stat = pd.DataFrame(columns=[element])
    # daily return mean
    d_mean = np.array(log_ret_df.mean())
    df = pd.DataFrame(d_mean, columns=[element])
    stat = stat.append(df)
    # annualized mean return
    y_mean = np.array(annualized_mean(log_ret_df))
    df = pd.DataFrame(y_mean, columns=[element])
    stat = stat.append(df)
    # minimum return
    min_ret = np.array(log_ret_df.min())
    df = pd.DataFrame(min_ret, columns=[element])
    stat = stat.append(df)
    # maximum return
    max_ret = np.array(log_ret_df.max())
    df = pd.DataFrame(max_ret, columns=[element])
    stat = stat.append(df)
    # daily standatrd deviation
    d_std = np.array(log_ret_df.std())
    df = pd.DataFrame(d_std, columns=[element])
    stat = stat.append(df)
    # annualized standard deviation
    y_std = np.array(annualized_std(log_ret_df))
    df = pd.DataFrame(y_std, columns=[element])
    stat = stat.append(df)
    # daily variance
    d_variance = np.array(log_ret_df.var())
    df = pd.DataFrame(d_variance, columns=[element])
    stat = stat.append(df)
    # Excess kurtosis
    exc_kurt = np.array(log_ret_df.kurtosis())
    df = pd.DataFrame(exc_kurt, columns=[element])
    stat = stat.append(df)
    # skewness
    skew = np.array(log_ret_df.skew())
    df = pd.DataFrame(skew, columns=[element])
    stat = stat.append(df)
    # normal distribution VaR_0,99 h_p 1 day
    VaR_n_ = np.array(VaR_n(log_ret_df))
    df = pd.DataFrame(VaR_n_, columns=[element])
    stat = stat.append(df)
    # normal distribution CVaR_0,99 h_p 1 day
    CVaR_n_ = np.array(CVaR_n(log_ret_df))
    df = pd.DataFrame(CVaR_n_, columns=[element])
    stat = stat.append(df)
    # t-student distribution VaR_0,99 h_p 1 day
    VaR_t_ = np.array(VaR_t(log_ret_df))
    df = pd.DataFrame(VaR_t_, columns=[element])
    stat = stat.append(df)
    # t-student distribution CVaR_0,99 h_p 1 day
    CVaR_t_ = np.array(CVaR_t(log_ret_df))
    df = pd.DataFrame(CVaR_t_, columns=[element])
    stat = stat.append(df)
    # Worst draw-down %
    drawdown_df = worst_drawdown(prices_df)
    stat = stat.append(drawdown_df)
    # Sharpe Ratio
    sharpe = np.array(sharpe_r(log_ret_df))
    df = pd.DataFrame(sharpe, columns=[element])
    stat = stat.append(df)

    stat.reset_index(inplace=True)

    # add column with stat name
    df_name = pd.DataFrame(STATISTICS, columns=["Statistics"])
    df_name[element] = stat[element]

    return df_name


def period_stat(prices_df, element, time_window):

    date_df = prices_df["Date"]

    first_date, last_date = window_period_back(date_df, time_window)

    sub_df = prices_df.loc[prices_df.Date.between(
        first_date, last_date, inclusive=True)]

    p_stat = statistics_calc(sub_df, element)

    return p_stat

# roll_max_price = single_price_series.rolling(
#     window=window, min_periods=1).max()

# daily_rolling_drawdown = single_price_series / roll_max_price - 1

# rolling_max_drawdown = daily_rolling_drawdown.rolling(
#     window=window, min_periods=1).min()
# fig, (ax0, ax1) = plt.subplots(2, 1)
# plt.rcParams['figure.figsize'] = [12, 16]
# daily_rolling_drawdown.plot(kind='area', ax=ax0)
# rolling_max_drawdown.plot(linewidth=3.0, ax=ax0)
# ax0.set_title(ticker + " Maximum rolling Drawdown for {} days".format(window))
# _ = nifty_levels_test['Close'].plot(ax=ax1, color='Blue')
# ax1.axvspan(nifty_levels_test.index[max_drawdown_peak_i],
#             nifty_levels_test.index[max_drawdown_start_j], alpha=0.5, color='red')
# ax1.axvspan(nifty_levels_test.index[max_drawdown_peak_i],
#             recovery_date, alpha=0.5, color='green')
# ax0.grid(True)
# ax0.set_xticklabels([])
# x_label = ax0.set_xlabel('')
# x_label.set_visible(False)
# fig.tight_layout()
# plt.show()


# print("Max Drawdown period for {} was between {} to {}".format(ticker,
#                                                                nifty_levels_test.index[max_drawdown_start_j].date(), nifty_levels_test.index[max_drawdown_peak_i].date()))
# print("Recovery was completed at {} post drawdown".format(recovery_date.date()))
# print("Max Drawdown Percentage  = {:2%}".format(max_DD_perc))
# print("Max Drawdown period = {} days".format(max_DD_perc_period_len))
# print("Max Drawdown recovery period = {} days".format(recovery_period))
