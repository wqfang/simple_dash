# from dash import html, dash_table


def conditional_formatting(conditional_formats):
    '''
    Create a conditional formatting dictionary for dash_table.DataTable.

    Parameters
    ----------
    conditional_formats : list of tuples
        [(column_title, condition, text color, background_color)]. In this way, the "condition" replaces "#" with the column title to make the final condition. For example, you might have:
            [('days_since_last_eval', '# > 10', 'black', 'red')]

    Returns
    -------
    dict
        the final conditional formatting dictionary
    '''
    style_data_conditional = []

    for c in conditional_formats:
        style_conditional = {
            'if': {
                'filter_query': c[1].replace('#', '{' + c[0] + '}'),
                'column_id': c[0]
            },
            'color': c[2],
            'backgroundColor': c[3]
        }
        
        style_data_conditional.append(style_conditional)

    return style_data_conditional

