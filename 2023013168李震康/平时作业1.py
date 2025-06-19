def banker_algorithm(Max, Need, Available, Allocated, Request, process_id):
    """
    银行家算法实现

    参数:
    Max (list of list): 每个进程的最大需求矩阵
    Need (list of list): 每个进程的剩余需求矩阵
    Available (list): 可用资源向量
    Allocated (list of list): 已分配资源矩阵
    Request (list): 进程的请求资源向量
    process_id (int): 请求资源的进程ID

    返回:
    tuple: (是否安全, 更新后的Available, 更新后的Allocated, 更新后的Need, Max)
    """
    # 步骤1：检查请求是否超过声明需求
    for i in range(len(Request)):
        if Request[i] > Need[process_id][i]:
            print("错误：请求超过进程声明需求")
            return False, Available.copy(), [row.copy() for row in Allocated], [row.copy() for row in Need], Max

    # 步骤2：检查系统是否有足够可用资源
    for i in range(len(Request)):
        if Request[i] > Available[i]:
            print("系统资源不足，进程需要等待")
            return False, Available.copy(), [row.copy() for row in Allocated], [row.copy() for row in Need], Max

    # 创建临时副本进行模拟分配
    temp_available = Available.copy()
    temp_allocated = [row.copy() for row in Allocated]
    temp_need = [row.copy() for row in Need]

    # 步骤3：尝试资源分配
    for i in range(len(Request)):
        temp_available[i] -= Request[i]
        temp_allocated[process_id][i] += Request[i]
        temp_need[process_id][i] -= Request[i]

    # 步骤4：安全性检查
    num_processes = len(Max)
    work = temp_available.copy()
    finish = [False] * num_processes
    safe_sequence = []

    for _ in range(num_processes):
        found = False
        for i in range(num_processes):
            if not finish[i] and all(temp_need[i][j] <= work[j] for j in range(len(work))):
                # 释放资源
                for j in range(len(work)):
                    work[j] += temp_allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            break

    if all(finish):
        print("安全序列:", safe_sequence)
        return True, temp_available, temp_allocated, temp_need, Max
    else:
        print("系统不安全，拒绝分配")
        return False, Available.copy(), [row.copy() for row in Allocated], [row.copy() for row in Need], Max


# 示例用法
if __name__ == "__main__":
    # 示例数据（来自操作系统经典案例）
    Max = [
        [7, 5, 3, 3],
        [3, 2, 2, 9],
        [9, 0, 2, 2],
        [2, 2, 2, 4],
        [4, 3, 3, 5]
    ]

    Allocated = [
        [0, 1, 0, 0],
        [2, 0, 0, 3],
        [3, 0, 2, 1],
        [2, 1, 1, 0],
        [0, 0, 2, 2]
    ]

    Need = [
        [7 - 0, 5 - 1, 3 - 0, 3 - 0],
        [3 - 2, 2 - 0, 2 - 0, 9 - 3],
        [9 - 3, 0 - 0, 2 - 2, 2 - 1],
        [2 - 2, 2 - 1, 2 - 1, 4 - 0],
        [4 - 0, 3 - 0, 3 - 2, 5 - 2]
    ]

    Available = [3, 3, 2, 1]

    # 测试进程1请求[1,0,2,1]
    Request = [1, 0, 2, 1]
    process_id = 1

    safe, new_avail, new_alloc, new_need, new_max = banker_algorithm(
        Max, Need, Available, Allocated, Request, process_id
    )

    print("\n分配结果:", "安全" if safe else "不安全")
    print("更新后的Available:", new_avail)
    print("更新后的Allocated:")
    for p in new_alloc:
        print(p)
    print("更新后的Need:")
    for p in new_need:
        print(p)