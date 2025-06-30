def banker_algorithm(Max, Need, Available, Allocated, Request, process_num):
    # 1. 检查请求是否小于等于需求
    for i in range(len(Request)):
        if Request[i] > Need[process_num][i]:
            return (False, [], Max, Need, Available, Allocated, "错误：请求超过声明的需求")

    # 2. 检查请求是否小于等于可用资源
    for i in range(len(Request)):
        if Request[i] > Available[i]:
            return (False, [], Max, Need, Available, Allocated, "错误：资源不足，请等待")

    # 3. 尝试分配资源
    old_Available = Available.copy()
    old_Allocated = [row.copy() for row in Allocated]
    old_Need = [row.copy() for row in Need]

    # 更新状态
    for i in range(len(Request)):
        Available[i] -= Request[i]
        Allocated[process_num][i] += Request[i]
        Need[process_num][i] -= Request[i]

    # 4. 检查安全性
    Work = Available.copy()
    Finish = [False] * len(Max)
    safe_sequence = []

    # 寻找可以完成的进程
    while True:
        found = False
        for i in range(len(Max)):
            if not Finish[i]:
                # 检查该进程的需求是否小于等于可用资源
                can_execute = True
                for j in range(len(Work)):
                    if Need[i][j] > Work[j]:
                        can_execute = False
                        break

                if can_execute:
                    # 执行该进程并释放资源
                    for j in range(len(Work)):
                        Work[j] += Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True

        if not found:
            break

    # 检查是否所有进程都完成
    is_safe = all(Finish)

    if is_safe:
        return (True, safe_sequence, Max, Need, Available, Allocated, "安全，可以分配")
    else:
        # 恢复原始状态
        return (False, [], Max, old_Need, old_Available, old_Allocated, "不安全，拒绝分配")


# 示例使用
if __name__ == "__main__":
    # 示例数据
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

    # 计算Need矩阵
    Need = []
    for i in range(len(Max)):
        Need.append([Max[i][j] - Allocated[i][j] for j in range(len(Max[i]))])

    Available = [3, 3, 2]

    # 进程1请求资源 (1, 0, 2)
    Request = [1, 0, 2]
    process_num = 1

    # 运行银行家算法
    result = banker_algorithm(Max, Need, Available, Allocated, Request, process_num)

    # 输出结果
    is_safe, sequence, new_Max, new_Need, new_Available, new_Allocated, message = result

    print(f"分配结果: {message}")
    print(f"安全序列: {sequence if is_safe else '无'}")
    print("\n分配后状态:")
    print("Max矩阵:")
    for row in new_Max:
        print(row)

    print("\nNeed矩阵:")
    for row in new_Need:
        print(row)

    print("\nAvailable向量:", new_Available)

    print("\nAllocated矩阵:")
    for row in new_Allocated:
        print(row)
