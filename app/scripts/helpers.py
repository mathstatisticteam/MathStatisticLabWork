from flask import request


def to_int_if_can(num):
    num = float(num)
    return int(num) if (num).is_integer() else num


def get_input_data():
    input_type = request.form['input_type']
    separator = {
        'space': ' ',
        'coma': ',',
        'semicolon': ';'
    }.get(request.form['separator'])

    if input_type == 'some_data':
        items = list(
            map(to_int_if_can, request.form['items'].split(separator))
        )
    elif input_type == 'stat_distr':
        data = request.form['items'].split(separator)
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
        w_nak = round(cnt / len(arr), 3)
        st.append({
            'x': x,
            'n': arr[x],
            'w': round(arr[x] / len(arr), 3),
            'n_nak': cnt,
            'w_nak': w_nak
        })
    
    return st
