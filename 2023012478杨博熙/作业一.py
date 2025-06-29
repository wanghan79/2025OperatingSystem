def bankers_algorithm(Max, Need, Available, Allocation, request, requesting_process):
    """
    银行家算法实现

    参数:
    Max - 最大需求矩阵，每个进程对每种资源的最大需求
    Need - 需求矩阵，每个进程还需要的各种资源数
    Available - 可用资源向量，系统中可用的各种资源数
    Allocation - 分配矩阵，每个进程已分配的各种资源数
    request - 资源申请向量，进程请求的各种资源数
    requesting_process - 请求资源的进程号

    返回:
    (是否可分配, 新的Need, 新的Available, 新的Allocation, 消息)
    """
    n_processes = len(Max)
    n_resources = len(Max[0])

    # 检查请求是否超过Need
    for i in range(n_resources):
        if request[i] > Need[requesting_process][i]:
            return False, Need, Available, Allocation, "请求超过了声明的最大需求"

    # 检查请求是否超过Available
    for i in range(n_resources):
        if request[i] > Available[i]:
            return False, Need, Available, Allocation, "请求超过了可用资源"

    # 创建临时矩阵进行模拟分配
    temp_need = [row[:] for row in Need]
    temp_available = Available[:]
    temp_allocation = [row[:] for row in Allocation]

    # 假设分配资源
    for i in range(n_resources):
        temp_need[requesting_process][i] -= request[i]
        temp_available[i] -= request[i]
        temp_allocation[requesting_process][i] += request[i]

    # 安全性检查
    work = temp_available[:]
    finish = [False] * n_processes

    # 找到一个满足条件的进程
    while True:
        found = False
        for i in range(n_processes):
            if not finish[i]:
                safe = True
                for j in range(n_resources):
                    if temp_need[i][j] > work[j]:
                        safe = False
                        break

                if safe:
                    # 可以完成进程i
                    for j in range(n_resources):
                        work[j] += temp_allocation[i][j]
                    finish[i] = True
                    found = True

        if not found:
            break

    # 如果所有进程都能完成，则系统处于安全状态
    if all(finish):
        return True, temp_need, temp_available, temp_allocation, "资源分配成功"
    else:
        return False, Need, Available, Allocation, "分配会导致不安全状态"


# 示例使用
if __name__ == "__main__":
    # 示例数据
    Max = [
        [7, 5, 3],  # 进程0最大需求
        [3, 2, 2],  # 进程1最大需求
        [9, 0, 2],  # 进程2最大需求
        [2, 2, 2],  # 进程3最大需求
        [4, 3, 3]  # 进程4最大需求
    ]

    Allocation = [
        [0, 1, 0],  # 进程0已分配
        [2, 0, 0],  # 进程1已分配
        [3, 0, 2],  # 进程2已分配
        [2, 1, 1],  # 进程3已分配
        [0, 0, 2]  # 进程4已分配
    ]

    Available = [3, 3, 2]  # 可用资源

    # 计算Need矩阵
    Need = []
    for i in range(len(Max)):
        need_row = []
        for j in range(len(Max[0])):
            need_row.append(Max[i][j] - Allocation[i][j])
        Need.append(need_row)

    # 进程1请求资源 [1, 0, 2]
    request = [1, 0, 2]
    requesting_process = 1

    # 执行银行家算法
    safe, new_need, new_available, new_allocation, message = bankers_algorithm(
        Max, Need, Available, Allocation, request, requesting_process
    )

    print(f"是否安全分配: {safe}")
    print(f"消息: {message}")

    if safe:
        print("\n分配后的Need矩阵:")
        for row in new_need:
            print(row)

        print("\n分配后的Available向量:")
        print(new_available)

        print("\n分配后的Allocation矩阵:")
        for row in new_allocation:
            print(row)
