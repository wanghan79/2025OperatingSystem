import random
import string

# 递归


def structDataSampling(**kwargs):
    result = list()
    num = kwargs['num'] if 'num' in kwargs else 1
    for index in range(num):
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

print(structDataSampling(**struct))






# # 非递归  =>  栈实现

# def ranGenerate(**kwargs):
#     reslut = list()
#     num = kwargs.get('num', 1)
#     for index in range(num):
#         res = list()
#         stack = [(k, v) for k, v in kwargs.items() if k != 'num'] # 初始化栈
#         while stack:
#             key, value = stack.pop()
            
#             if key == 'dict':
#                 elem = dict()
#                 elem[random.randint(0,10)] = random.randint(10, 50)
#                 res.append(elem)
                
#             elif key == 'list':
#                 stack.extend([('list_item', v_item) for v_item in value.items()])
                
#             elif key == 'tuple':
#                 stack.extend([('tuple_item', v_item) for v_item in value.items()])
                
#             elif key == 'int':
#                 it = iter(value['datarange'])
#                 res.append(random.randint(next(it), next(it)))
                
#             elif key == 'float':
#                 it = iter(value['datarange'])
#                 res.append(random.uniform(next(it), next(it)))
                
#             elif key == 'str':
#                 datarange, length = value['datarange'], value['len']
#                 s = ''.join(random.choice(datarange) for _ in range(length))
#                 res.append(s)
            
#             elif key == 'list_item':
#                 stack.append((value[0], value[1]))
            
#             elif key == 'tuple_item':
#                 stack.append((value[0], value[1]))
                
#         reslut.append(res)
#     return reslut




# struct = {'num':3, 'tuple':{'str':{"datarange": string.ascii_uppercase, "len": 50}}, 'list':{'int':{"datarange": (0,10)}, 'float':{"datarange": (0, 1.0)}}, 'dict':{}}

# print(structDataSampling(**struct))