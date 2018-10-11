from copy import deepcopy


def rule(data):
    result = []
    for k, v in data.items():
        result.append(v['code'])
    return result


def optimum(sub, result, path):
    if path != '/':
        path += '.'

    res = result
    for k in sub:
        result = deepcopy(res)
        temp = res
        res = []
        flag = False
        for data in result:
            if path + k not in data:
                flag = True
                res.append(data)
        if not flag:
            temp.sort(key=lambda d: rule(d))
            return temp[0]
    result.sort(key=lambda d: rule(d))
    return result[0]


def check(sub, parent,  sp='/', pp='/'):
    '''
    sp: sub_path
    pp: parent_path
    '''
    re = {'code': 0, 'result': {}, 'var': {}}
    if sp != '/':
        sp += '.'
    if pp != '/':
        pp += '.'

    for k, sv in sub.items():
        # 判断键值是否是 <value> 格式，如果是，则表明是变量赋值
        var_flag = isinstance(sv, str) and sv.startswith(
            '<') and sv.endswith('>')

        if sv == '-':
            if k not in parent:
                re['code'] = 0
            else:
                re['code'] = 0  # 预期键不存在，实际键存在
                re['result'][sp + k] = {'code': 4, 'sv': sv, 'pp': pp + k, 'pv': parent[k]}
        elif k in parent:
            pv = parent[k]
            code = 0

            if var_flag:
                re['var'][sv[1:-1]] = pv
                continue

            elif isinstance(sv, str):
                if not isinstance(pv, str):
                    code = 2  # 键值的数据类型不一致
                elif sv.startswith('*'):
                    if sv[1:] not in pv:
                        code = 1
                elif sv.startswith('^'):
                    if not pv.startswith(sv[1:]):
                        code = 1
                elif sv.startswith('$'):
                    if not pv.endswith(sv[1:]):
                        code = 1
                elif sv.startswith('#'):
                    if sv[1:] == pv:
                        code = 1
                elif sv.startswith('\\'):
                    sv = sv[1:]
                elif sv != pv:
                    code = 1  # 键值不等

            elif isinstance(sv, int):
                if not isinstance(pv, int):
                    code = 2  # 键值的数据类型不一致
                elif sv != pv:
                    code = 1  # 键值不等

            elif isinstance(sv, float):
                if not absisinstance(pv, float):
                    code = 2  # 键值的数据类型不一致
                elif sv != pv:
                    code = 1  # 键值不等

            elif isinstance(sv, list):
                if not isinstance(pv, list):
                    code = 2  # 键值的数据类型不一致
                elif not isinstance(sv[0], dict):
                    if sv != pv:
                        code = 1  # 键值不等
                else:
                    for i, sv_i in enumerate(sv):
                        result = []
                        flag = False
                        for j, pv_i in enumerate(pv):
                            r = check(sv_i, pv_i, sp + k + '[%s]' % i, pp + k + '[%s]' % j)
                            if r['code'] == 0:
                                # code = 0
                                flag = True
                                re['var'] = dict(re['var'], **r['var'])
                                break
                            else:
                                result.append(r['result'])
                        if result:
                            o = optimum(sv_i, result, sp + k + '[%s]' % i)
                        else:
                            o = {}
                        re['var'] = dict(re['var'], **re['var'])

                        if not flag:
                            re['code'] = 1
                            re['result'] = dict(re['result'], **o)


            elif isinstance(sv, dict):
                if not isinstance(pv, dict):
                    code = 2  # 键值的数据类型不一致
                else:
                    r = check(sv, pv, sp + k, pp + k)
                    if r['code'] == 0:
                       re['var'] = dict(re['var'], **r['var'])
                       continue
                    else:
                        re['result'] = dict(re['result'], **r['result'])

            if code == 1:
                re['code'] = 1
                re['result'][sp + k] = {'code': 1, 'sv': sv, 'pp': pp + k, 'pv': pv}
            elif code == 2:
                re['code'] = 2
                re['result'][sp + k] = {'code': 2, 'sv': sv, 'pp': pp + k, 'pv': pv}
        else:
            re['code'] = 3  # 键不存在
            if var_flag:
                re['var']['_' + sv[1:-1]] = None
            else:
                re['result'][sp + k] = {'code': 3, 'sv': sv, 'pp': None, 'pv': ''}

    re['code'] = len(re['result'])
    return re


if __name__ == '__main__':
    pass
