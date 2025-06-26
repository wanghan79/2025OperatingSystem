def banker_algorithm(max_res, need, available, allocated, request):
    """
    银行家算法实现资源分配请求的安全检查

    参数:
        max_res (list): 每个进程的最大需求矩阵
        need (list): 每个进程还需要的资源矩阵
        available (list): 可用资源向量
        allocated (list): 已分配资源矩阵
        request (tuple): 请求 (进程ID, 请求资源向量)

    返回:
        tuple: (结果消息, 最大需求矩阵, 新需求矩阵, 新可用资源, 新分配矩阵)
    """
    pid, req = request
    process_count = len(max_res)
    resource_types = len(available)

    # 保存原始状态以便回滚
    original_state = {
        'need': [row[:] for row in need],
        'available': available[:],
        'allocated': [row[:] for row in allocated]
    }

    # 检查1: 请求是否超过进程声明的最大需求
    if any(req[j] > need[pid][j] for j in range(resource_types)):
        return ("错误：请求超过进程需求", max_res,
                original_state['need'],
                original_state['available'],
                original_state['allocated'])

    # 检查2: 系统是否有足够资源满足请求
    if any(req[j] > available[j] for j in range(resource_types)):
        return ("错误：请求超过可用资源", max_res,
                original_state['need'],
                original_state['available'],
                original_state['allocated'])

    # 尝试分配资源
    new_available = [available[j] - req[j] for j in range(resource_types)]
    new_allocated = [row[:] for row in allocated]
    new_need = [row[:] for row in need]

    for j in range(resource_types):
        new_allocated[pid][j] += req[j]
        new_need[pid][j] -= req[j]

    # 安全检查
    work = new_available[:]
    finish = [False] * process_count
    safe_sequence = []

    while True:
        found = False
        for i in range(process_count):
            if not finish[i] and all(new_need[i][j] <= work[j] for j in range(resource_types)):
                # 释放进程资源
                for j in range(resource_types):
                    work[j] += new_allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True

        if not found:
            break

    if all(finish):
        return (f"分配成功！安全序列: {safe_sequence}",
                max_res, new_need, new_available, new_allocated)
    else:
        return ("错误：分配会导致系统不安全", max_res,
                original_state['need'],
                original_state['available'],
                original_state['allocated'])


def print_system_state(max_res, allocated, need, available):
    """打印系统状态表格"""
    # 计算每列宽度
    max_len = 0
    for matrix in [max_res, allocated, need]:
        for row in matrix:
            for num in row:
                if len(str(num)) > max_len:
                    max_len = len(str(num))
    col_width = max(5, max_len + 2)

    # 打印表头
    headers = ["Max", "Allocated", "Need", "Available"]
    max_header_width = col_width * len(max_res[0])
    alloc_header_width = col_width * len(allocated[0])
    need_header_width = col_width * len(need[0])

    header_line = (
        f"{headers[0].ljust(max_header_width)} | "
        f"{headers[1].ljust(alloc_header_width)} | "
        f"{headers[2].ljust(need_header_width)} | "
        f"{headers[3]}"
    )
    print(header_line)
    print("-" * len(header_line))

    # 打印每行数据
    avail_str = "".join(f"{str(num):<{col_width}}" for num in available)
    for max_row, alloc_row, need_row in zip(max_res, allocated, need):
        max_str = "".join(f"{str(num):<{col_width}}" for num in max_row)
        alloc_str = "".join(f"{str(num):<{col_width}}" for num in alloc_row)
        need_str = "".join(f"{str(num):<{col_width}}" for num in need_row)
        print(f"{max_str} | {alloc_str} | {need_str} | {avail_str}")


if __name__ == "__main__":
    # 测试数据
    Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    Allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
    Available = [3, 3, 2]
    Request = (1, [1, 0, 2])  # 进程1请求资源[1,0,2]

    # 执行银行家算法
    result, Max_out, Need_out, Available_out, Allocated_out = banker_algorithm(
        Max, Need, Available, Allocated, Request
    )

    # 输出结果
    print(result)
    print("\n分配后系统状态：")
    print_system_state(Max_out, Allocated_out, Need_out, Available_out)