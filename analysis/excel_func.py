import xlsxwriter
import pandas as pd
from datetime import datetime
from config import (
    VAR_GRAPH_LIST, GRAPH_COLOR, SP500_GRAPH_LIST,
    FORMAT_DICT, VAR_STATIC_LIST, EQUITY, BOND,
    CURRENCY, COMMODITY, CRYPTO, VARIOUS_LIST,
    VS_SP500_LIST, ASSET_CATEGORY, TIME_WINDOW,
    CRYPTO_STATIC_LIST, CRYPTO_LIST, CRYPTO_GRAPH_LIST)


def alt_to_excel(file_name, dyn_ret_list, stat_ret_list,
                 dyn_alt_corr_3Y, dyn_alt_corr_1Y,
                 dyn_alt_corr_1Q, dyn_alt_corr_1M,
                 stat_alt_corr_all, stat_alt_corr_3Y,
                 stat_alt_corr_1Y,
                 stat_alt_corr_1Q, stat_alt_corr_1M):

    len_corr_mat = stat_alt_corr_all.shape[0]
    space = 5
    space_left = 2

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        dyn_alt_corr_3Y.to_excel(writer, sheet_name='3Y RW', index=False)
        print(dyn_alt_corr_3Y)
        format_sheets(writer, '3Y RW')
        format_header(writer, '3Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '3Y RW', dyn_alt_corr_3Y,
                  graph_name='Correlation with Bitcoin on a 3 years rolling window',
                  graph_set=CRYPTO_GRAPH_LIST)

        dyn_alt_corr_1Y.to_excel(writer, sheet_name='1Y RW', index=False)
        format_sheets(writer, '1Y RW')
        format_header(writer, '1Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Y RW', dyn_alt_corr_1Y,
                  graph_name='Correlation with Bitcoin on a 1 year rolling window',
                  graph_set=CRYPTO_GRAPH_LIST)

        dyn_alt_corr_1Q.to_excel(writer, sheet_name='1Q RW', index=False)
        format_sheets(writer, '1Q RW')
        format_header(writer, '1Q RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Q RW', dyn_alt_corr_1Q,
                  graph_name='Correlation with Bitcoin on a 1 quarter rolling window',
                  graph_set=CRYPTO_GRAPH_LIST)

        dyn_alt_corr_1M.to_excel(writer, sheet_name='1M RW', index=False)
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
        # asset_formatter(writer, 'all_matrix', len(
        #     stat_ret_list) + space + 2, space_left)

        stat_alt_corr_3Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 2 + len_corr_mat * 1),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 2) + 1 + len_corr_mat * 1,
                              space_left + 1)
        # asset_formatter(writer, 'all_matrix', len(
        #     stat_ret_list) + (space * 2) + 2 + len_corr_mat * 1, space_left)

        stat_alt_corr_1Y.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 3 + len_corr_mat * 2),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 3) + 1 + len_corr_mat * 2,
                              space_left + 1)
        # asset_formatter(writer, 'all_matrix', len(
        #     stat_ret_list) + (space * 3) + 2 + len_corr_mat * 2, space_left)

        stat_alt_corr_1Q.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 4 + len_corr_mat * 3),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 4) + 1 + len_corr_mat * 3,
                              space_left + 1)
        # asset_formatter(writer, 'all_matrix', len(
        #     stat_ret_list) + (space * 4) + 2 + len_corr_mat * 3, space_left)

        stat_alt_corr_1M.to_excel(
            writer, sheet_name='Correlation Matrix',
            startrow=(space * 5 + len_corr_mat * 4),
            startcol=space_left, index=False)
        half_matrix_formatter(writer, 'Correlation Matrix',
                              stat_ret_list,
                              (space * 5) + 1 + len_corr_mat * 4,
                              space_left + 1)
        # asset_formatter(writer, 'all_matrix', len(
        #     stat_ret_list) + (space * 5) + 2 + len_corr_mat * 4, space_left)

        static_sheet(writer, 'Correlation Matrix', space, space_left,
                     TIME_WINDOW, CRYPTO_STATIC_LIST)
        format_sheets(writer, 'Correlation Matrix')


def var_to_excel(file_name, dyn_ret_list, stat_ret_list,
                 dyn_var_corr_3Y, dyn_var_corr_1Y,
                 dyn_var_corr_1Q, dyn_var_corr_1M,
                 stat_var_corr_all, stat_var_corr_3Y,
                 stat_var_corr_1Y,
                 stat_var_corr_1Q, stat_var_corr_1M,
                 dyn_SP500_corr_3Y):

    len_corr_mat = stat_var_corr_all.shape[0]
    space = 5
    space_left = 2

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        dyn_var_corr_3Y.to_excel(writer, sheet_name='3Y RW', index=False)
        format_sheets(writer, '3Y RW')
        format_header(writer, '3Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '3Y RW', dyn_var_corr_3Y,
                  graph_name='Correlation with Bitcoin on a 3 years rolling window')

        dyn_var_corr_1Y.to_excel(writer, sheet_name='1Y RW', index=False)
        format_sheets(writer, '1Y RW')
        format_header(writer, '1Y RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Y RW', dyn_var_corr_1Y,
                  graph_name='Correlation with Bitcoin on a 1 year rolling window')

        dyn_var_corr_1Q.to_excel(writer, sheet_name='1Q RW', index=False)
        format_sheets(writer, '1Q RW')
        format_header(writer, '1Q RW', dyn_ret_list, 0, 1)
        put_graph(writer, '1Q RW', dyn_var_corr_1Q,
                  graph_name='Correlation with Bitcoin on a 1 quarter rolling window')

        dyn_var_corr_1M.to_excel(writer, sheet_name='1M RW', index=False)
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
                     TIME_WINDOW, VAR_STATIC_LIST)
        format_sheets(writer, 'Correlation Matrix')

        dyn_SP500_corr_3Y.to_excel(
            writer, sheet_name='3Y RW S&P500', index=False)
        format_sheets(writer, '3Y RW S&P500')
        format_header(writer, '3Y RW S&P500', VS_SP500_LIST, 0, 1)
        put_graph(writer, '3Y RW S&P500', dyn_SP500_corr_3Y,
                  graph_name='Correlation with S&P500 on a 3 years rolling window',
                  graph_set=SP500_GRAPH_LIST)


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

    if "BSV" in df_columns:

        chart.set_y_axis({'num_format': '0.00%',
                          'min': -0.30,
                          'max': 1.10
                          })
    else:

        if "1M" in sheet_name:

            chart.set_y_axis({'num_format': '0.00%',
                              'min': -0.95,
                              'max': 0.95
                              })

        elif "S&P500" in sheet_name:

            chart.set_y_axis({'num_format': '0.00%',
                              'min': -1,
                              'max': 0.85
                              })

        else:

            chart.set_y_axis({'num_format': '0.00%',
                              'min': -0.7,
                              'max': 0.7
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
        'reverse': True,
        # 'min': '2017-12-31',
        'minor_unit':      1,
        'minor_unit_type': 'months',
        'major_unit':      90,
        'major_unit_type': 'months',
        'num_format':      'dd/mm/yyyy',
    })

    if "BSV" in df_columns:

        worksheet.insert_chart('O5', chart, {'x_scale': 2, 'y_scale': 2})

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


def format_finder(writer_obj, element, position="H"):

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


def static_sheet(writer_obj, sheet_name, space,
                 space_left, window_arr, header_set):

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

            format_to_use = format_finder(writer_obj, var)
            format_to_use_v = format_finder(writer_obj, var, position='V')

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
        last_col = first_col + len(CRYPTO) - 1

    elif value_to_put == 'Commodity':

        bg_color = '#6AA84F'
        first_col = first_col + len(CRYPTO)
        last_col = first_col + len(COMMODITY) - 1

    elif value_to_put == 'Currency':

        bg_color = '#0000FF'
        first_col = first_col + len(CRYPTO) + len(COMMODITY)
        last_col = first_col + len(CURRENCY) - 1

    elif value_to_put == 'Equity':

        bg_color = '#444444'
        first_col = first_col + len(CRYPTO) + len(COMMODITY) + len(CURRENCY)
        last_col = first_col + (len(EQUITY) - 1) - 1

    elif value_to_put == 'Volatility':

        bg_color = '#CCCCCC'
        first_col = first_col + \
            len(CRYPTO) + len(COMMODITY) + len(CURRENCY) + (len(EQUITY) - 1)
        last_col = first_col + 1 - 1

    elif value_to_put == 'Bond':

        bg_color = '#999999'
        first_col = first_col + \
            len(CRYPTO) + len(COMMODITY) + \
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


def asset_formatter(writer_obj, sheet_name, first_row, first_col):

    for element in ASSET_CATEGORY:

        merging_excel(writer_obj, sheet_name,
                      element, first_row, first_col)
