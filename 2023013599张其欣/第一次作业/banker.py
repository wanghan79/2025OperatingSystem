def is_safe(allocation, max_need, available, n_processes, n_resources):
    """
    检查系统是否处于安全状态。
    
    参数:
        allocation (list): 当前资源分配矩阵
        max_need (list): 进程最大资源需求矩阵
        available (list): 可用资源向量
        n_processes (int): 进程数量
        n_resources (int): 资源种类数量
    
    返回:
        tuple: (是否安全, 安全序列)
    """
    work = available.copy()
    finish = [False] * n_processes
    safe_sequence = []

    while len(safe_sequence) < n_processes:
        found = False
        for i in range(n_processes):
            if not finish[i]:
                # 检查该进程是否可以被满足
                if all(max_need[i][j] - allocation[i][j] <= work[j] for j in range(n_resources)):
                    # 假设该进程完成，释放资源
                    for j in range(n_resources):
                        work[j] += allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
        if not found:
            return (False, [])
    return (True, safe_sequence)


def banker_algorithm(allocation, max_need, available, n_processes, n_resources, request, process_id):
    """
    银行家算法核心实现。
    
    参数:
        allocation (list): 当前资源分配矩阵
        max_need (list): 进程最大资源需求矩阵
        available (list): 可用资源向量
        n_processes (int): 进程数量
        n_resources (int): 资源种类数量
        request (list): 进程请求的资源向量
        process_id (int): 请求资源的进程ID
    
    返回:
        tuple: (是否允许分配, 新的资源分配状态)
    """
    # 检查请求是否超过该进程的最大需求
    for j in range(n_resources):
        if request[j] > max_need[process_id][j] - allocation[process_id][j]:
            print(f"进程 {process_id} 请求超出其最大需求！")
            return (False, None)

    # 检查系统是否有足够的资源
    for j in range(n_resources):
        if request[j] > available[j]:
            print(f"系统没有足够的资源 {j} 满足请求！")
            return (False, None)

    # 假设分配资源
    for j in range(n_resources):
        allocation[process_id][j] += request[j]
        available[j] -= request[j]

    # 检查系统是否仍处于安全状态
    is_safe_state, safe_seq = is_safe(allocation, max_need, available, n_processes, n_resources)
    if is_safe_state:
        print(f"资源分配成功！安全序列为: {safe_seq}")
        return (True, (allocation, available))
    else:
        # 回滚
        print("资源分配后系统不安全，回滚！")
        for j in range(n_resources):
            allocation[process_id][j] -= request[j]
            available[j] += request[j]
        return (False, None)


def main():
    """
    主函数，初始化资源并调用银行家算法。
    """
    # 初始化数据
    n_processes = 5
    n_resources = 3
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    max_need = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    available = [3, 3, 2]
    request = [0, 1, 0]
    process_id = 1

    print("初始资源分配状态:")
    for i in range(n_processes):
        print(f"进程 {i}: 分配 = {allocation[i]}, 最大需求 = {max_need[i]}")
    print(f"可用资源: {available}")

    # 调用银行家算法
    success, new_state = banker_algorithm(allocation, max_need, available, n_processes, n_resources, request, process_id)

    if success:
        new_allocation, new_available = new_state
        print("\n资源分配后的新状态:")
        for i in range(n_processes):
            print(f"进程 {i}: 分配 = {new_allocation[i]}")
        print(f"可用资源: {new_available}")
    else:
        print("\n资源分配失败，系统仍保持原状态。")


if __name__ == "__main__":
    main()