import operator
import statistics
from bokeh.embed import components
from bokeh.models import ColumnDataSource, LabelSet, Arrow, NormalHead, Span
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from flask import redirect, render_template, request, url_for

from . import app


def get_figure(x, y, x_axis_label, y_axis_label):
    source = ColumnDataSource(data=dict(x=x, y=y))

    fig = figure(
        height=600,
        sizing_mode='stretch_width',
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label
    )
    labels = LabelSet(x='x', y='y', text='y', level='glyph',
                      x_offset=-15, y_offset=8, source=source, render_mode='canvas')
    fig.add_layout(labels)
    fig.line(x='x', y='y', line_color="blue", source=source, line_width=2)
    fig.circle(x='x', y='y', fill_color="blue",
               line_color="blue", size=8, source=source)

    return fig


def get_empirical_figure(x, y, data):
    fig = figure(
        height=600,
        sizing_mode='stretch_width',
        x_axis_label='X',
        y_axis_label='F(x)'
    )

    x.append(x[len(x)-1]+1)
    y.append(y[len(y)-1])
    fig.circle(x=x, y=y, fill_alpha=0)

    for i in range(0, len(data)):
        x=data[i+1].get('x') if i != len(data)-1 else data[i].get('x')+1
        fig.add_layout(Arrow(
            end=NormalHead(size=10, fill_color="blue"),
            line_color="blue",
            line_width=2,
            x_start=x,
            y_start=data[i].get('w_nak'),
            x_end=data[i].get('x'),
            y_end=data[i].get('w_nak')
        ))
        fig.add_layout(Span(
            location=data[i].get('x'),
            dimension='height', line_color='black',
            line_dash='dashed', line_width=1
        ))

    return fig


@app.route('/lab_work_1', methods=['POST'])
def bokehPost():
    st = []
    cnt = w_nak = 0
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    items = list(map(float, request.form["items"].split(' ')))
    items.sort()

    res = {x: items.count(x) for x in items}
    mode = [str(k) for k, v in res.items() if v == max(res.values())]
    median = statistics.median(items)

    for x in res:
        cnt = cnt + res[x]
        w_nak = round(cnt / len(items), 2)
        st.append({'x': x, 'n': res[x], 'w': round(
            res[x] / len(items), 2), 'n_nak': cnt, 'w_nak': w_nak})

    x = [s.get('x') for s in st]

    fig = get_figure(x, [s.get('n') for s in st], 'X', 'N')
    plot_1 = {}
    plot_1['script'], plot_1['div'] = components(fig)

    fig2 = get_figure(x, [s.get('w') for s in st], 'X', 'W')
    plot_2 = {}
    plot_2['script'], plot_2['div'] = components(fig2)

    fig3 = get_figure(x, [s.get('n_nak') for s in st], 'X', 'N нак')
    plot_3 = {}
    plot_3['script'], plot_3['div'] = components(fig3)

    fig4 = get_figure(x, [s.get('w_nak') for s in st], 'X', 'W нак')
    plot_4 = {}
    plot_4['script'], plot_4['div'] = components(fig4)
    
    fig5 = get_empirical_figure(x, [s.get('w_nak') for s in st], st)
    plot_5 = {}
    plot_5['script'], plot_5['div'] = components(fig5)

    html = render_template(
        'lab_work_1_res.html',
        sum=0,
        mode=", ".join(mode),
        median=median,
        items=items,
        st=st,
        plot_1=plot_1,
        plot_2=plot_2,
        plot_3=plot_3,
        plot_4=plot_4,
        plot_5=plot_5,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


@app.route('/lab_work_1', methods=['GET'])
def bokehGet():
    html = render_template('lab_work_1.html')
    return encode_utf8(html)
