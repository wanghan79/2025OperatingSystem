import random
import string
import time

# 定义装饰器
def StatisticsRes(*statistics):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = list(func(*args, **kwargs))
            values = []
            # 遍历生成的结果，提取所有数值
            for res in results:
                def extract_values(data):
                    if isinstance(data, (int, float)):
                        values.append(data)
                    elif isinstance(data, dict):
                        for v in data.values():
                            extract_values(v)
                    elif isinstance(data, (list, tuple)):
                        for item in data:
                            extract_values(item)
                extract_values(res)

            stats = {}
            if 'SUM' in statistics:
                stats['SUM'] = sum(values)
            if 'AVG' in statistics:
                stats['AVG'] = sum(values) / len(values) if values else 0
            if 'MAX' in statistics:
                stats['MAX'] = max(values) if values else None
            if 'MIN' in statistics:
                stats['MIN'] = min(values) if values else None

            return stats
        return wrapper
    return decorator

def generate_random_value(datarange, length=None):
    try:
        if isinstance(datarange, tuple):
            if isinstance(datarange[0], int):
                return random.randint(*datarange)
            else:
                return random.uniform(*datarange)
        elif isinstance(datarange, str):
            length = length if length is not None else 1
            return ''.join(random.choice(datarange) for _ in range(length))
    except Exception as e:
        print(f"生成随机值时出错: {e}")
        return None

def generate(**kwargs):
    num = kwargs.get('num', 1)
    for _ in range(num):
        res = {}
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif isinstance(v, dict):
                if 'datarange' in v:
                    res[k] = generate_random_value(v['datarange'], v.get('len'))
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

# 使用装饰器修饰 generate 函数
@StatisticsRes('SUM', 'AVG', 'MAX', 'MIN')
def decorated_generate(**kwargs):
    return generate(**kwargs)

def main():
    struct = {
        'num': 10000,
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
    start_time = time.time()
    result = decorated_generate(**struct)
    end_time = time.time()
    print(f"统计结果: {result}")
    print(f"耗时 {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()
    