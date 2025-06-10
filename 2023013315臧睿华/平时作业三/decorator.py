import random
import string

# 递归提取所有 int 和 float 类型的值
def extract_numbers(data):
    numbers = []
    
    def recursive_extract(item):
        if isinstance(item, (int, float)):
            numbers.append(item)
            
        elif isinstance(item, (list, tuple)):
            for subitem in item:
                recursive_extract(subitem)
                
        elif isinstance(item, dict):
            for key, value in item.items():
                recursive_extract(key)
                recursive_extract(value)
            
    recursive_extract(data)
    return numbers

# 参数化装饰器 - 用于处理统计数据
def StaticRes(enable=True):
    def decorator(func):
        def wrapper(*wargs, **kwargs):
            result = func(*wargs, **kwargs)

            if not enable:
                return result

            # 统计每个样本中的int和float数据
            stat_result = {
                'SUM': 0,
                'AVG': 0,
                'MAX': float('-inf'),
                'MIN': float('inf'),
                'COUNT': 0
            }

            # all_numbers = []
            # for sample in result:
            #     for item in sample:
            #         if isinstance(item, (int, float)):
            #             all_numbers.append(item)

            all_numbers = extract_numbers(result)
            
            if all_numbers:
                stat_result['SUM'] = sum(all_numbers)
                stat_result['AVG'] = stat_result['SUM'] / len(all_numbers)
                stat_result['MAX'] = max(all_numbers)
                stat_result['MIN'] = min(all_numbers)
                stat_result['COUNT'] = len(all_numbers)

            return stat_result
        return wrapper
    return decorator


# 数据生成函数
@StaticRes(enable=False)  # 默认不启用统计
def structDataSampling(**kwargs):
    result = list()
    num = kwargs.get('num', 1)

    for _ in range(num):
        res = list()

        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k == 'dict':
                elem = dict()
                elem[random.randint(0,10)] = random.randint(10, 50)
                res.append(elem)
            elif k == 'list':
                res.append(structDataSampling(**v))
            elif k == 'tuple':
                res.append(
                    tuple(structDataSampling(**v))
                )
            elif k == 'int':
                it = iter(v['datarange'])
                res.append(random.randint(next(it), next(it)))
            elif k == 'float':
                it = iter(v['datarange'])
                res.append(random.uniform(next(it), next(it)))
            elif k == 'str':
                datarange, length = v['datarange'], v['len']
                s = ''.join(random.choice(datarange) for _ in range(length))
                res.append(s)
            else:
                continue

        result.append(res)

    return result



struct = {'num':3, 'tuple':{'str':{"datarange": string.ascii_uppercase, "len": 50}}, 'list':{'int':{"datarange": (0,10)}, 'float':{"datarange": (0, 1.0)}}, 'dict':{}}

# 执行调用（被装饰后，通过设置enable参数控制是否返回统计结果）
output = structDataSampling(**struct)
print("原始数据：")
for idx, d in enumerate(output, 1):
    print(f"样本 {idx}: {d}")

# 启用统计
decorated_func = StaticRes(enable=True)(structDataSampling)
statistics = decorated_func(**struct)
print("\n统计结果：")
print(statistics)