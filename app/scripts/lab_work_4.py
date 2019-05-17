import math
import statistics

import numpy as np
from bokeh.util.string import encode_utf8
from flask import redirect, render_template, request, url_for

from app import app
from app.scripts.helpers import get_input_data, get_stat_distr


@app.route('/lab_work_4', methods=['POST'])
def lab_work_4_post():
    groupe_cnt = int(request.form['groupeCnt'])
    groups_data = []
    common_N = 0
    common_mean_sum = 0
    inner_variance_sum = 0

    for i in range(groupe_cnt):
        group_items, group_res = get_input_data("items%s" % str(i))
        st = get_stat_distr(group_res)
        N = len(group_items)
        common_N += N
        mean = statistics.mean(group_items)
        pvariance = statistics.pvariance(group_items, mean)
        groups_data.append({
            'index': i+1,
            'st': st,
            'N': N,
            'mean': mean,
            'pvariance': pvariance
        })
        common_mean_sum += N * mean
        inner_variance_sum += N * pvariance

    common_mean = common_mean_sum / common_N
    inner_variance = inner_variance_sum / common_N
    intergroup_variance = 0

    for data in groups_data:
        intergroup_variance += (
            data['N'] * math.pow(data['mean']-common_mean, 2)
        ) / common_N

    common_variance = inner_variance + intergroup_variance

    html = render_template(
        'lab_work_4/lab_work_4_res.html',
        action_url='/lab_work_4',
        groups_data=groups_data,
        common_mean=round(common_mean, 3),
        inner_variance=round(inner_variance, 3),
        intergroup_variance=round(intergroup_variance, 3),
        common_variance=round(common_variance, 3)
    )
    return encode_utf8(html)


@app.route('/lab_work_4', methods=['GET'])
def lab_work_4_get():
    html = render_template(
        'lab_work_4/lab_work_4.html',
        action_url='/lab_work_4'
    )
    return encode_utf8(html)
