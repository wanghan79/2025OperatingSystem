def banker_algorithm(processes, resources, Max, Allocated, Available, Request=None):
    """
    银行家算法实现
    :param processes: 进程数量
    :param resources: 资源种类数量
    :param Max: 最大需求矩阵 (processes x resources)
    :param Allocated: 已分配矩阵 (processes x resources)
    :param Available: 可用资源向量 (1 x resources)
    :param Request: 请求资源 (process_index, [r1, r2,...])
    :return: 分配结果和更新后的矩阵
    """

    # 计算需求矩阵Need
    Need = [[Max[i][j] - Allocated[i][j] for j in range(resources)] for i in range(processes)]

    # 如果有资源请求
    if Request:
        process_idx, req_vector = Request

        # 检查请求是否超过需求
        if any(req_vector[j] > Need[process_idx][j] for j in range(resources)):
            return False, "Error: Request exceeds maximum need", Max, Need, Allocated, Available

        # 检查请求是否超过可用资源
        if any(req_vector[j] > Available[j] for j in range(resources)):
            return False, "Error: Not enough resources available", Max, Need, Allocated, Available

        # 尝试分配资源
        new_Allocated = [row[:] for row in Allocated]
        new_Need = [row[:] for row in Need]
        new_Available = Available[:]

        for j in range(resources):
            new_Allocated[process_idx][j] += req_vector[j]
            new_Need[process_idx][j] -= req_vector[j]
            new_Available[j] -= req_vector[j]

        # 检查安全性
        safe, sequence = is_safe(processes, resources, new_Allocated, new_Need, new_Available)

        if safe:
            return True, f"Request granted. Safe sequence: {sequence}", Max, new_Need, new_Allocated, new_Available
        else:
            return False, "Request denied: would lead to unsafe state", Max, Need, Allocated, Available
    else:
        # 无请求时只检查系统当前状态
        safe, sequence = is_safe(processes, resources, Allocated, Need, Available)
        if safe:
            return True, f"System is safe. Safe sequence: {sequence}", Max, Need, Allocated, Available
        else:
            return False, "System is not safe", Max, Need, Allocated, Available


def is_safe(processes, resources, Allocated, Need, Available):
    """检查系统是否处于安全状态"""
    work = Available[:]
    finish = [False] * processes
    safe_sequence = []

    while True:
        # 查找满足条件的进程
        found = False
        for i in range(processes):
            if not finish[i] and all(Need[i][j] <= work[j] for j in range(resources)):
                # 模拟分配资源
                for j in range(resources):
                    work[j] += Allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break

        if not found:
            break

    # 检查是否所有进程都能完成
    if all(finish):
        return True, safe_sequence
    else:
        return False, []


# 示例使用
if __name__ == "__main__":
    # 示例数据
    processes = 5
    resources = 3

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

    # 测试1: 无请求，只检查系统状态
    print("=== 测试1: 检查初始系统状态 ===")
    result, message, new_Max, new_Need, new_Allocated, new_Available = banker_algorithm(
        processes, resources, Max, Allocated, Available)
    print(message)
    print("Need矩阵:")
    for row in new_Need:
        print(row)

    # 测试2: 合法请求
    print("\n=== 测试2: 合法请求 ===")
    Request = (1, [1, 0, 2])  # 进程1请求[1,0,2]
    result, message, new_Max, new_Need, new_Allocated, new_Available = banker_algorithm(
        processes, resources, Max, Allocated, Available, Request)
    print(message)
    print("分配后的Allocated矩阵:")
    for row in new_Allocated:
        print(row)
    print("分配后的Available向量:", new_Available)

    # 测试3: 非法请求(超过可用资源)
    print("\n=== 测试3: 非法请求 ===")
    Request = (0, [7, 5, 3])  # 进程0请求全部资源
    result, message, _, _, _, _ = banker_algorithm(
        processes, resources, Max, Allocated, Available, Request)
    print(message)
