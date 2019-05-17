from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure
from flask import request


def to_int_if_can(num):
    num = float(num)
    return int(num) if (num).is_integer() else num


def get_input_data(field_name = 'items'):
    input_type = request.form['input_type']
    separator = {
        'space': ' ',
        'coma': ',',
        'semicolon': ';'
    }.get(request.form['separator'])

    if input_type == 'some_data':
        items = list(
            map(to_int_if_can, request.form[field_name].split(separator))
        )
    elif input_type == 'stat_distr':
        data = request.form[field_name].strip(' ').split(separator)
        items = sum([
            [k for x in range(v)] for k, v in {
                to_int_if_can(x.split(':')[0]): int(x.split(':')[1]) for x in data
            }.items()
        ], [])

    items.sort()
    res = {x: items.count(x) for x in items}

    return [items, res]


def get_stat_distr(arr):
    st = []
    cnt = w_nak = 0

    for x in arr:
        cnt = cnt + arr[x]
        w_nak = round(cnt / sum(arr.values()), 3)
        st.append({
            'x': x,
            'n': arr[x],
            'w': round(arr[x] / len(arr), 3),
            'n_nak': cnt,
            'w_nak': w_nak
        })

    return st


def get_figure(x, y, x_axis_label, y_axis_label):
    source = ColumnDataSource(data=dict(x=x, y=y))

    fig = figure(
        height=600,
        sizing_mode='stretch_width',
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label
    )
    labels = LabelSet(
        x='x',
        y='y',
        text='y',
        level='glyph',
        x_offset=-15,
        y_offset=8,
        source=source,
        render_mode='canvas',
        text_font_size="8pt"
    )
    fig.add_layout(labels)
    fig.line(x='x', y='y', line_color="blue", source=source, line_width=2)
    fig.circle(
        x='x',
        y='y',
        fill_color="blue",
        line_color="blue",
        size=8,
        source=source
    )
    fig.yaxis.fixed_location = 0

    return fig


def get_reg_line_figure(x, y, x2, y2, x_axis_label, y_axis_label):
    source = ColumnDataSource(data=dict(x=x, y=y))
    source2 = ColumnDataSource(data=dict(x=x2, y=y2))

    fig = figure(
        height=600,
        sizing_mode='stretch_width',
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label
    )
    labels = LabelSet(
        x='x',
        y='y',
        text='y',
        level='glyph',
        x_offset=-15,
        y_offset=8,
        source=source,
        render_mode='canvas',
        text_font_size="8pt"
    )
    fig.add_layout(labels)
    fig.line(x='x', y='y', line_color="red", source=source2, line_width=2)
    fig.line(x='x', y='y', line_color="blue", source=source, line_width=2)
    fig.circle(
        x='x',
        y='y',
        fill_color="blue",
        line_color="blue",
        size=8,
        source=source
    )
    fig.circle(
        x='x',
        y='y',
        fill_color="red",
        line_color="red",
        size=8,
        source=source2
    )
    fig.yaxis.fixed_location = 0

    return fig
