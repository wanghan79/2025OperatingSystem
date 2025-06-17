def banker_algorithm(Max, Allocated, Available, Request, process_num):
    """
    银行家算法实现

    参数:
        Max: 最大需求矩阵，n*m维，n个进程对m类资源的最大需求
        Allocated: 分配矩阵，n*m维，表示已分配给每个进程的资源
        Need: 需求矩阵，n*m维，表示每个进程还需要的资源
        Available: 可用资源向量，长度为m
        Request: 请求向量，长度为m，表示进程process_num请求的资源
        process_num: 发起请求的进程编号

    返回:
        (是否安全, 分配后的Max, 分配后的Allocated, 分配后的Need, 分配后的Available)
    """
    # 计算Need矩阵
    Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]

    # 检查请求是否小于等于Need
    for j in range(len(Request)):
        if Request[j] > Need[process_num][j]:
            return (False, "Error: Request exceeds need", Max, Allocated, Need, Available)

    # 检查请求是否小于等于Available
    for j in range(len(Request)):
        if Request[j] > Available[j]:
            return (False, "Error: Request exceeds available", Max, Allocated, Need, Available)

    # 尝试分配资源
    temp_available = Available.copy()
    temp_allocated = [row.copy() for row in Allocated]
    temp_need = [row.copy() for row in Need]

    for j in range(len(Request)):
        temp_available[j] -= Request[j]
        temp_allocated[process_num][j] += Request[j]
        temp_need[process_num][j] -= Request[j]

    # 检查系统是否处于安全状态
    work = temp_available.copy()
    finish = [False] * len(Max)
    safe_sequence = []

    while True:
        found = False
        for i in range(len(Max)):
            if not finish[i] and all(temp_need[i][j] <= work[j] for j in range(len(work))):
                # 找到可以执行的进程
                for j in range(len(work)):
                    work[j] += temp_allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break

        if not found:
            break

    if all(finish):
        # 安全，返回分配后的矩阵
        return (True, "Safe", Max, temp_allocated, temp_need, temp_available, safe_sequence)
    else:
        # 不安全，返回原始矩阵
        return (False, "Unsafe: No safe sequence", Max, Allocated, Need, Available, [])


def print_matrices(Max, Allocated, Need, Available):
    """打印各个矩阵"""
    print("\nMax Matrix:")
    for row in Max:
        print(row)

    print("\nAllocated Matrix:")
    for row in Allocated:
        print(row)

    print("\nNeed Matrix:")
    for row in Need:
        print(row)

    print("\nAvailable Resources:")
    print(Available)


def test_banker_algorithm():
    # 测试用例
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    Allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    Available = [3, 3, 2]

    # 进程1请求资源 (1, 0, 2)
    Request = [1, 0, 2]
    process_num = 1

    print("Initial state:")
    Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]
    print_matrices(Max, Allocated, Need, Available)

    print(f"\nProcess {process_num} requests: {Request}")
    result = banker_algorithm(Max, Allocated, Available, Request, process_num)

    if result[0]:
        print("\nRequest granted. System is safe.")
        print("Safe sequence:", result[6])
        print("\nUpdated state:")
        print_matrices(result[2], result[3], result[4], result[5])
    else:
        print("\nRequest denied. Reason:", result[1])
        print("\nState remains unchanged:")
        print_matrices(result[2], result[3], result[4], result[5])


if __name__ == "__main__":
    test_banker_algorithm()