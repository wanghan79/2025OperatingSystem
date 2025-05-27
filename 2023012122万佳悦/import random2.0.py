import random
import string
import time


def generate(**kwargs):
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
                    res[k] = next(generate(**v))
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
        yield res


def main():
    struct = {
        'num': 100000000,
        'list': [
            {"int": {"datarange": (0, 100)}},
            {"float": {"datarange": (0, 10.0)}}
        ],
        'tuple': {
            'str': {"datarange": string.ascii_uppercase, "len": 5},
            'list': [
                {"int": {"datarange": (0, 10)}},
                {"float": {"datarange": (0, 1.0)}}
            ]
        },
        'dict': {
            'nested_int': {"datarange": (1, 100)},
            'nested_str': {"datarange": string.ascii_lowercase, "len": 3}
        }
    }
    count = 0
    start_time = time.time()
    for _ in generate(**struct):
        count += 1
    end_time = time.time()
    print(f"成功生成 {count} 个样本，耗时 {end_time - start_time:.2f} 秒")
    if count == struct.get('num', 1):
        print("生成数量与预期一致")
    else:
        print("生成数量与预期不一致")


if __name__ == "__main__":
    main()
    
