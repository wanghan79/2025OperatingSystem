import random
import string

def generate(**kwargs):
    result = []
    num = kwargs.get('num', 1)
    for _ in range(num):
        res = {}
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif isinstance(v, dict):
                if 'datarange' in v:
                    it = iter(v['datarange'])
                    if isinstance(v['datarange'], tuple):
                        if isinstance(next(it), int):
                            it = iter(v['datarange'])
                            tmp = random.randint(next(it), next(it))
                            res[k] = tmp
                        else:
                            it = iter(v['datarange'])
                            tmp = random.uniform(next(it), next(it))
                            res[k] = tmp
                    elif isinstance(v['datarange'], str):
                        length = v.get('len', 1)
                        tmp = ''.join(random.choice(v['datarange']) for _ in range(length))
                        res[k] = tmp
                else:
                    res[k] = generate(**v)[0]  # 递归处理嵌套字典
            elif isinstance(v, list):
                sub_res = []
                for sub_struct in v:
                    if isinstance(sub_struct, dict):
                        sub_res.extend(generate(**sub_struct))
                res[k] = sub_res
            elif isinstance(v, tuple):
                sub_res = []
                for sub_struct in v:
                    if isinstance(sub_struct, dict):
                        sub_res.extend(generate(**sub_struct))
                res[k] = tuple(sub_res)
        result.append(res)
    return result

def main():
    struct = {
        'num': 2,
        'list': [  # 顶层 list
            {"int": {"datarange": (0, 100)}},
            {"float": {"datarange": (0, 10.0)}}
        ],
        'tuple': {  # 顶层 tuple
            'str': {"datarange": string.ascii_uppercase, "len": 5},
            'list': [  # 嵌套 list
                {"int": {"datarange": (0, 10)}},
                {"float": {"datarange": (0, 1.0)}}
            ]
        },
        'dict': {  # 顶层 dict
            'nested_int': {"datarange": (1, 100)},
            'nested_str': {"datarange": string.ascii_lowercase, "len": 3}
        }
    }
    result = generate(**struct)
    for item in result:
        print(item)

main()