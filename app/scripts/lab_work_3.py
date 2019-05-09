import math
import operator
import statistics
import decimal

import numpy as np
from bokeh.util.string import encode_utf8
from flask import redirect, render_template, request, url_for

from app import app
from app.scripts.helpers import get_input_data, get_stat_distr


def get_select_sum(data, m=1):
    res_sum = 0
    for k, v in data.items():
        res_sum = res_sum + (k**m) * v
    return res_sum


def get_desper_select_sum(data, mean, m=1):
    res_sum = 0
    for k, v in data.items():
        res_sum = res_sum + ((k-mean)**m) * v
    return res_sum


@app.route('/lab_work_3', methods=['POST'])
def lab_work_3_post():
    items, res = get_input_data()
    m = list(map(int, request.form['m'].split(',')))
    st = get_stat_distr(res)

    sel_sum = get_select_sum(res)

    sel_average = statistics.mean(items)
    pvariance = statistics.pvariance(items, sel_average)
    variance = statistics.variance(items, sel_average)

    init_m = {x: (
        get_select_sum(res, x),
        get_select_sum(res, x)/len(items)) for x in m
    }
    mid_m = {
        x: (
            "%.25f" % float(get_desper_select_sum(res, sel_average, x)),
            "%.25f" % float(
                get_desper_select_sum(res, sel_average, x)/len(items)
            )
        ) for x in m
    }

    m3 = get_desper_select_sum(res, sel_average, 3)/len(items)
    m4 = get_desper_select_sum(res, sel_average, 4)/len(items)
    q3 = math.pow(math.sqrt(pvariance), 3)
    q4 = math.pow(math.sqrt(pvariance), 4)

    html = render_template(
        'lab_work_3/lab_work_3_res.html',
        action_url='/lab_work_3',
        items=items,
        sel_sum=sel_sum,
        m=m,
        init_m=init_m,
        mid_m=mid_m,
        k=', '.join(list(map(str, m))),
        R=max(items)-min(items),
        V=round((sel_average/math.sqrt(pvariance))*100, 3),
        A=m3/q3,
        E=(m3/q3)-3,
        pvariance=round(pvariance, 3),
        variance=round(variance, 3),
        pvariance_sqrt=round(math.sqrt(pvariance), 3),
        variance_sqrt=round(math.sqrt(variance), 3),
        sel_average=round(sel_average, 3),
        st=st
    )
    return encode_utf8(html)


@app.route('/lab_work_3', methods=['GET'])
def lab_work_3_get():
    html = render_template(
        'lab_work_3/lab_work_3.html',
        action_url='/lab_work_3'
    )
    return encode_utf8(html)
