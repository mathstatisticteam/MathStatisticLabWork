import math
import statistics

import numpy as np
from bokeh.util.string import encode_utf8
from bokeh.resources import INLINE
from bokeh.embed import components
from flask import redirect, render_template, request, url_for

from app import app
from app.scripts.helpers import to_int_if_can, get_figure


def get_selective_averages(axis_arr, sum_arr, N, n=1):
    res = 0
    for index, v in enumerate(axis_arr):
        res += math.pow(v, n) * sum_arr[index]

    return round(res/N, 3)


@app.route('/lab_work_5', methods=['POST'])
def lab_work_5_post():
    x = []
    y = []

    form_data = request.form.to_dict()
    x_size = int(form_data['x'])
    y_size = int(form_data['y'])
    matrix = np.zeros((x_size-1, y_size-1), dtype=int)

    del form_data['x']
    del form_data['y']

    for k, v in form_data.items():
        i, j = list(map(int, k.split('x')))
        if v == '':
            continue
        if i == 0 and j != 0:
            y.append(to_int_if_can(v))
        elif i != 0 and j == 0:
            x.append(to_int_if_can(v))
        else:
            matrix[i-1][j-1] = to_int_if_can(v)

    sum_rows = [to_int_if_can(sum(matrix[i])) for i in range(x_size-1)]
    sum_cols = [to_int_if_can(sum(matrix[:, i])) for i in range(y_size-1)]
    sum_n = sum(sum_rows)

    averages_y_for_x = []
    averages_x_for_y = []
    res = 0

    for i in range(0, x_size-1):
        for index, v in enumerate(matrix[i]):
            if v == 0:
                continue
            res += v * y[index]

        averages_y_for_x.append(
            to_int_if_can(round(res/sum_rows[i], 3))
        )
        res = 0

    for j in range(0, y_size-1):
        for index, v in enumerate(matrix[:, j]):
            if v == 0:
                continue
            res += v * x[index]

        averages_x_for_y.append(
            to_int_if_can(round(res/sum_cols[j], 3))
        )
        res = 0

    selective_averages_x = get_selective_averages(x, sum_rows, sum_n)
    selective_averages_x_2 = get_selective_averages(x, sum_rows, sum_n, 2)
    sigma_x = math.sqrt(
        selective_averages_x_2 - math.pow(selective_averages_x, 2)
    )

    selective_averages_y = get_selective_averages(y, sum_cols, sum_n)
    selective_averages_y_2 = get_selective_averages(y, sum_cols, sum_n, 2)
    sigma_y = math.sqrt(
        selective_averages_y_2 - math.pow(selective_averages_y, 2)
    )

    sum_nxy_x_y = 0

    for i in range(0, x_size-1):
        for index, v in enumerate(matrix[i]):
            if v == 0:
                continue
            sum_nxy_x_y += v * y[index] * x[i]

    selective_correlation_coefficient = (
        sum_nxy_x_y - sum_n *
        selective_averages_x *
        selective_averages_y
    ) / (
        sum_n *
        sigma_x *
        sigma_y
    )

    f_x_1 = selective_correlation_coefficient * sigma_y / sigma_x
    # f_x_1 = selective_correlation_coefficient * sigma_x / sigma_y
    f_x_2 = selective_averages_y + ((selective_averages_x * -1) * f_x_1)
    # f_x_2 = selective_averages_x + (selective_averages_y * f_x_1)

    distr_conditional_averages_x = []
    distr_conditional_averages_y = []

    for e in x:
        distr_conditional_averages_x.append({
            'x': e,
            'y': round(f_x_1*e+f_x_2, 3)
        })

    # for e in y:
    #     distr_conditional_averages_y.append({
    #         'y': e,
    #         'x': round((f_x_2+e)/(f_x_1*-1), 3)
    #     })

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    fig = get_figure(x, averages_y_for_x, 'x', 'y')
    plot_1 = {}
    plot_1['script'], plot_1['div'] = components(fig)

    fig2 = get_figure(y, averages_x_for_y, 'x', 'y')
    plot_2 = {}
    plot_2['script'], plot_2['div'] = components(fig2)

    html = render_template(
        'lab_work_5/lab_work_5_res.html',
        action_url='/lab_work_5',
        js_resources=js_resources,
        css_resources=css_resources,
        plot_1=plot_1,
        plot_2=plot_2,
        x=x,
        y=y,
        matrix=matrix,
        sum_n=sum_n,
        sum_cols=sum_cols,
        sum_rows=sum_rows,
        averages_y_for_x=averages_y_for_x,
        averages_x_for_y=averages_x_for_y,
        selective_averages_x=selective_averages_x,
        selective_averages_y=selective_averages_y,
        sigma_x=round(sigma_x, 3),
        sigma_y=round(sigma_y, 3),
        selective_correlation_coefficient=round(
            selective_correlation_coefficient, 3
        ),
        f_x_1=round(f_x_1, 3),
        f_x_2=round(f_x_2, 3),
        distr_conditional_averages_x=distr_conditional_averages_x,
        distr_conditional_averages_y=distr_conditional_averages_y
    )
    return encode_utf8(html)


@app.route('/lab_work_5', methods=['GET'])
def lab_work_5_get():
    html = render_template(
        'lab_work_5/lab_work_5.html',
        action_url='/lab_work_5'
    )
    return encode_utf8(html)
