def banker_algorithm(Max, Need, Available, Allocated, Request, pid):
    """
    银行家算法实现

    参数:
        Max: 最大需求矩阵 (二维列表)
        Need: 需求矩阵 (二维列表)
        Available: 可用资源向量 (一维列表)
        Allocated: 已分配矩阵 (二维列表)
        Request: 请求资源向量 (一维列表)
        pid: 请求资源的进程ID (从0开始)

    返回:
        result: 分配结果字符串
        Max: 最大需求矩阵 (不变)
        Need: 更新后的需求矩阵
        Available: 更新后的可用资源向量
        Allocated: 更新后的已分配矩阵
    """
    n = len(Allocated)  # 进程数
    m = len(Available)  # 资源种类数

    # 步骤1: 检查Request是否小于等于Need[pid]
    for j in range(m):
        if Request[j] > Need[pid][j]:
            return ("分配失败：申请的资源超过需求", Max, Need, Available, Allocated)

    # 步骤2: 检查Request是否小于等于Available
    for j in range(m):
        if Request[j] > Available[j]:
            return ("分配失败：资源不足，请等待", Max, Need, Available, Allocated)

    # 步骤3: 尝试分配资源 (创建副本避免修改原数据)
    new_Available = Available[:]  # 可用资源副本
    new_Allocated = [row[:] for row in Allocated]  # 已分配矩阵副本
    new_Need = [row[:] for row in Need]  # 需求矩阵副本

    # 模拟分配资源
    for j in range(m):
        new_Available[j] -= Request[j]
        new_Allocated[pid][j] += Request[j]
        new_Need[pid][j] -= Request[j]

    # 步骤4: 安全性检查
    def is_safe(work, allocated, need):
        n_proc = len(allocated)
        finish = [False] * n_proc
        safe_sequence = []
        count = 0

        while count < n_proc:
            found = False
            for i in range(n_proc):
                if not finish[i]:
                    # 检查进程i的需求是否小于等于当前可用资源
                    if all(need[i][j] <= work[j] for j in range(m)):
                        # 执行进程i并释放资源
                        for j in range(m):
                            work[j] += allocated[i][j]
                        finish[i] = True
                        safe_sequence.append(i)
                        count += 1
                        found = True
                        break  # 重新扫描所有进程
            if not found:
                break  # 没有找到可执行的进程

        # 判断是否所有进程都完成
        if all(finish):
            return True, safe_sequence
        else:
            return False, safe_sequence

    # 进行安全性检查 (传入work的副本)
    safe, sequence = is_safe(new_Available[:], new_Allocated, new_Need)

    # 步骤5: 根据安全性检查结果决定是否分配
    if safe:
        return ("分配成功", Max, new_Need, new_Available, new_Allocated)
    else:
        return ("分配失败：系统将进入不安全状态", Max, Need, Available, Allocated)


# 测试示例
if __name__ == "__main__":
    # 示例数据 (经典银行家算法案例)
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

    # 计算初始Need矩阵 (Need = Max - Allocated)
    Need = [
        [Max[i][j] - Allocated[i][j] for j in range(3)]
        for i in range(5)
    ]

    Available = [3, 3, 2]  # 可用资源

    # 进程1 (pid=1) 请求资源 [1, 0, 2]
    Request = [1, 0, 2]
    pid = 1

    # 调用银行家算法
    result, Max_out, Need_out, Available_out, Allocated_out = banker_algorithm(
        Max, Need, Available, Allocated, Request, pid
    )

    # 打印结果
    print("分配结果:", result)
    print("\n最大需求矩阵(Max):")
    for row in Max_out:
        print(row)

    print("\n需求矩阵(Need):")
    for row in Need_out:
        print(row)

    print("\n可用资源向量(Available):", Available_out)
    print("\n已分配矩阵(Allocated):")
    for row in Allocated_out:
        print(row)
