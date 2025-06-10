def bankers_algorithm(Max, Allocation, Available, Request, process_num=None):
    """
    银行家算法实现

    参数:
        Max: 最大需求矩阵 (n x m), n=进程数, m=资源类型数
        Allocation: 已分配矩阵 (n x m)
        Available: 可用资源向量 (m,)
        Request: 请求资源向量 (m,), 如果不指定process_num则必须指定
        process_num: 发起请求的进程编号 (从0开始)

    返回:
        (是否安全, 安全序列, 新的Allocation, 新的Need, 新的Available)
    """
    # 如果Request和process_num都提供了，检查Request是否合法
    if process_num is not None:
        # 计算Need矩阵
        Need = [[Max[i][j] - Allocation[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]

        # 步骤1: 检查Request <= Need[process_num]
        if not all(Request[j] <= Need[process_num][j] for j in range(len(Request))):
            return (False, None, Allocation, Need, Available, "Error: Request exceeds maximum claim.")

        # 步骤2: 检查Request <= Available
        if not all(Request[j] <= Available[j] for j in range(len(Request))):
            return (False, None, Allocation, Need, Available, "Error: Request exceeds available resources.")

    # 假设请求被满足，尝试分配
    if process_num is not None:
        # 临时修改分配状态
        new_Allocation = [row[:] for row in Allocation]
        new_Available = Available[:]
        new_Need = [row[:] for row in Need]

        for j in range(len(Request)):
            new_Allocation[process_num][j] += Request[j]
            new_Available[j] -= Request[j]
            new_Need[process_num][j] -= Request[j]
    else:
        new_Allocation = Allocation
        new_Available = Available
        new_Need = [[Max[i][j] - new_Allocation[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]

    # 安全检查算法
    work = new_Available[:]
    finish = [False] * len(new_Allocation)
    safe_sequence = []

    while True:
        # 找到一个满足finish[i]=False且Need[i] <= work的进程
        found = False
        for i in range(len(new_Allocation)):
            if not finish[i] and all(new_Need[i][j] <= work[j] for j in range(len(work))):
                # 执行并释放资源
                for j in range(len(work)):
                    work[j] += new_Allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break

        if not found:
            break

    # 检查是否所有进程都完成了
    if all(finish):
        if process_num is not None:
            return (True, safe_sequence, new_Allocation, new_Need, new_Available, "Request granted.")
        else:
            return (True, safe_sequence, new_Allocation, new_Need, new_Available, "System is in safe state.")
    else:
        if process_num is not None:
            return (False, None, Allocation, Need, Available, "Request denied: would lead to unsafe state.")
        else:
            return (False, None, Allocation, Need, Available, "System is in unsafe state.")


def print_state(Allocation, Need, Available, Max=None):
    """打印当前系统状态"""
    print("\n当前系统状态:")
    if Max is not None:
        print("Max矩阵:")
        for row in Max:
            print(row)

    print("\nAllocation矩阵:")
    for row in Allocation:
        print(row)

    print("\nNeed矩阵:")
    for row in Need:
        print(row)

    print("\nAvailable向量:")
    print(Available)


if __name__ == "__main__":
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

    Available = [3, 3, 2]

    # 计算初始Need矩阵
    Need = [[Max[i][j] - Allocation[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]

    # 打印初始状态
    print("初始状态:")
    print_state(Allocation, Need, Available, Max)

    print("\n示例1: 进程1请求(1,0,2)")
    process_num = 1
    Request = [1, 0, 2]

    result, seq, new_Alloc, new_Need, new_Avail, msg = bankers_algorithm(Max, Allocation, Available, Request,
                                                                         process_num)
    print("\n结果:", msg)
    if result:
        print("安全序列:", seq)
        print_state(new_Alloc, new_Need, new_Avail)

    print("\n示例2: 进程0请求(0,2,0)")
    process_num = 0
    Request = [0, 2, 0]

    result, seq, new_Alloc, new_Need, new_Avail, msg = bankers_algorithm(Max, Allocation, Available, Request,
                                                                         process_num)
    print("\n结果:", msg)
    if result:
        print("安全序列:", seq)
        print_state(new_Alloc, new_Need, new_Avail)
    else:
        print("分配未执行，系统状态保持不变")
        print_state(Allocation, Need, Available)