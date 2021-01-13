import xlsxwriter
import pandas as pd
from datetime import datetime

from btc_analysis.config import (
    DB_NAME, INDEX_DB_NAME
)
from btc_analysis.calc import (
    return_retrieve, price_retrieve
)
from btc_analysis.config import (
    VAR_GRAPH_LIST, GRAPH_COLOR, SP500_GRAPH_LIST,
    FORMAT_DICT, VAR_STATIC_LIST, EQUITY, BOND,
    CURRENCY, COMMODITY, CRYPTO, VARIOUS_LIST,
    VS_SP500_LIST, ASSET_CATEGORY, TIME_WINDOW,
    CRYPTO_STATIC_LIST, CRYPTO_LIST, CRYPTO_GRAPH_LIST,
    CRYPTO_FOR_STATIC, METAL_GRAPH_LIST, METAL_LIST,
    CRYPTO_FOR_STATIC_YAHOO, COMMODITY_YAHOO, EQUITY_YAHOO,
    BOND_YAHOO, VAR_STATIC_LIST_Y
)


def date_reformat(return_df, writer_obj, sheet_name):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    return_df["Date"] = [datetime.strptime(
        x, "%Y-%m-%d") for x in return_df["Date"]]

    format_date = workbook.add_format({'num_format': 'dd/mm/yy'})

    for i, date in enumerate(return_df["Date"]):

        worksheet.write(i + 1, 0, date, format_date)


def metal_to_excel(file_name, dyn_ret_list,
                   dyn_met_corr_3Y, dyn_met_corr_1Y,
                   dyn_met_corr_1Q, dyn_met_corr_1M):

    price_df = price_retrieve("metal_prices")
    return_df = return_retrieve("metal_returns")

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        dyn_met_corr_3Y.to_excel(writer, sheet_name='3Y RW', index=False)
        date_reformat(dyn_met_corr_3Y, writer, '3Y RW')
        format_sheets(writer, '3Y RW')
        format_header(writer, '3Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '3Y RW', dyn_met_corr_3Y,
                  graph_name='Correlation with Bitcoin on a 3 years rolling window',
                  graph_set=METAL_GRAPH_LIST)

        dyn_met_corr_1Y.to_excel(writer, sheet_name='1Y RW', index=False)
        date_reformat(dyn_met_corr_1Y, writer, '1Y RW')
        format_sheets(writer, '1Y RW')
        format_header(writer, '1Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Y RW', dyn_met_corr_1Y,
                  graph_name='Correlation with Bitcoin on a 1 year rolling window',
                  graph_set=METAL_GRAPH_LIST)

        dyn_met_corr_1Q.to_excel(writer, sheet_name='1Q RW', index=False)
        date_reformat(dyn_met_corr_1Q, writer, '1Q RW')
        format_sheets(writer, '1Q RW')
        format_header(writer, '1Q RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Q RW', dyn_met_corr_1Q,
                  graph_name='Correlation with Bitcoin on a 1 quarter rolling window',
                  graph_set=METAL_GRAPH_LIST)

        dyn_met_corr_1M.to_excel(writer, sheet_name='1M RW', index=False)
        date_reformat(dyn_met_corr_1M, writer, '1M RW')
        format_sheets(writer, '1M RW')
        format_header(writer, '1M RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1M RW', dyn_met_corr_1M,
                  graph_name='Correlation with Bitcoin on a 1 month rolling window',
                  graph_set=METAL_GRAPH_LIST)


def alt_to_excel(file_name, dyn_ret_list, stat_ret_list,
                 dyn_alt_corr_3Y, dyn_alt_corr_1Y,
                 dyn_alt_corr_1Q, dyn_alt_corr_1M,
                 stat_alt_corr_all, stat_alt_corr_3Y,
                 stat_alt_corr_1Y,
                 stat_alt_corr_1Q, stat_alt_corr_1M):

    len_corr_mat = stat_alt_corr_all.shape[0]
    space = 5
    space_left = 2

    # retrieve return from MongoDB
    alt_price_df = price_retrieve("crypto_price", db_name=INDEX_DB_NAME)
    alt_ret_df = return_retrieve("crypto_price_return", db_name=INDEX_DB_NAME)

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        alt_price_df.to_excel(
            writer, sheet_name='Cryptocurrencies Prices', index=False)
        date_reformat(alt_price_df, writer, 'Cryptocurrencies Prices')
        format_header(writer, 'Cryptocurrencies Prices', dyn_ret_list, 0, 1)

        alt_ret_df.to_excel(
            writer, sheet_name='Cryptocurrencies Returns', index=False)
        date_reformat(alt_ret_df, writer, 'Cryptocurrencies Returns')
        format_header(writer, 'Cryptocurrencies Returns', dyn_ret_list, 0, 1)

        dyn_alt_corr_3Y.to_excel(writer, sheet_name='3Y RW', index=False)
        date_reformat(dyn_alt_corr_3Y, writer, '3Y RW')
        format_sheets(writer, '3Y RW')
        format_header(writer, '3Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '3Y RW', dyn_alt_corr_3Y,
                  graph_name='Correlation with Bitcoin on a 3 years rolling window',
                  graph_set=CRYPTO_GRAPH_LIST)

        dyn_alt_corr_1Y.to_excel(writer, sheet_name='1Y RW', index=False)
        date_reformat(dyn_alt_corr_1Y, writer, '1Y RW')
        format_sheets(writer, '1Y RW')
        format_header(writer, '1Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Y RW', dyn_alt_corr_1Y,
                  graph_name='Correlation with Bitcoin on a 1 year rolling window',
                  graph_set=CRYPTO_GRAPH_LIST)

        dyn_alt_corr_1Q.to_excel(writer, sheet_name='1Q RW', index=False)
        date_reformat(dyn_alt_corr_1Q, writer, '1Q RW')
        format_sheets(writer, '1Q RW')
        format_header(writer, '1Q RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Q RW', dyn_alt_corr_1Q,
                  graph_name='Correlation with Bitcoin on a 1 quarter rolling window',
                  graph_set=CRYPTO_GRAPH_LIST)

        dyn_alt_corr_1M.to_excel(writer, sheet_name='1M RW', index=False)
        date_reformat(dyn_alt_corr_1M, writer, '1M RW')
        format_sheets(writer, '1M RW')
        format_header(writer, '1M RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1M RW', dyn_alt_corr_1M,
                  graph_name='Correlation with Bitcoin on a 1 month rolling window',
                  graph_set=CRYPTO_GRAPH_LIST)

        # static correlation matrix
        stat_alt_corr_all.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 1),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 1) + 1, space_left + 1)
        format_header(writer, 'Correlation Matrix', stat_ret_list,
                      len(stat_ret_list) + space + 1, space_left)

        stat_alt_corr_3Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 2 + len_corr_mat * 1),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 2) + 1 + len_corr_mat * 1,
                              space_left + 1)

        stat_alt_corr_1Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 3 + len_corr_mat * 2),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 3) + 1 + len_corr_mat * 2,
                              space_left + 1)

        stat_alt_corr_1Q.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 4 + len_corr_mat * 3),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 4) + 1 + len_corr_mat * 3,
                              space_left + 1)

        stat_alt_corr_1M.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 5 + len_corr_mat * 4),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 5) + 1 + len_corr_mat * 4,
                              space_left + 1)

        static_sheet(writer, 'Correlation Matrix', space, space_left,
                     TIME_WINDOW, CRYPTO_STATIC_LIST, "various")
        format_sheets(writer, 'Correlation Matrix')


def var_to_excel(file_name, dyn_ret_list, stat_ret_list,
                 dyn_var_corr_3Y, dyn_var_corr_1Y,
                 dyn_var_corr_1Q, dyn_var_corr_1M,
                 stat_var_corr_all, stat_var_corr_3Y,
                 stat_var_corr_1Y,
                 stat_var_corr_1Q, stat_var_corr_1M,
                 dyn_SP500_corr_3Y
                 ):

    len_corr_mat = stat_var_corr_all.shape[0]
    space = 5
    space_left = 2

    price_df = price_retrieve("all_prices")
    return_df = return_retrieve("all_returns")

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        price_df.to_excel(
            writer, sheet_name='Prices', index=False)
        date_reformat(price_df, writer, 'Prices')
        format_header(writer, 'Prices', dyn_ret_list, 0, 1)

        return_df.to_excel(
            writer, sheet_name='Returns', index=False)
        date_reformat(return_df, writer, 'Returns')
        format_header(writer, 'Returns', dyn_ret_list, 0, 1)

        dyn_var_corr_3Y.to_excel(writer, sheet_name='3Y RW', index=False)
        date_reformat(dyn_var_corr_3Y, writer, '3Y RW')
        format_sheets(writer, '3Y RW')
        format_header(writer, '3Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '3Y RW', dyn_var_corr_3Y,
                  graph_name='Correlation with Bitcoin on a 3 years rolling window')

        dyn_var_corr_1Y.to_excel(writer, sheet_name='1Y RW', index=False)
        date_reformat(dyn_var_corr_1Y, writer, '1Y RW')
        format_sheets(writer, '1Y RW')
        format_header(writer, '1Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Y RW', dyn_var_corr_1Y,
                  graph_name='Correlation with Bitcoin on a 1 year rolling window')

        dyn_var_corr_1Q.to_excel(writer, sheet_name='1Q RW', index=False)
        date_reformat(dyn_var_corr_1Q, writer, '1Q RW')
        format_sheets(writer, '1Q RW')
        format_header(writer, '1Q RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Q RW', dyn_var_corr_1Q,
                  graph_name='Correlation with Bitcoin on a 1 quarter rolling window')

        dyn_var_corr_1M.to_excel(writer, sheet_name='1M RW', index=False)
        date_reformat(dyn_var_corr_1M, writer, '1M RW')
        format_sheets(writer, '1M RW')
        format_header(writer, '1M RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1M RW', dyn_var_corr_1M,
                  graph_name='Correlation with Bitcoin on a 1 month rolling window')

        # static correlation matrix
        stat_var_corr_all.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 1),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 1) + 1, space_left + 1)
        format_header(writer, 'Correlation Matrix', stat_ret_list,
                      len(stat_ret_list) + space + 1, space_left)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + space + 2, space_left)

        stat_var_corr_3Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 2 + len_corr_mat * 1),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 2) + 1 + len_corr_mat * 1,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 2) + 2 + len_corr_mat * 1, space_left)

        stat_var_corr_1Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 3 + len_corr_mat * 2),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 3) + 1 + len_corr_mat * 2,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 3) + 2 + len_corr_mat * 2, space_left)

        stat_var_corr_1Q.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 4 + len_corr_mat * 3),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 4) + 1 + len_corr_mat * 3,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 4) + 2 + len_corr_mat * 3, space_left)

        stat_var_corr_1M.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 5 + len_corr_mat * 4),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 5) + 1 + len_corr_mat * 4,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 5) + 2 + len_corr_mat * 4, space_left)

        static_sheet(writer, 'Correlation Matrix', space, space_left,
                     TIME_WINDOW, VAR_STATIC_LIST, "various")
        format_sheets(writer, 'Correlation Matrix')


def yahoo_to_excel(file_name, dyn_ret_list, stat_ret_list,
                   dyn_yahoo_corr_3Y, dyn_yahoo_corr_1Y,
                   dyn_yahoo_corr_1Q, dyn_yahoo_corr_1M,
                   stat_yahoo_corr_all, stat_yahoo_corr_3Y,
                   stat_yahoo_corr_1Y,
                   stat_yahoo_corr_1Q, stat_yahoo_corr_1M
                   ):

    len_corr_mat = stat_yahoo_corr_all.shape[0]
    space = 5
    space_left = 2

    price_df = price_retrieve("all_prices_y")
    return_df = return_retrieve("all_returns_y")

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        price_df.to_excel(
            writer, sheet_name='Prices', index=False)
        date_reformat(price_df, writer, 'Prices')
        format_header_yahoo(writer, 'Prices', dyn_ret_list, 0, 1)

        return_df.to_excel(
            writer, sheet_name='Returns', index=False)
        date_reformat(return_df, writer, 'Returns')
        format_header_yahoo(writer, 'Returns', dyn_ret_list, 0, 1)

        dyn_yahoo_corr_3Y.to_excel(writer, sheet_name='3Y RW', index=False)
        date_reformat(dyn_yahoo_corr_3Y, writer, '3Y RW')
        format_sheets(writer, '3Y RW')
        format_header_yahoo(writer, '3Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '3Y RW', dyn_yahoo_corr_3Y,
                  graph_name='Correlation with Bitcoin on a 3 years rolling window')

        dyn_yahoo_corr_1Y.to_excel(writer, sheet_name='1Y RW', index=False)
        date_reformat(dyn_yahoo_corr_1Y, writer, '1Y RW')
        format_sheets(writer, '1Y RW')
        format_header_yahoo(writer, '1Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Y RW', dyn_yahoo_corr_1Y,
                  graph_name='Correlation with Bitcoin on a 1 year rolling window')

        dyn_yahoo_corr_1Q.to_excel(writer, sheet_name='1Q RW', index=False)
        date_reformat(dyn_yahoo_corr_1Q, writer, '1Q RW')
        format_sheets(writer, '1Q RW')
        format_header_yahoo(writer, '1Q RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Q RW', dyn_yahoo_corr_1Q,
                  graph_name='Correlation with Bitcoin on a 1 quarter rolling window')

        dyn_yahoo_corr_1M.to_excel(writer, sheet_name='1M RW', index=False)
        date_reformat(dyn_yahoo_corr_1M, writer, '1M RW')
        format_sheets(writer, '1M RW')
        format_header_yahoo(writer, '1M RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1M RW', dyn_yahoo_corr_1M,
                  graph_name='Correlation with Bitcoin on a 1 month rolling window')

        # static correlation matrix
        stat_yahoo_corr_all.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 1),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 1) + 1, space_left + 1)
        format_header_yahoo(writer, 'Correlation Matrix', stat_ret_list,
                            len(stat_ret_list) + space + 1, space_left)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + space + 2,
            space_left, set_="yahoo")

        stat_yahoo_corr_3Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 2 + len_corr_mat * 1),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 2) + 1 + len_corr_mat * 1,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 2) + 2 + len_corr_mat * 1,
            space_left, set_="yahoo")

        stat_yahoo_corr_1Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 3 + len_corr_mat * 2),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 3) + 1 + len_corr_mat * 2,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 3) + 2 + len_corr_mat * 2,
            space_left, set_="yahoo")

        stat_yahoo_corr_1Q.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 4 + len_corr_mat * 3),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 4) + 1 + len_corr_mat * 3,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 4) + 2 + len_corr_mat * 3,
            space_left, set_="yahoo")

        stat_yahoo_corr_1M.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 5 + len_corr_mat * 4),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 5) + 1 + len_corr_mat * 4,
                              space_left + 1)
        asset_formatter(writer, 'Correlation Matrix', len(
            stat_ret_list) + (space * 5) + 2 + len_corr_mat * 4,
            space_left, set_="yahoo")

        static_sheet(writer, 'Correlation Matrix', space, space_left,
                     TIME_WINDOW, VAR_STATIC_LIST_Y, "yahoo")
        format_sheets(writer, 'Correlation Matrix')


def SP500_to_excel(file_name, dyn_SP500_corr_3Y):

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        dyn_SP500_corr_3Y.to_excel(
            writer, sheet_name='3Y RW S&P500', index=False)
        put_graph(writer, '3Y RW S&P500', dyn_SP500_corr_3Y,
                  graph_name='Correlation with S&P500 on a 3 years rolling window',
                  graph_set=SP500_GRAPH_LIST)


def corr_to_excel(dyn_var_corr_3Y, dyn_var_corr_1Y,
                  dyn_var_corr_1Q, dyn_var_corr_1M,
                  stat_var_corr_all, stat_var_corr_3Y,
                  stat_var_corr_1Y, stat_var_corr_1Q,
                  stat_var_corr_1M, dyn_SP500_corr_3Y,
                  dyn_alt_corr_3Y, dyn_alt_corr_1Y,
                  dyn_alt_corr_1Q, dyn_alt_corr_1M,
                  stat_alt_corr_all, stat_alt_corr_3Y,
                  stat_alt_corr_1Y, stat_alt_corr_1Q,
                  stat_alt_corr_1M):

    today_str = datetime.now().strftime("%Y-%m-%d")
    file_name_var = today_str + "_Various-Correlations.xlsx"
    file_name_alt = today_str + "_Altcoin-Correlations.xlsx"

    var_to_excel(file_name_var, VARIOUS_LIST, VAR_STATIC_LIST,
                 dyn_var_corr_3Y, dyn_var_corr_1Y,
                 dyn_var_corr_1Q, dyn_var_corr_1M,
                 stat_var_corr_all, stat_var_corr_3Y,
                 stat_var_corr_1Y, stat_var_corr_1Q, stat_var_corr_1M,
                 dyn_SP500_corr_3Y)

    alt_to_excel(file_name_alt, CRYPTO_LIST, CRYPTO_STATIC_LIST,
                 dyn_alt_corr_3Y, dyn_alt_corr_1Y,
                 dyn_alt_corr_1Q, dyn_alt_corr_1M,
                 stat_alt_corr_all, stat_alt_corr_3Y,
                 stat_alt_corr_1Y,
                 stat_alt_corr_1Q, stat_alt_corr_1M)


def metal_corr_to_excel(dyn_met_corr_3Y, dyn_met_corr_1Y,
                        dyn_met_corr_1Q, dyn_met_corr_1M):

    today_str = datetime.now().strftime("%Y-%m-%d")
    file_name_met = today_str + "_Metal-Correlations.xlsx"

    metal_to_excel(file_name_met, METAL_LIST,
                   dyn_met_corr_3Y, dyn_met_corr_1Y,
                   dyn_met_corr_1Q, dyn_met_corr_1M)


def put_graph(writer_obj, sheet_name, df_to_graph,
              graph_name=None, graph_set=VAR_GRAPH_LIST):

    df_columns = df_to_graph.columns

    last_df_row = 680

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    # Create a chart object.
    chart = workbook.add_chart({'type': 'line'})

    chart.set_title({
        'name': graph_name
    })

    # Configure the series of the chart from the dataframe data.
    # for i in range(len(df_columns)):
    for i, head in enumerate(df_columns):

        col = i
        # using a list of values instead of category/value formulas:
        #     [sheetname, first_row, first_col, last_row, last_col]
        if head in graph_set:

            chart.add_series({
                'name':       [sheet_name, 0, col],
                'categories': [sheet_name, 1, 0, last_df_row, 0],
                'values': [sheet_name, 1, col, last_df_row, col],
                'line': GRAPH_COLOR.get(head)
            })
        else:
            pass

    if "ETH" in df_columns:

        if "1M" in sheet_name:

            min_ = -0.95
            max_ = 1.2

        else:

            min_ = -0.7
            max_ = 1.1

    else:

        if "S&P500" in sheet_name:

            min_ = -1
            max_ = 0.85

        else:

            min_ = -0.7
            max_ = 0.7

    chart.set_y_axis({'num_format': '0.00%',
                      'min': min_,
                      'max': max_
                      })

    chart.set_plotarea({
        'layout': {
            'x':      0.10,
            'y':      0.10,  # 0.26
            'width':  0.90,
            'height': 0.75,  # 0.6
        }
    })
    chart.set_legend({'position': 'bottom',
                      'font': {'size': 7,
                               'bold': True}
                      })

    chart.set_x_axis({
        'label_position': 'low',
        'date_axis': True,
        # 'reverse': True,
        'minor_unit':      3,
        'minor_unit_type': 'months',
        'major_unit':      3,
        'major_unit_type': 'months',
        # 'num_format': 'dd/mm/yyyy',
        'num_format': 'mmm-yy',
        'num_font':  {'rotation': -30}
    })

    if "BSV" in df_columns:

        worksheet.insert_chart('O5', chart, {'x_scale': 2, 'y_scale': 2})

    elif "Copper" in df_columns:

        worksheet.insert_chart('G5', chart, {'x_scale': 2, 'y_scale': 2})

    elif "ETH" in df_columns:

        worksheet.insert_chart('Y5', chart, {'x_scale': 2, 'y_scale': 2})

    else:

        worksheet.insert_chart('S5', chart, {'x_scale': 2, 'y_scale': 2})


def format_sheets(writer_obj, sheet_name):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    format_neg_4 = workbook.add_format(FORMAT_DICT.get('blue'))
    format_neg_3 = workbook.add_format(FORMAT_DICT.get('sky_blue'))
    format_neg_2 = workbook.add_format(FORMAT_DICT.get('light_blue'))
    format_neg_1 = workbook.add_format(FORMAT_DICT.get('lighter_blue'))
    format_neutral = workbook.add_format(FORMAT_DICT.get('light_grey'))
    format_pos_1 = workbook.add_format(FORMAT_DICT.get('lighter_orange'))
    format_pos_2 = workbook.add_format(FORMAT_DICT.get('light_orange'))
    format_pos_3 = workbook.add_format(FORMAT_DICT.get('orange'))
    format_pos_4 = workbook.add_format(FORMAT_DICT.get('dark_orange'))
    format_white = workbook.add_format(FORMAT_DICT.get('white'))

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': -1,
                                               'maximum': -0.75,
                                               'format': format_neg_4})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': -0.75,
                                               'maximum': -0.5,
                                               'format': format_neg_3})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': -0.5,
                                               'maximum': -0.25,
                                               'format': format_neg_2})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': -0.25,
                                               'maximum': -0.05,
                                               'format': format_neg_1})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': -0.05,
                                               'maximum': -0.00002,
                                               'format': format_neutral})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': -0.00001,
                                               'maximum': 0.00001,
                                               'format': format_white})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': 0.00002,
                                               'maximum': 0.05,
                                               'format': format_neutral})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': 0.05,
                                               'maximum': 0.25,
                                               'format': format_pos_1})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': 0.25,
                                               'maximum': 0.5,
                                               'format': format_pos_2})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': 0.5,
                                               'maximum': 0.75,
                                               'format': format_pos_3})

    worksheet.conditional_format('A1:AR2499', {'type': 'cell',
                                               'criteria': 'between',
                                               'minimum': 0.75,
                                               'maximum': 1,
                                               'format': format_pos_4})


def format_finder(writer_obj, element, position="H", corr_set="various"):

    workbook = writer_obj.book
    writer_obj.book = workbook

    if position == "V":

        # vertical format
        format_equity = workbook.add_format(FORMAT_DICT.get('equity_grey_v'))
        format_currency = workbook.add_format(
            FORMAT_DICT.get('currency_blue_v'))
        format_bond = workbook.add_format(FORMAT_DICT.get('bond_grey_v'))
        format_commodity = workbook.add_format(
            FORMAT_DICT.get('commodity_green_v'))
        format_crypto = workbook.add_format(FORMAT_DICT.get('crypto_orange_v'))

    else:

        # horizontal format
        format_equity = workbook.add_format(FORMAT_DICT.get('equity_grey'))
        format_currency = workbook.add_format(FORMAT_DICT.get('currency_blue'))
        format_bond = workbook.add_format(FORMAT_DICT.get('bond_grey'))
        format_commodity = workbook.add_format(
            FORMAT_DICT.get('commodity_green'))
        format_crypto = workbook.add_format(FORMAT_DICT.get('crypto_orange'))

    if corr_set == "various":

        if element in CRYPTO:

            return format_crypto

        elif element in CURRENCY:

            return format_currency

        elif element in EQUITY:

            return format_equity

        elif element in COMMODITY:

            return format_commodity

        elif element in BOND:

            return format_bond

    elif corr_set == "yahoo":

        if element in CRYPTO:

            return format_crypto

        elif element in CURRENCY:

            return format_currency

        elif element in EQUITY_YAHOO:

            return format_equity

        elif element in COMMODITY_YAHOO:

            return format_commodity

        elif element in BOND_YAHOO:

            return format_bond


def format_header(writer_obj, sheet_name, header, row_start, col_start):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    format_equity = workbook.add_format(FORMAT_DICT.get('equity_grey'))
    format_currency = workbook.add_format(FORMAT_DICT.get('currency_blue'))
    format_bond = workbook.add_format(FORMAT_DICT.get('bond_grey'))
    format_commodity = workbook.add_format(FORMAT_DICT.get('commodity_green'))
    format_crypto = workbook.add_format(FORMAT_DICT.get('crypto_orange'))

    for i, element in enumerate(header):

        if element in CRYPTO:

            worksheet.write(row_start, col_start +
                            i, element, format_crypto)

        elif element in CURRENCY:

            worksheet.write(row_start, col_start +
                            i, element, format_currency)

        elif element in EQUITY:

            worksheet.write(row_start, col_start +
                            i, element, format_equity)

        elif element in COMMODITY:

            worksheet.write(row_start, col_start +
                            i, element, format_commodity)

        elif element in BOND:

            worksheet.write(row_start, col_start +
                            i, element, format_bond)


def format_header_yahoo(writer_obj, sheet_name, header, row_start, col_start):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    format_equity = workbook.add_format(FORMAT_DICT.get('equity_grey'))
    format_currency = workbook.add_format(FORMAT_DICT.get('currency_blue'))
    format_bond = workbook.add_format(FORMAT_DICT.get('bond_grey'))
    format_commodity = workbook.add_format(FORMAT_DICT.get('commodity_green'))
    format_crypto = workbook.add_format(FORMAT_DICT.get('crypto_orange'))

    for i, element in enumerate(header):

        if element in CRYPTO:

            worksheet.write(row_start, col_start +
                            i, element, format_crypto)

        elif element in CURRENCY:

            worksheet.write(row_start, col_start +
                            i, element, format_currency)

        elif element in EQUITY_YAHOO:

            worksheet.write(row_start, col_start +
                            i, element, format_equity)

        elif element in COMMODITY_YAHOO:

            worksheet.write(row_start, col_start +
                            i, element, format_commodity)

        elif element in BOND_YAHOO:

            worksheet.write(row_start, col_start +
                            i, element, format_bond)


def static_sheet(writer_obj, sheet_name, space,
                 space_left, window_arr, header_set,
                 corr_set):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    c_format = workbook.add_format({'bg_color': '#FFFFFF'})

    w_format = workbook.add_format({'font_color': '#000000',
                                    'align': 'center',
                                    'valign': 'vcenter',
                                    'bold': True,
                                    })
    w_format.set_right()

    header = header_set
    try:

        header.remove("Date")

    except ValueError:
        pass

    len_head = len(header)
    under_row_start = len_head + space + 1
    above_row_start = space

    for j in range(5):

        # time window display
        static_window = TIME_WINDOW[j]
        worksheet.write(above_row_start, space_left - 1,
                        static_window, w_format)

        j = j + 1

        for i, var in enumerate(header):

            format_to_use = format_finder(writer_obj, var, corr_set=corr_set)
            format_to_use_v = format_finder(
                writer_obj, var, position='V', corr_set=corr_set)

            # column names
            row_start = space * j + len_head * (j - 1) + 1
            worksheet.write(row_start + i, 1, var, format_to_use_v)

            # row names
            worksheet.write(under_row_start, space_left +
                            i, var, format_to_use)

            # row up removing
            worksheet.write_blank(
                above_row_start, space_left + i, '', c_format)

        under_row_start = under_row_start + len_head + space
        above_row_start = above_row_start + len_head + space


def half_matrix_formatter(writer_obj, sheet_name, header,
                          row_start, col_start):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    canc_format = workbook.add_format({'bg_color': '#FFFFFF'})

    try:

        header.remove("Date")

    except ValueError:
        pass

    for j in range(col_start, len(header) + 2):

        for i in range(j-2):

            worksheet.write_blank(
                row_start + i, j, '', canc_format)


def merging_excel(writer_obj, sheet_name, value_to_put, first_row, first_col):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    if value_to_put == 'Crypto-currency':

        bg_color = '#FF9900'
        first_col = first_col
        last_col = first_col + len(CRYPTO_FOR_STATIC) - 1

    elif value_to_put == 'Commodity':

        bg_color = '#6AA84F'
        first_col = first_col + len(CRYPTO_FOR_STATIC)
        last_col = first_col + len(COMMODITY) - 1

    elif value_to_put == 'Currency':

        bg_color = '#0000FF'
        first_col = first_col + len(CRYPTO_FOR_STATIC) + len(COMMODITY)
        last_col = first_col + len(CURRENCY) - 1

    elif value_to_put == 'Equity':

        bg_color = '#444444'
        first_col = first_col + \
            len(CRYPTO_FOR_STATIC) + len(COMMODITY) + len(CURRENCY)
        last_col = first_col + (len(EQUITY) - 1) - 1

    elif value_to_put == 'Volatility':

        bg_color = '#CCCCCC'
        first_col = first_col + \
            len(CRYPTO_FOR_STATIC) + len(COMMODITY) + \
            len(CURRENCY) + (len(EQUITY) - 1)
        last_col = first_col + 1 - 1

    elif value_to_put == 'Bond':

        bg_color = '#999999'
        first_col = first_col + \
            len(CRYPTO_FOR_STATIC) + len(COMMODITY) + \
            len(CURRENCY) + (len(EQUITY) - 1) + 1
        last_col = first_col + len(BOND) - 1

    merge_format = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': bg_color,
        'font_color': '#FFFFFF'
    })

    # (first_row, first_col, last_row, last_col, data[, cell_format])
    if value_to_put == 'Volatility':

        worksheet.write(first_row, first_col, value_to_put, merge_format)

    else:

        worksheet.merge_range(first_row, first_col, first_row,
                              last_col, value_to_put, merge_format)


def merging_excel_yahoo(writer_obj, sheet_name, value_to_put,
                        first_row, first_col):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    if value_to_put == 'Crypto-currency':

        bg_color = '#FF9900'
        first_col = first_col
        last_col = first_col + len(CRYPTO_FOR_STATIC_YAHOO) - 1

    elif value_to_put == 'Commodity':

        bg_color = '#6AA84F'
        first_col = first_col + len(CRYPTO_FOR_STATIC_YAHOO)
        last_col = first_col + len(COMMODITY_YAHOO) - 1

    elif value_to_put == 'Currency':

        bg_color = '#0000FF'
        first_col = first_col + \
            len(CRYPTO_FOR_STATIC_YAHOO) + len(COMMODITY_YAHOO)
        last_col = first_col + len(CURRENCY) - 1

    elif value_to_put == 'Equity':

        bg_color = '#444444'
        first_col = first_col + \
            len(CRYPTO_FOR_STATIC_YAHOO) + len(COMMODITY_YAHOO) + len(CURRENCY)
        last_col = first_col + (len(EQUITY_YAHOO) - 1) - 1

    elif value_to_put == 'Volatility':

        bg_color = '#CCCCCC'
        first_col = first_col + \
            len(CRYPTO_FOR_STATIC_YAHOO) + len(COMMODITY_YAHOO) + \
            len(CURRENCY) + (len(EQUITY_YAHOO) - 1)
        last_col = first_col + 1 - 1

    elif value_to_put == 'Bond':

        bg_color = '#999999'
        first_col = first_col + \
            len(CRYPTO_FOR_STATIC_YAHOO) + len(COMMODITY_YAHOO) + \
            len(CURRENCY) + (len(EQUITY_YAHOO) - 1) + 1
        last_col = first_col + len(BOND_YAHOO) - 1

    merge_format = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': bg_color,
        'font_color': '#FFFFFF'
    })

    # (first_row, first_col, last_row, last_col, data[, cell_format])
    if value_to_put == 'Volatility':

        worksheet.write(first_row, first_col, value_to_put, merge_format)

    else:

        worksheet.merge_range(first_row, first_col, first_row,
                              last_col, value_to_put, merge_format)


def asset_formatter(writer_obj, sheet_name, first_row,
                    first_col, set_="various"):

    for element in ASSET_CATEGORY:

        if set_ == "various":

            merging_excel(writer_obj, sheet_name,
                          element, first_row, first_col)

        elif set_ == "yahoo":

            merging_excel_yahoo(writer_obj, sheet_name,
                                element, first_row, first_col)


# ############# BITCOIN STATISTICS ##############


def statistics_to_excel(file_name, stat_df, eff_fr_df, tot_df,
                        comp_tot_df):

    column = list(stat_df.columns)
    column.remove("Statistics")
    only_name = stat_df["Statistics"]
    only_stat = stat_df[column]

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        start = 0
        only_name.to_excel(writer, sheet_name='Statistics', index=False)

        for obj in column:

            start = start + 1
            obj_stat = only_stat[obj]
            obj_stat.to_excel(writer, sheet_name='Statistics',
                              index=False, startcol=start)

        eff_fr_df.to_excel(
            writer, sheet_name='Efficient Frontier', index=False)
        ef_graph(writer, 'Efficient Frontier', eff_fr_df,
                 graph_name='Efficient Frontier')

        tot_df.to_excel(writer, sheet_name='Allocation w BTC', index=False)

        comp_tot_df.to_excel(
            writer, sheet_name='Allocation w_o BTC', index=False)

        stacked_area_chart(writer, 'Allocation w BTC', tot_df,
                           graph_name='CAPM w BTC', graph_set=None)

        stacked_area_chart(writer, 'Allocation w_o BTC', comp_tot_df,
                           graph_name='CAPM w_o BTC', graph_set=None)


def ef_graph(writer_obj, sheet_name, df_to_graph,
             graph_name=None, graph_set=None):

    df_columns = df_to_graph.columns
    last_df_row = 251

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    # Create a chart object.
    chart = workbook.add_chart({'type': 'line'})

    chart.set_title({
        'name': graph_name
    })

    graph_set = ["Return w BTC", "Return w_o BTC"]

    # Configure the series of the chart from the dataframe data.
    # for i in range(len(df_columns)):
    for i, head in enumerate(df_columns):

        if head in graph_set:

            col = i
            # using a list of values instead of category/value formulas:
            #     [sheetname, first_row, first_col, last_row, last_col]

            chart.add_series({
                'name':       [sheet_name, 0, col],
                'categories': [sheet_name, 1, 0, last_df_row, 0],
                'values': [sheet_name, 1, col, last_df_row, col],
                'line': GRAPH_COLOR.get(head)
            })

        else:
            pass

    chart.set_y_axis({'num_format': '0.00%',
                      #   'min': 0.0,
                      #   'max': 0.
                      })

    chart.set_plotarea({
        'layout': {
            'x':      0.10,
            'y':      0.10,  # 0.26
            'width':  0.90,
            'height': 0.75,  # 0.6
        }
    })
    chart.set_legend({'position': 'bottom',
                      'font': {'size': 7,
                               'bold': True}
                      })

    chart.set_x_axis({
        'label_position': 'low',
        'num_format': '0.00%',
        'min': 0,
        'max': 0.8,
        'minor_unit':      20,
        'major_unit':      20,
        'num_font':  {'rotation': -30}
    })

    worksheet.insert_chart('C5', chart, {'x_scale': 2, 'y_scale': 2})


def stacked_area_chart(writer_obj, sheet_name, df_to_graph,
                       graph_name=None, graph_set=None):

    df_columns = list(df_to_graph.columns)
    df_columns.remove("Volatility")
    df_columns.remove("Return")

    last_df_row = 251

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    chart = workbook.add_chart({'type': 'line', 'subtype': 'stacked'})

    chart.set_title({
        'name': graph_name
    })

    if graph_set is None:

        graph_set = df_columns

    # Configure the series of the chart from the dataframe data.
    # for i in range(len(df_columns)):
    for i, head in enumerate(df_columns):

        if head in graph_set:

            col = i + 2
            # using a list of values instead of category/value formulas:
            #     [sheetname, first_row, first_col, last_row, last_col]

            chart.add_series({
                'name':       [sheet_name, 0, col],
                'categories': [sheet_name, 1, 0, last_df_row, 0],
                'values': [sheet_name, 1, col, last_df_row, col],
                'line': GRAPH_COLOR.get(head)
            })

        else:
            pass

    chart.set_y_axis({'num_format': '0.00%',
                      #   'min': 0.0,
                      #   'max': 0.
                      })

    chart.set_plotarea({
        'layout': {
            'x':      0.10,
            'y':      0.10,  # 0.26
            'width':  0.90,
            'height': 0.75,  # 0.6
        }
    })
    chart.set_legend({'position': 'bottom',
                      'font': {'size': 7,
                               'bold': True}
                      })

    chart.set_x_axis({
        'label_position': 'low',
        'num_format': '0.00%',
        'min': 0,
        'max': 0.8,
        'minor_unit':      20,
        'major_unit':      20,
        'num_font':  {'rotation': -30}
    })

    worksheet.insert_chart('C5', chart, {'x_scale': 2, 'y_scale': 2})
