def print_matrix(title: str, matrix: list, processes: int, resources: int) -> None:
    """打印矩阵信息（最大需求/分配/需求矩阵）"""
    print(f"\n{title}")
    header = "    " + " ".join([f"R{j}" for j in range(resources)])  # 生成资源列头
    print(header)
    for i in range(processes):
        # 格式化进程行数据（每个元素占2位宽度）
        row = " ".join([f"{val:2d}" for val in matrix[i]])
        print(f"P{i}  {row}")
def safety_check(available: list, allocation: list, need: list) -> tuple[bool, list]:
    """
    安全性检查算法
    """
    n_processes = len(allocation)  # 进程数
    n_resources = len(available)  # 资源种类数
    work = available.copy()  # 工作向量（可用资源副本）
    finish = [False] * n_processes  # 进程完成状态
    safe_sequence = []  # 安全序列

    # 核心检查逻辑（最多执行n_processes次循环）
    for _ in range(n_processes):
        found = False  # 是否找到可执行进程标记
        for i in range(n_processes):
            if not finish[i]:
                # 检查当前进程所有资源需求是否都可满足
                if all(need[i][j] <= work[j] for j in range(n_resources)):
                    # 模拟分配资源：回收已分配资源到work向量
                    for j in range(n_resources):
                        work[j] += allocation[i][j]
                    finish[i] = True  # 标记进程完成
                    safe_sequence.append(i)  # 添加到安全序列
                    found = True
                    break  # 找到一个进程后立即处理下一轮
        if not found:  # 无可用进程，提前终止
            break
    return all(finish), safe_sequence  # 返回安全状态和序列

def banker_algorithm(pid: int, request: list,
                     available: list, max_matrix: list,
                     allocation: list, need: list) -> tuple[bool, str]:
    """
    银行家算法核心逻辑
    :param pid: 请求资源的进程ID
    :param request: 请求的资源向量
    :return: (是否允许分配, 结果信息)
    """
    n_resources = len(available)
    # 步骤1：检查请求是否超过进程声明的最大需求
    for j in range(n_resources):
        if request[j] > need[pid][j]:
            return False, f"错误：进程P{pid}的请求超过最大需求"
    # 步骤2：检查请求是否超过系统当前可用资源
    for j in range(n_resources):
        if request[j] > available[j]:
            return False, f"错误：进程P{pid}的请求超过可用资源"
    # 步骤3：尝试预分配资源（创建副本避免修改原始数据）
    new_available = available.copy()
    new_allocation = [row.copy() for row in allocation]
    new_need = [row.copy() for row in need]
    for j in range(n_resources):
        new_available[j] -= request[j]  # 减少系统可用资源
        new_allocation[pid][j] += request[j]  # 增加进程已分配资源
        new_need[pid][j] -= request[j]  # 减少进程剩余需求
    # 步骤4：进行安全性检查
    is_safe, safe_seq = safety_check(new_available, new_allocation, new_need)
    if is_safe:
        return True, f"分配成功，安全序列为：{' → '.join(f'P{p}' for p in safe_seq)}"
    else:
        return False, f"分配失败：将导致系统进入不安全状态"
if __name__ == "__main__":
    # 初始化系统资源状态（3类资源，5个进程）
    available = [3, 3, 2]
    max_matrix = [
        [7, 5, 3],  # P0最大需求
        [3, 2, 2],  # P1最大需求
        [9, 0, 2],  # P2最大需求
        [2, 2, 2],  # P3最大需求
        [4, 3, 3]  # P4最大需求
    ]
    allocation = [
        [0, 1, 0],  # P0已分配资源
        [2, 0, 0],  # P1已分配资源
        [3, 0, 2],  # P2已分配资源
        [2, 1, 1],  # P3已分配资源
        [0, 0, 2]  # P4已分配资源
    ]

    # 计算需求矩阵 Need = Max - Allocation
    need = [
        [max_matrix[i][j] - allocation[i][j]
         for j in range(3)] for i in range(5)
    ]

    processes, resources = 5, 3  # 进程数和资源数
    # 输出可用资源
    print("\n当前系统可用资源向量 Available:")
    print(" ".join([f"R{j}:{val:2d}" for j, val in enumerate(available)]))
    # 输出各矩阵信息
    print_matrix("最大需求矩阵 Max:", max_matrix, processes, resources)
    print_matrix("已分配矩阵 Allocation:", allocation, processes, resources)
    print_matrix("需求矩阵 Need:", need, processes, resources)
    # 执行初始安全检查
    is_safe, safe_seq = safety_check(available.copy(), allocation, need)
    print("\n" + "=" * 50)
    print("初始系统安全性检查结果：")
    if is_safe:
        print(f"系统处于安全状态，安全序列为：{' → '.join(f'P{p}' for p in safe_seq)}")
    else:
        print("系统处于不安全状态！")
    # 模拟进程请求（P1请求资源[1,0,2]）
    print("\n" + "=" * 50)
    pid, request = 1, [1, 0, 2]
    print(f"模拟进程P{pid}请求资源：{request}")
    success, msg = banker_algorithm(pid, request, available, max_matrix, allocation, need)
    print(msg)
