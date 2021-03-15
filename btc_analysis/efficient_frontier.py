import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# simulation


def sharpe_simulation(log_ret_df, stock_df, num_simulation=None,
                      days=252, chart="Y"):

    # the random seed makes sure that the code gets
    # the same random numbers every time for reproducibility
    np.random.seed(88)

    if num_simulation is None:

        num_simulation = 10000

    # initializing df and array
    all_weights = np.zeros((num_simulation, len(stock_df.columns)))
    ret_arr = np.zeros(num_simulation)
    vol_arr = np.zeros(num_simulation)
    sharpe_arr = np.zeros(num_simulation)

    for x in range(num_simulation):

        # find random weights and transfrom into fractions
        weights = np.array(np.random.random(len(stock_df.columns)))
        weights = weights/np.sum(weights)

        # recursively composing the weights array
        all_weights[x, :] = weights

        # recursively composing the Expected return array
        ret_arr[x] = np.sum((log_ret_df.mean() * weights * days))

        # recursively composing the Expected volatility array
        vol_arr[x] = np.sqrt(
            np.dot(weights.T, np.dot(log_ret_df.cov()*days, weights)))

        # recursively composing the Sharpe Ratio array
        sharpe_arr[x] = ret_arr[x] / vol_arr[x]

    if chart == "Y":

        # print chart
        dot_chart(ret_arr, vol_arr, sharpe_arr, all_weights)

    return ret_arr, vol_arr, sharpe_arr, all_weights


def min_max_ret(ret_arr):

    min_ret = ret_arr.min()
    max_ret = ret_arr.max()

    return min_ret, max_ret


def find_max(ret_arr, vol_arr, sharpe_arr, all_weights):

    max_sharpe_ret = ret_arr[sharpe_arr.argmax()]
    max_sharpe_vol = vol_arr[sharpe_arr.argmax()]

    max_weights = all_weights[sharpe_arr.argmax(), :]

    return max_sharpe_ret, max_sharpe_vol, max_weights


# the function will return an array with:
# return, volatility and sharpe ratio from any given set of weight

def ret_vol_sharpe_from_w(weights, log_ret_df, days=252):

    # redefine the df for the reverse engineering of the
    # function
    log_ret = pd.DataFrame(log_ret_df)

    weights = np.array(weights)
    #
    ret = np.sum(log_ret.mean() * weights) * days
    covar = log_ret.cov()
    vol = np.sqrt(np.dot(weights.T, np.dot(covar*days, weights)))
    sharpe = ret / vol

    return np.array([ret, vol, sharpe])


def neg_sharpe(weights, log_ret_df):

    return ret_vol_sharpe_from_w(weights, log_ret_df)[2] * - 1


def check_sum(weights):
    # return 0 if sum of the weights is 1
    return np.sum(weights)-1


def optmization_single(stock_df, log_ret_df):

    minimization_guess = 1 / len(stock_df.columns)

    cons = ({'type': 'eq', 'fun': check_sum})

    bounds = ()
    minimization_guess = 1 / len(stock_df.columns)
    initial_guess = [minimization_guess]

    for i in range(len(stock_df.columns)):

        bounds = bounds + ((0, 1),)
        if i < len(stock_df.columns) - 1:
            initial_guess.append(minimization_guess)
        else:
            pass

    optimization_res = minimize(neg_sharpe, initial_guess,
                                args=(log_ret_df,),
                                method='SLSQP', bounds=bounds,
                                constraints=cons)

    return optimization_res

# the efficient frontier objective is the minimum amount
# of risk for a certain level of the expected return


def minimize_vol(weights, log_ret_df):

    return ret_vol_sharpe_from_w(weights, log_ret_df)[1]


# the efficient frontier is the set of portfolios that gets
# us the highest expected return for any given risk level

def efficient_frontier(stock_df, log_ret_df, dimension=250,
                       min_ret=0, max_ret=1):

    frontier_y = np.linspace(min_ret, max_ret, dimension)
    frontier_x = []
    log_ret_c = pd.DataFrame(log_ret_df)
    all_weights = np.zeros((dimension, len(stock_df.columns)))

    for count, possible_return in enumerate(frontier_y):

        bounds = ()
        minimization_guess = 1 / len(stock_df.columns)
        initial_guess = [minimization_guess]

        for i in range(len(stock_df.columns)):

            bounds = bounds + ((0, 1),)
            if i < len(stock_df.columns) - 1:
                initial_guess.append(minimization_guess)
            else:
                pass

        cons = ({'type': 'eq', 'fun': check_sum},
                {'type': 'eq',
                 'fun': lambda w: ret_vol_sharpe_from_w(w, log_ret_c)[0] - possible_return})

        result = minimize(minimize_vol, initial_guess, args=(log_ret_df,),
                          method='SLSQP', bounds=bounds, constraints=cons)

        all_weights[count, :] = result.x

        # frontier x represent volatility
        frontier_x.append(result['fun'])

    return frontier_x, frontier_y, all_weights


def efficient_frontier_chart(frontier_x, frontier_y):

    plt.figure(figsize=(12, 8))
    plt.title('Efficient Frontier')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.plot(frontier_x, frontier_y, 'steelblue', linewidth=3)

    plt.savefig('markovitz\\file\\Efficient_Frontier.png')
    plt.show()

    return None


def double_ef_chart(f_x_1, f_y_1, f_x_2, f_y_2,
                    label_1='Efficient Frontier 1',
                    label_2='Efficient Frontier 2',
                    color_1='steelblue',
                    color_2='forestgreen'):

    plt.figure(figsize=(12, 8))
    plt.title('Efficient Frontier')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.plot(f_x_1, f_y_1, color_1, label=label_1, linewidth=3)
    plt.plot(f_x_2, f_y_2, color_2, label=label_2, linewidth=3)

    plt.savefig('markovitz\\file\\Efficient_Frontier_comp.png')
    plt.show()

    return fig


# python chart used to display CAPM allocation

def stacked_chart(total_df, label_list, title='CAPM Optimal Asset Allocation',
                  name='CAPM_allocation'):

    total_df.plot.area(x="Volatility", y=label_list, ylim=(0, 1))
    plt.title(title)
    plt.xlabel('Volatility')
    plt.ylabel('Weights')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.margins(0, 0)

    plt.savefig('markovitz\\file\\' + name + '.png')
    plt.show()

    return None


def dot_chart(ret_arr, vol_arr, sharpe_arr, all_weights, max_sharpe="Y"):

    max_sharpe_ret, max_sharpe_vol, _ = find_max(
        ret_arr, vol_arr, sharpe_arr, all_weights)

    plt.figure(figsize=(12, 8))
    plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis')
    plt.colorbar(label='Sharpe Ratio')
    plt.title('Portfolio Simulation')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    if max_sharpe == "Y":

        plt.scatter(max_sharpe_vol, max_sharpe_ret, c='red', s=50)

    plt.savefig('markovitz\\file\\Simulation_chart.png')
    plt.show()


def eff_front_op(stock_df, log_ret_df, simulation=None,
                 stock_to_remove=None):

    try:

        stock_df = stock_df.drop(columns=["Date"])

    except KeyError:
        pass

    label_list = stock_df.columns

    # perform the simulation
    ret_arr, _, _, _ = sharpe_simulation(
        log_ret_df, stock_df, num_simulation=simulation, chart="N")

    # find the min and max return based on the simulation and compute
    # the efficient frontier
    min_ret_tot, max_ret_tot = min_max_ret(ret_arr)

    if stock_to_remove is not None:

        comp_stock = stock_df.drop(columns=[stock_to_remove])
        comp_label_list = comp_stock.columns
        comp_logret = log_ret_df.drop(columns=[stock_to_remove])

        # perform the simulation
        comp_ret_arr, _, _, _ = sharpe_simulation(
            comp_logret, comp_stock, num_simulation=simulation, chart="N")

        # find the min and max return based on the simulation and compute
        # the efficient frontier
        min_ret_comp, max_ret_comp = min_max_ret(comp_ret_arr)
        min_ret = min(min_ret_comp, min_ret_tot)
        max_ret = max(max_ret_comp, max_ret_tot)

        fx, fy, all_weights = efficient_frontier(
            stock_df, log_ret_df, min_ret=min_ret_tot, max_ret=max_ret_tot)

        comp_fx, comp_fy, comp_weights = efficient_frontier(
            comp_stock, comp_logret, min_ret=min_ret_comp, max_ret=max_ret_comp)

        double_ef_chart(fx, fy, comp_fx, comp_fy,
                        label_1='Efficient Frontier w BTC',
                        label_2='Efficient Frontier w/o BTC',
                        color_1='darkorange',
                        color_2='forestgreen')

        # composing the total df containing vol, return and all the weights
        weight_df = pd.DataFrame(all_weights, columns=label_list)
        comp_weight_df = pd.DataFrame(comp_weights, columns=comp_label_list)

        # composing the df containing all the needed information
        tot_df = pd.DataFrame(columns=["Volatility", "Return"])
        tot_df["Volatility"] = fx
        tot_df["Return"] = fy
        tot_df = pd.concat([tot_df, weight_df], axis=1)

        comp_tot_df = pd.DataFrame(columns=["Volatility", "Return"])
        comp_tot_df["Volatility"] = comp_fx
        comp_tot_df["Return"] = comp_fy
        comp_tot_df = pd.concat([comp_tot_df, comp_weight_df], axis=1)

        # stacked_chart(tot_df, label_list,
        #               title='CAPM Optimal Asset Allocation w BTC',
        #               name='CAPM_allocation_BTC')
        # stacked_chart(comp_tot_df, comp_label_list,
        #               title='CAPM Optimal Asset Allocation w_o BTC',
        #               name='CAPM_allocation_no_BTC')

        return tot_df, comp_tot_df

    else:

        # composing the total df containing vol, return and all the weights
        weight_df = pd.DataFrame(all_weights, columns=label_list)

        tot_df = pd.DataFrame(columns=["Volatility", "Return"])
        tot_df["Volatility"] = fx
        tot_df["Return"] = fy
        tot_df = pd.concat([tot_df, weight_df], axis=1)

        # drawing the stacked chart af the CAPM and the efficient frontier
        efficient_frontier_chart(fx, fy)
        stacked_chart(tot_df, label_list)

        return tot_df
