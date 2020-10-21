import xlsxwriter
import pandas as pd
from datetime import datetime
from config import (
    VAR_GRAPH_LIST, GRAPH_COLOR, SP500_GRAPH_LIST,
    FORMAT_DICT, VAR_STATIC_LIST, EQUITY, BOND,
    CURRENCY, COMMODITY, CRYPTO, VARIOUS_LIST,
    VS_SP500_LIST)


# wk = writer.book
# worksheet = writer.sheets['Sheet_name_1']
# chart = wk.add_chart({'type': 'line'})


def var_to_excel(file_name, dyn_var_corr_3Y, dyn_var_corr_1Y,
                 dyn_var_corr_1Q, dyn_var_corr_1M,
                 stat_var_corr_all, stat_var_corr_3Y,
                 stat_var_corr_1Y,
                 stat_var_corr_1Q, stat_var_corr_1M,
                 dyn_SP500_corr_3Y):

    len_corr_mat = stat_var_corr_all.shape[0]
    space = 2
    space_left = 2

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:

        dyn_var_corr_3Y.to_excel(writer, sheet_name='3Y RW', index=False)
        format_sheets(writer, '3Y RW')
        format_header(writer, '3Y RW', VARIOUS_LIST, 0, 1)
        put_graph(writer, '3Y RW', dyn_var_corr_3Y,
                  graph_name='Correlation with Bitcoin on a 3 years rolling window')

        dyn_var_corr_1Y.to_excel(writer, sheet_name='1Y RW', index=False)
        format_sheets(writer, '1Y RW')
        format_header(writer, '1Y RW', VARIOUS_LIST, 0, 1)
        put_graph(writer, '1Y RW', dyn_var_corr_1Y,
                  graph_name='Correlation with Bitcoin on a 1 year rolling window')

        dyn_var_corr_1Q.to_excel(writer, sheet_name='1Q RW', index=False)
        format_sheets(writer, '1Q RW')
        format_header(writer, '1Q RW', VARIOUS_LIST, 0, 1)
        put_graph(writer, '1Q RW', dyn_var_corr_1Q,
                  graph_name='Correlation with Bitcoin on a 1 quarter rolling window')

        dyn_var_corr_1M.to_excel(writer, sheet_name='1M RW', index=False)
        format_sheets(writer, '1M RW')
        format_header(writer, '1M RW', VARIOUS_LIST, 0, 1)
        put_graph(writer, '1M RW', dyn_var_corr_1M,
                  graph_name='Correlation with Bitcoin on a 1 month rolling window')

        stat_var_corr_all.to_excel(
            writer, sheet_name='all_matrix',
            startrow=(space * 1), startcol=space_left, index=False)
        half_matrix_formatter(writer, 'all_matrix',
                              VAR_STATIC_LIST, 3, 3)
        stat_var_corr_3Y.to_excel(
            writer, sheet_name='all_matrix',
            startrow=(space*2 + len_corr_mat * 1), startcol=space_left, index=False)
        stat_var_corr_1Y.to_excel(
            writer, sheet_name='all_matrix',
            startrow=(space*3 + len_corr_mat * 2), startcol=space_left, index=False)
        stat_var_corr_1Q.to_excel(
            writer, sheet_name='all_matrix',
            startrow=(space*4 + len_corr_mat * 3), startcol=space_left, index=False)
        stat_var_corr_1M.to_excel(
            writer, sheet_name='all_matrix',
            startrow=(space * 5 + len_corr_mat * 4), startcol=space_left, index=False)
        static_sheet(writer, 'all_matrix')

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
                  stat_var_corr_1Y,
                  stat_var_corr_1Q, stat_var_corr_1M,
                  dyn_SP500_corr_3Y):

    today_str = datetime.now().strftime("%Y-%m-%d")
    file_name_var = today_str + "_Various-Correlations.xlsx"
    file_name_alt = today_str + "_Altcoin-Correlations.xlsx"

    var_to_excel(file_name_var, dyn_var_corr_3Y, dyn_var_corr_1Y,
                 dyn_var_corr_1Q, dyn_var_corr_1M,
                 stat_var_corr_all, stat_var_corr_3Y,
                 stat_var_corr_1Y, stat_var_corr_1Q, stat_var_corr_1M,
                 dyn_SP500_corr_3Y)

    #SP500_to_excel(file_name_var, dyn_SP500_corr_3Y)


def put_graph(writer_obj, sheet_name, df_to_graph,
              graph_name=None, graph_set=VAR_GRAPH_LIST):

    df_columns = df_to_graph.columns
    # last_df_row = df_to_graph.shape[0]
    last_df_row = 700

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

    chart.set_y_axis({'num_format': '0.00%',
                      'min': -0.5,
                      'max': 0.5
                      })

    chart.set_plotarea({
        'layout': {
            'x':      0.07,
            'y':      0.26,
            'width':  0.90,
            'height': 0.60,
        }
    })
    chart.set_legend({'position': 'bottom',
                      'font': {'size': 7, 'bold': True}
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

    worksheet.insert_chart('S5', chart, {'x_scale': 2, 'y_scale': 2})


def format_sheets(writer_obj, sheet_name):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    worksheet.hide_gridlines()

    format_neg_4 = workbook.add_format(FORMAT_DICT.get('blue'))
    format_neg_3 = workbook.add_format(FORMAT_DICT.get('sky_blue'))
    format_neg_2 = workbook.add_format(FORMAT_DICT.get('light_blue'))
    format_neg_1 = workbook.add_format(FORMAT_DICT.get('lighter_blue'))
    format_neutral = workbook.add_format(FORMAT_DICT.get('light_grey'))
    format_pos_1 = workbook.add_format(FORMAT_DICT.get('lighter_orange'))
    format_pos_2 = workbook.add_format(FORMAT_DICT.get('light_orange'))
    format_pos_3 = workbook.add_format(FORMAT_DICT.get('orange'))
    format_pos_4 = workbook.add_format(FORMAT_DICT.get('dark_orange'))

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': -1,
                                              'maximum': -0.75,
                                              'format': format_neg_4})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': -0.75,
                                              'maximum': -0.5,
                                              'format': format_neg_3})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': -0.5,
                                              'maximum': -0.25,
                                              'format': format_neg_2})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': -0.25,
                                              'maximum': -0.05,
                                              'format': format_neg_1})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': -0.05,
                                              'maximum': 0.05,
                                              'format': format_neutral})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': 0.05,
                                              'maximum': 0.25,
                                              'format': format_pos_1})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': 0.25,
                                              'maximum': 0.5,
                                              'format': format_pos_2})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': 0.5,
                                              'maximum': 0.75,
                                              'format': format_pos_3})

    worksheet.conditional_format('B2:R2499', {'type': 'cell',
                                              'criteria': 'between',
                                              'minimum': 0.75,
                                              'maximum': 1,
                                              'format': format_pos_4})


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


def static_sheet(writer_obj, sheet_name):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    header = VAR_STATIC_LIST
    try:

        header.remove("Date")

    except ValueError:
        pass

    len_head = len(header)
    space = 2

    for j in range(5):

        j = j + 1

        for i, var in enumerate(header):

            row_start = space * j + len_head * (j - 1) + 1
            worksheet.write(row_start + i, 1, var)


def half_matrix_formatter(writer_obj, sheet_name, header,
                          row_start, col_start):

    workbook = writer_obj.book
    writer_obj.book = workbook
    worksheet = writer_obj.sheets[sheet_name]

    c_format = workbook.add_format({'bg_color': '#FFFFFF'})

    try:

        header.remove("Date")

    except ValueError:
        pass

    for j in range(col_start, len(header) + 2):

        for i in range(j-2):

            worksheet.write_blank(
                row_start + i, j, '', c_format)
