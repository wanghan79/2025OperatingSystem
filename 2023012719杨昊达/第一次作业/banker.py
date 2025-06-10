import copy


def safety_check(available, max_demand, allocation):
    """
    安全检测算法 - 检查系统是否处于安全状态

    参数:
        available: 当前可用资源向量(列表)
        max_demand: 进程最大需求矩阵(二维列表)
        allocation: 资源分配矩阵(二维列表)

    返回:
        (is_safe, safe_sequence):
            is_safe - 布尔值，系统是否安全
            safe_sequence - 安全序列列表(如果有)
    """

    # 计算当前的需求矩阵(最大需求 - 已分配)
    need = []
    for i in range(len(allocation)):
        process_need = [max_demand[i][j] - allocation[i][j] for j in range(len(available))]
        need.append(process_need)

    # 工作向量，初始化为可用资源向量
    work = available.copy()

    # 完成状态标记，初始所有进程都未完成
    finish = [False] * len(allocation)

    # 安全序列，用于存储可能的执行顺序
    safe_sequence = []

    # 安全检测过程
    found = True
    while found:
        found = False
        for i in range(len(allocation)):
            # 检查进程是否已完成
            if not finish[i]:
                # 检查当前进程的资源需求是否小于等于工作向量
                can_run = True
                for j in range(len(available)):
                    if need[i][j] > work[j]:
                        can_run = False
                        break

                # 如果需求满足，则可以执行该进程
                if can_run:
                    # 执行完进程后释放资源
                    for j in range(len(available)):
                        work[j] += allocation[i][j]
                    # 标记进程为已完成
                    finish[i] = True
                    # 添加到安全序列
                    safe_sequence.append(i)
                    found = True

    # 检查所有进程是否都已完成
    is_safe = all(finish)
    return (is_safe, safe_sequence)


def request_resources(process_id, request, available, max_demand, allocation):
    """
    处理进程的资源请求

    参数:
        process_id: 请求资源的进程ID
        request: 请求的资源向量(列表)
        available: 当前可用资源向量(列表)
        max_demand: 进程最大需求矩阵(二维列表)
        allocation: 资源分配矩阵(二维列表)

    返回:
        (result, message, new_available, new_allocation, new_need, safe_sequence):
            result - 布尔值，请求是否成功
            message - 描述结果的字符串
            new_available - 分配后的可用资源
            new_allocation - 分配后的分配矩阵
            new_need - 分配后的需求矩阵
            safe_sequence - 安全序列(如果成功)
    """

    # 创建数据的深拷贝，以便在操作失败时可以回滚
    old_available = copy.deepcopy(available)
    old_allocation = copy.deepcopy(allocation)
    old_max_demand = copy.deepcopy(max_demand)

    # 步骤1：检查请求是否超过进程的最大需求
    for j in range(len(available)):
        if request[j] > (max_demand[process_id][j] - allocation[process_id][j]):
            return (False, f"错误：进程P{process_id}的请求超过其最大需求",
                    old_available, old_allocation, None, [])

    # 步骤2：检查请求是否超过当前可用资源
    for j in range(len(available)):
        if request[j] > available[j]:
            return (False, f"错误：进程P{process_id}的请求超过可用资源",
                    old_available, old_allocation, None, [])

    # 步骤3：尝试分配资源（假设可以）
    new_available = [available[j] - request[j] for j in range(len(available))]
    new_allocation = copy.deepcopy(allocation)
    new_allocation[process_id] = [allocation[process_id][j] + request[j] for j in range(len(available))]

    # 计算新的需求矩阵
    new_need = []
    for i in range(len(allocation)):
        process_need = [max_demand[i][j] - new_allocation[i][j] for j in range(len(available))]
        new_need.append(process_need)

    # 步骤4：进行安全检查
    is_safe, safe_sequence = safety_check(new_available, max_demand, new_allocation)

    if is_safe:
        return (True, f"成功：安全序列为 {safe_sequence}",
                new_available, new_allocation, new_need, safe_sequence)
    else:
        # 不安全状态，回滚操作
        return (False, "错误：分配会导致系统进入不安全状态",
                old_available, old_allocation, None, [])


def print_system_state(available, max_demand, allocation, need, resource_names, process_names):
    """
    打印系统当前状态

    参数:
        available: 可用资源向量
        max_demand: 最大需求矩阵
        allocation: 分配矩阵
        need: 需求矩阵
        resource_names: 资源名称列表
        process_names: 进程名称列表
    """
    # 打印可用资源
    print("\n" + "=" * 50)
    print("当前系统状态")
    print("=" * 50)

    # 打印可用资源
    print("\n可用资源:")
    for i, res in enumerate(resource_names):
        print(f"{res}: {available[i]}", end="  ")
    print()

    # 打印标题
    print("\n" + "-" * 70)
    header = f"{'进程':<6}"
    for res in resource_names:
        header += f"{'Max_' + res:<6}"
    for res in resource_names:
        header += f"{'Alloc_' + res:<6}"
    for res in resource_names:
        header += f"{'Need_' + res:<6}"
    print(header)
    print("-" * 70)

    # 打印每个进程的资源情况
    for i, process in enumerate(process_names):
        row = f"{process:<6}"
        # 最大需求
        for j in range(len(resource_names)):
            row += f"{max_demand[i][j]:<6}"
        # 已分配资源
        for j in range(len(resource_names)):
            row += f"{allocation[i][j]:<6}"
        # 需求资源
        for j in range(len(resource_names)):
            row += f"{need[i][j]:<6}"
        print(row)
    print("-" * 70)


def main():
    """
    主函数 - 演示银行家算法的使用
    """
    # ========================================
    # 初始化系统状态
    # ========================================

    # 资源名称
    resource_names = ['A', 'B', 'C']

    # 进程名称
    process_names = ['P0', 'P1', 'P2', 'P3', 'P4']

    # 可用资源向量: [A, B, C]
    available = [3, 3, 2]

    # 最大需求矩阵 (Max Demands)
    max_demand = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3]  # P4
    ]

    # 当前分配矩阵 (Allocations)
    allocation = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]  # P4
    ]

    # 计算当前需求矩阵 (Need = Max - Allocation)
    need = []
    for i in range(len(allocation)):
        process_need = [max_demand[i][j] - allocation[i][j] for j in range(len(available))]
        need.append(process_need)

    # 打印初始系统状态
    print("初始系统状态:")
    print_system_state(available, max_demand, allocation, need, resource_names, process_names)

    # ========================================
    # 执行安全检查
    # ========================================
    print("\n执行安全检查...")
    is_safe, safe_sequence = safety_check(available, max_demand, allocation)

    if is_safe:
        print(f"✓ 系统安全! 安全序列: {' → '.join([f'P{i}' for i in safe_sequence])}")
    else:
        print("✗ 系统不安全!")

    # ========================================
    # 模拟进程请求资源
    # ========================================
    # 示例1: P1请求资源 [1, 0, 2]
    print("\n模拟1: 进程P1请求资源 [1, 0, 2]")
    success, message, new_available, new_allocation, new_need, safe_seq = request_resources(
        process_id=1,
        request=[1, 0, 2],
        available=available,
        max_demand=max_demand,
        allocation=allocation
    )

    print(message)
    if success:
        # 更新系统状态
        available = new_available
        allocation = new_allocation
        need = new_need
        print_system_state(available, max_demand, allocation, need, resource_names, process_names)

    # 示例2: P0请求资源 [0, 2, 0] (可能导致不安全状态)
    print("\n模拟2: 进程P0请求资源 [0, 2, 0]")
    success, message, new_available, new_allocation, new_need, safe_seq = request_resources(
        process_id=0,
        request=[0, 2, 0],
        available=available,
        max_demand=max_demand,
        allocation=allocation
    )

    print(message)
    if success:
        # 更新系统状态
        available = new_available
        allocation = new_allocation
        need = new_need
        print_system_state(available, max_demand, allocation, need, resource_names, process_names)
    else:
        # 保持原状态
        print("资源分配未发生改变，系统状态保持不变")

    # 示例3: P4请求资源 [3, 3, 0] (超过最大需求)
    print("\n模拟3: 进程P4请求资源 [3, 3, 0]")
    success, message, new_available, new_allocation, new_need, safe_seq = request_resources(
        process_id=4,
        request=[3, 3, 0],
        available=available,
        max_demand=max_demand,
        allocation=allocation
    )

    print(message)

    # 示例4: P2请求资源 [0, 0, 1] (超过可用资源)
    print("\n模拟4: 进程P2请求资源 [0, 0, 1]")
    success, message, new_available, new_allocation, new_need, safe_seq = request_resources(
        process_id=2,
        request=[0, 0, 1],
        available=available,
        max_demand=max_demand,
        allocation=allocation
    )

    print(message)


if __name__ == "__main__":

    main()