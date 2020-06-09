from copy import deepcopy


def rule(data):
    result = []
    for k in data:
        result.append(data[k]['code'])
    return result


def optimum(sub, result, path):
    # if path != '/':
    #     path += '.'

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


def list2dict(data):
    keys = ['['+str(i)+']' for i in range(len(data))]
    return dict(zip(keys, data))


def check(sub, parent,  sp='/', pp='/'):
    '''
    sp: sub_path
    pp: parent_path
    '''
    re = {'code': 0, 'result': {}, 'var': {}, 'none':[]}
    # if sp != '/':
    #     sp += '.'
    # if pp != '/':
    #     pp += '.'
  
    def _in(k, data):
        try:
            return  eval('data[k]')
        except:
            return ''      


    for k, sv in sub.items():
        # 判断键值是否是 <value> 格式，如果是，则表明是变量赋值
        var_flag = isinstance(sv, str) and sv.startswith(
            '<') and sv.endswith('>')
        index = ''

        if '[' in k:
            s = k.split('[', 1)
            index = '[' + s[1]
            k = s[0]

        _k = '[\'' + k + '\']' + index

        # 预期键不存在
        if sv == '-':
            # 预期键不存在，实际键存在
            if k in parent:
                re['result'][sp + _k] = {'code': 4, 'sv': sv, 'pp': pp + _k, 'pv': parent[k]}

        # 预期键存在
        elif sv == '+':
            # 预期键存在，实际键不存在
            if k not in parent:
                re['result'][sp + _k] = {'code': 3, 'sv': sv, 'pp': None, 'pv': None}

        elif k in parent:
            if index:
                try:
                    pv = eval('parent[k]' + index)
                except:
                    if var_flag:
                        re['var'][sv[1:-1]] = None
                        re['none'].append(sv[1:-1])
                    else:                    
                        re['result'][sp + _k] = {'code': 3, 'sv': sv, 'pp': None, 'pv': None}
                    continue
            else:   
                pv = parent[k]

            code = 0

            if var_flag:
                re['var'][sv[1:-1]] = pv
                continue

            elif isinstance(sv, str):
                if sv.startswith('#'):
                    if sv[1:] == str(pv):
                        code = 1
                elif sv.startswith('<>'):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv == float(sv[2:]):
                        code = 1                          
                elif sv.startswith('>='):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv < float(sv[2:]):
                        code = 1                        
                elif sv.startswith('>'):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv <= float(sv[1:]):
                        code = 1
                elif sv.startswith('<='):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv > float(sv[2:]):
                        code = 1                        
                elif sv.startswith('<'):
                    if (isinstance(pv, int) or isinstance(pv, float)) and pv >= float(sv[1:]):
                        code = 1                                                                         
                elif not isinstance(pv, str):
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
                if not isinstance(pv, float):
                    code = 2  # 键值的数据类型不一致
                elif sv != pv:
                    code = 1  # 键值不等

            elif isinstance(sv, list):
                if not isinstance(pv, list):
                    code = 2  # 键值的数据类型不一致
            
                else:
                    for i in range(len(sv)):  # 把二级列表转换为 dict                         
                        if isinstance(sv[i], list):
                            sv[i] = list2dict(sv[i])
                    for i in range(len(pv)):  # 把二级列表转换为 dict                            
                        if isinstance(pv[i], list):
                            pv[i] = list2dict(pv[i]) 

                    if isinstance(sv[0], dict):  # list 子项为 dict
                        for i, sv_i in enumerate(sv):
                            result = []
                            flag = False
                            for j, pv_i in enumerate(pv):
                                r = check(sv_i, pv_i, sp + _k + '[%s]' % i, pp + _k + '[%s]' % j)
                                if r['code'] == 0:
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
                                re['result'] = dict(re['result'], **o)

                    else:  # list 子项为 int/str/float/None/False/True
                        for v in sv:
                            if v not in pv:
                                code = 5  # 预期的 list 值在实际值的 list 不存在
                                re['result'][sp + _k] = {'code': 5, 'sv': sv, 'pp': pp + _k, 'pv': pv}

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
                        for k in r['var']:
                            r['var'][k] = None
                            if k not in re['none']:
                                re['none'].append(k)
                        re['var'] = dict(re['var'], **r['var'])


            if code != 0:
                re['result'][sp + _k] = {'code': code, 'sv': sv, 'pp': pp + _k, 'pv': pv}
        else:  # 键不存在
            if var_flag:
                re['var'][sv[1:-1]] = None
                re['none'].append(sv[1:-1])
            else:            
                re['result'][sp + _k] = {'code': 3, 'sv': sv, 'pp': None, 'pv': None}

    re['code'] = len(re['result'])
    return re


if __name__ == '__main__':
    pass
