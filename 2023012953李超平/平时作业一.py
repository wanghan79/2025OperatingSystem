"""
此为 Python 程序设计课平时作业一：银行家算法
在运行示例中给出了 Available，MAX，Allocation，以及 Request 和 对应请求进程的 pid 等参数。

作者：李超平
用途：Python 程序设计课平时作业一
"""

import copy

def isSafe(Available, Need, Allocation):
    """
    安全检测函数

    参数:
        Available: 当前可用资源向量
        Need: 每个进程尚需资源矩阵
        Allocation: 当前资源分配矩阵

    返回:
        bool: 系统是否处于安全状态
    """
    n, m = len(Need), len(Available)
    finished = [False] * n
    Work = Available[:]
    while True:
        found = False
        for i in range(len(Need)):
            if finished[i] is False and all(Need[i][j] <= Work[j] for j in range(m)):
                Work = [Work[j] + Allocation[i][j] for j in range(m)]
                finished[i] = True
                found = True
        if found is False:
            break
    return all(finished[i] for i in range(n))


def banker_algorithm(Max, Need, Available, Allocation, Request, pid):
    """
    银行家算法

    参数:
        Max: 每个进程的最大资源需求矩阵
        Need: 每个进程的剩余需求矩阵（Max - Allocation）
        Available: 当前可用资源向量
        Allocation: 当前资源分配矩阵
        Request: 某一进程的资源请求向量
        pid: 发出请求的进程编号

    返回:
        dict: 分配结果
    """
    n, m = len(Max), len(Available)
    if any(Request[j] > Need[pid][j] for j in range(m)):
        return {
            "state": False,
            "info": "资源请求超限"
        }
    if any(Request[j] > Available[j] for j in range(m)):
        return {
            "state": False,
            "info": "资源不足"
        }

    AvailableNew = [Available[j] - Request[j] for j in range(m)]
    AllocationNew = copy.deepcopy(Allocation)
    AllocationNew[pid] = [Allocation[pid][j] + Request[j] for j in range(m)]
    NeedNew = copy.deepcopy(Need)
    NeedNew[pid] = [Need[pid][j] - Request[j] for j in range(m)]
    if isSafe(AvailableNew, NeedNew, AllocationNew):
        return {
            "state": True,
            "info": {
                "Available": AvailableNew,
                "Allocation": AllocationNew,
                "Need": NeedNew,
                "Max": Max  # Max 不变
            }
        }
    else :
        return {
            "state": False,
            "info": "请求后系统不安全，拒绝分配"
        }

def main(Max, Need, Available, Allocation, Request, pid):
    res = banker_algorithm(Max, Need, Available, Allocation, Request, pid)
    state, result = res["state"], res["info"]

    if state:
        print("请求可以被安全满足")
        print("Available:", result["Available"])
        print("Allocation:")
        for row in result["Allocation"]:
            print(" ", row)
        print("Need:")
        for row in result["Need"]:
            print(" ", row)
    else:
        print("请求被拒绝：", result)


if __name__ == '__main__':
    # EXAMPLE 1
    Available = [3, 3, 2]

    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    Allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    Need = [[Max[i][j] - Allocation[i][j] for j in range(3)] for i in range(5)]

    Request = [1, 0, 2]  # 进程 P1 请求
    pid = 1  # 进程编号 1

    # 测试
    main(Max, Need, Available, Allocation, Request, pid)


"""
EXAMPLE 1
    Available = [3, 3, 2]

    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    Allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    Request = [1, 0, 2]  # 进程 P1 请求
    pid = 1  # 进程编号 1

    OUTPUT:
    请求可以被安全满足
    Available: [2, 3, 0]
    Allocation:
      [0, 1, 0]
      [3, 0, 2]
      [3, 0, 2]
      [2, 1, 1]
      [0, 0, 2]
    Need:
      [7, 4, 3]
      [0, 2, 0]
      [6, 0, 0]
      [0, 1, 1]
      [4, 3, 1]

EXAMPLE 2
    Available = [1, 0, 0]

    Max = [
        [2, 2, 2],  # P0
        [3, 2, 2],  # P1
        [2, 2, 2],  # P2
    ]

    Allocation = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 0, 1]
    ]

    Need = [[Max[i][j] - Allocation[i][j] for j in range(3)] for i in range(3)]

    Request = [1, 0, 0]  # P1 请求 1 单位 A
    pid = 1

    OUTPUT:
    请求被拒绝： 请求后系统不安全，拒绝分配
"""



