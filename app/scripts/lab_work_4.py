import math
import statistics

import numpy as np
from bokeh.util.string import encode_utf8
from flask import redirect, render_template, request, url_for

from app import app
from app.scripts.helpers import get_input_data, get_stat_distr


@app.route('/lab_work_4', methods=['POST'])
def lab_work_4_post():
    group_1_items, group_1_res = get_input_data()
    group_2_items, group_2_res = get_input_data('items2')

    st1 = get_stat_distr(group_1_res)
    st2 = get_stat_distr(group_2_res)

    N1 = len(group_1_items)
    N2 = len(group_2_items)

    mean1 = statistics.mean(group_1_items)
    mean2 = statistics.mean(group_2_items)
    common_mean = (N1 * mean1 + N2 * mean2) / (N1 + N2)

    pvariance1 = statistics.pvariance(group_1_items, mean1)
    pvariance2 = statistics.pvariance(group_2_items, mean2)
    inner_variance = (N1 * pvariance1 + N2 * pvariance2) / (N1 + N2)
    intergroup_variance = (N1 * math.pow(mean1-common_mean, 2) +
                           N2 * math.pow(mean2-common_mean, 2)) / (N1 + N2)
    common_variance = inner_variance + intergroup_variance

    html = render_template(
        'lab_work_4/lab_work_4_res.html',
        action_url='/lab_work_4',
        st1=st1,
        st2=st2,
        mean1=mean1,
        mean2=mean2,
        common_mean=common_mean,
        pvariance1=pvariance1,
        pvariance2=pvariance2,
        inner_variance=inner_variance,
        intergroup_variance=intergroup_variance,
        common_variance=common_variance
    )
    return encode_utf8(html)


@app.route('/lab_work_4', methods=['GET'])
def lab_work_4_get():
    html = render_template(
        'lab_work_4/lab_work_4.html',
        action_url='/lab_work_4'
    )
    return encode_utf8(html)
