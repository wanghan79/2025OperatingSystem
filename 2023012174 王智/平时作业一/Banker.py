def banker_algorithm(Max, Allocation, Need, Available, Request, process_index):
    """
    使用银行家算法判断是否可以满足某进程的资源请求，并输出分配结果

    :param Max: 每个进程对资源的最大需求矩阵
    :param Allocation: 当前每个进程已分配资源矩阵
    :param Need: 当前每个进程还需要的资源矩阵
    :param Available: 系统当前可用资源向量
    :param Request: 进程请求资源向量
    :param process_index: 请求资源的进程索引
    :return: 一个元组，包含是否可以分配的布尔值和分配后的四个矩阵
    """
    # 检查请求是否合法
    if any(Request[i] > Need[process_index][i] for i in range(len(Request))):
        print(f"进程 {process_index} 的请求超过其最大需求，请求不合法")
        return False, Max, Allocation, Need, Available

    # 检查系统是否有足够的资源来满足请求
    if any(Request[i] > Available[i] for i in range(len(Request))):
        print(f"系统当前可用资源不足以满足进程 {process_index} 的请求")
        return False, Max, Allocation, Need, Available

    # 创建临时副本用于模拟分配
    temp_available = Available.copy()
    temp_allocation = [row.copy() for row in Allocation]
    temp_need = [row.copy() for row in Need]

    # 模拟分配资源
    for i in range(len(Request)):
        temp_available[i] -= Request[i]
        temp_allocation[process_index][i] += Request[i]
        temp_need[process_index][i] -= Request[i]

    # 安全检查算法
    n = len(Max)  # 进程数
    m = len(Request)  # 资源种类数
    Work = temp_available.copy()
    Finish = [False] * n

    while True:
        # 查找一个尚未完成且其需求小于等于Work的进程
        found = False
        for i in range(n):
            if not Finish[i] and all(temp_need[i][j] <= Work[j] for j in range(m)):
                # 找到这样的进程，将其资源回收到可用资源中
                for j in range(m):
                    Work[j] += temp_allocation[i][j]
                Finish[i] = True
                found = True

        if not found:
            break

    # 判断是否所有进程都能完成
    if all(Finish):
        print(f"可以安全地将资源分配给进程 {process_index}")
        # 更新实际的Available、Allocation和Need矩阵
        Available[:] = temp_available
        Allocation[process_index] = temp_allocation[process_index]
        Need[process_index] = temp_need[process_index]
        return True, Max, Allocation, Need, Available
    else:
        print(f"无法安全地将资源分配给进程 {process_index}")
        return False, Max, Allocation, Need, Available



if __name__ == "__main__":
    # 定义示例数据
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

    Need = [
        [7 - 0, 5 - 1, 3 - 0],
        [3 - 2, 2 - 0, 2 - 0],
        [9 - 3, 0 - 0, 2 - 2],
        [2 - 2, 2 - 1, 2 - 1],
        [4 - 0, 3 - 0, 3 - 2]
    ]

    Available = [10, 5, 7]

    Request = [1, 0, 2]
    process_index = 1  # 进程 P1

    # 调用银行家算法函数
    success, Max, Allocation, Need, Available = banker_algorithm(
        Max, Allocation, Need, Available, Request, process_index)

    # 输出结果
    if success:
        print("分配后的 Available 矩阵:", Available)
        print("分配后的 Allocation 矩阵:")
        for row in Allocation:
            print(row)
        print("分配后的 Need 矩阵:")
        for row in Need:
            print(row)
