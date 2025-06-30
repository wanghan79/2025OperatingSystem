def calculate_need(Max, Allocation):
    """计算每个进程的需求矩阵"""
    Need = []
    for i in range(len(Max)):
        need = [Max[i][j] - Allocation[i][j] for j in range(len(Max[i]))]
        Need.append(need)
    return Need

def print_state(processes, resources, Max, Need, Allocation, Available):
    """打印系统当前状态"""
    print("\n系统状态:")
    print(f"可用资源: {Available} ({', '.join(resources)})")
    
    print("\n进程\tMax\t\tAllocation\tNeed")
    for i in processes:
        print(f"P{i}\t{Max[i]}\t\t{Allocation[i]}\t\t{Need[i]}")
    print()

def banker_algorithm(processes, resources, Max, Allocation, Available, Request, process_id):
    """银行家算法实现"""
    # 获取请求进程的索引
    p_idx = process_id
    
    # 检查请求是否超过需求
    for j in range(len(resources)):
        if Request[j] > Max[p_idx][j]:
            print(f"错误: 进程P{process_id}的请求超过了其最大需求")
            return False, Max, Allocation, Available
    
    need = calculate_need(Max, Allocation)
    
    # 检查请求是否超过当前需求
    for j in range(len(resources)):
        if Request[j] > need[p_idx][j]:
            print(f"错误: 进程P{process_id}的请求超过了其当前需求")
            return False, Max, Allocation, Available
    
    # 检查可用资源是否足够
    for j in range(len(resources)):
        if Request[j] > Available[j]:
            print(f"错误: 可用资源不足，无法满足进程P{process_id}的请求")
            return False, Max, Allocation, Available
    
    # 预分配资源
    new_Available = [Available[j] - Request[j] for j in range(len(resources))]
    new_Allocation = [row[:] for row in Allocation]  # 复制矩阵
    new_Allocation[p_idx] = [new_Allocation[p_idx][j] + Request[j] for j in range(len(resources))]
    
    new_Need = calculate_need(Max, new_Allocation)
    
    # 安全性检查
    if is_safe_state(processes, resources, Max, new_Allocation, new_Available):
        print(f"资源分配成功，进程P{process_id}的请求被批准")
        return True, Max, new_Allocation, new_Available
    else:
        print(f"资源分配失败，进程P{process_id}的请求会导致系统进入不安全状态")
        return False, Max, Allocation, Available

def is_safe_state(processes, resources, Max, Allocation, Available):
    """检查系统是否处于安全状态"""
    Need = calculate_need(Max, Allocation)
    work = Available.copy()
    finish = [False] * len(processes)
    safe_sequence = []
    
    while True:
        found = False
        for i in processes:
            if not finish[i] and all(Need[i][j] <= work[j] for j in range(len(resources))):
                # 分配资源并回收
                for j in range(len(resources)):
                    work[j] += Allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        
        if not found:
            break
    
    if all(finish):
        safe_seq_str = " -> ".join([f"P{p}" for p in safe_sequence])
        print(f"安全状态，安全序列: {safe_seq_str}")
        return True
    else:
        print("不安全状态")
        return False

# 主程序
if __name__ == "__main__":
    # 定义进程和资源
    processes = [0, 1, 2, 3, 4]
    resources = ['A', 'B', 'C']

    # 初始矩阵定义
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
    Need = calculate_need(Max, Allocation)

    # 打印初始状态
    print("初始状态:")
    print_state(processes, resources, Max, Need, Allocation, Available)

    # 进程1请求资源 [1, 0, 2]
    Request = [1, 0, 2]
    process_id = 1
    print(f"进程P{process_id}请求资源: {Request}")

    success, Max, Allocation, Available = banker_algorithm(
        processes, resources, Max, Allocation, Available, Request, process_id
    )

    Need = calculate_need(Max, Allocation)  # 更新Need矩阵
    print_state(processes, resources, Max, Need, Allocation, Available)

    # 进程4请求资源 [3, 3, 0]
    Request = [3, 3, 0]
    process_id = 4
    print(f"进程P{process_id}请求资源: {Request}")

    success, Max, Allocation, Available = banker_algorithm(
        processes, resources, Max, Allocation, Available, Request, process_id
    )

    Need = calculate_need(Max, Allocation)  # 更新Need矩阵
    print_state(processes, resources, Max, Need, Allocation, Available)