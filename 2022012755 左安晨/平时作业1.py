def banker_algorithm(max_matrix, allocated_matrix, available_matrix, request_process, request_vector):
    """
    银行家算法实现

    参数:
        max_matrix: 每个进程的最大需求矩阵 (n×m)
        allocated_matrix: 当前已分配矩阵 (n×m)
        available_matrix: 可用资源向量 (1×m)
        request_process: 请求资源的进程索引 (0-based)
        request_vector: 请求的资源向量 (1×m)

    返回:
        (是否安全, 安全序列, 新的分配矩阵, 新的需求矩阵, 新的可用向量)
    """
    # 复制矩阵以避免修改原始数据
    max_matrix = [row[:] for row in max_matrix]
    allocated = [row[:] for row in allocated_matrix]
    available = available_matrix[:]
    need = []

    # 计算需求矩阵 Need = Max - Allocated
    n = len(max_matrix)  # 进程数
    m = len(available)  # 资源类型数

    for i in range(n):
        need_row = [max_matrix[i][j] - allocated[i][j] for j in range(m)]
        need.append(need_row)

    # 1. 检查请求是否小于等于需求
    for j in range(m):
        if request_vector[j] > need[request_process][j]:
            return (False, [], allocated, need, available, "错误：请求超过了声明的最大需求")

    # 2. 检查请求是否小于等于可用资源
    for j in range(m):
        if request_vector[j] > available[j]:
            return (False, [], allocated, need, available, "错误：请求超过了可用资源")

    # 3. 尝试分配资源
    for j in range(m):
        available[j] -= request_vector[j]
        allocated[request_process][j] += request_vector[j]
        need[request_process][j] -= request_vector[j]

    # 4. 检查安全性
    work = available[:]
    finish = [False] * n
    safe_sequence = []

    while True:
        found = False
        for i in range(n):
            if not finish[i]:
                can_allocate = True
                for j in range(m):
                    if need[i][j] > work[j]:
                        can_allocate = False
                        break

                if can_allocate:
                    # 释放资源
                    for j in range(m):
                        work[j] += allocated[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

        if not found:
            break

    # 检查是否所有进程都完成了
    if all(finish):
        return (True, safe_sequence, allocated, need, available, "安全：请求可以立即授予")
    else:
        # 回滚分配
        for j in range(m):
            available[j] += request_vector[j]
            allocated[request_process][j] -= request_vector[j]
            need[request_process][j] += request_vector[j]
        return (False, [], allocated_matrix, need, available_matrix, "不安全：请求会导致系统进入不安全状态")


def print_matrices(allocated, need, available, max_matrix):
    """打印各个矩阵"""
    print("\n当前系统状态:")
    print("Max矩阵:")
    for row in max_matrix:
        print(row)

    print("\nAllocated矩阵:")
    for row in allocated:
        print(row)

    print("\nNeed矩阵:")
    for row in need:
        print(row)

    print("\nAvailable向量:")
    print(available)


# 示例使用
if __name__ == "__main__":
    # 示例数据
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    allocated_matrix = [
        [0, 9, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    available_matrix = [3, 99, 2]

    # 进程P1(索引为1)请求资源 (1, 0, 2)
    request_process = 1
    request_vector = [1, 0, 2]

    print("初始状态:")
    print_matrices(allocated_matrix,
                   [[max_matrix[i][j] - allocated_matrix[i][j] for j in range(len(available_matrix))] for i in
                    range(len(max_matrix))],
                   available_matrix,
                   max_matrix)

    print(f"\n进程 P{request_process} 请求资源: {request_vector}")

    # 调用银行家算法
    is_safe, safe_sequence, new_allocated, new_need, new_available, message = banker_algorithm(
        max_matrix, allocated_matrix, available_matrix, request_process, request_vector
    )

    print("\n结果:", message)
    if is_safe:
        print("安全序列:", safe_sequence)
        print_matrices(new_allocated, new_need, new_available, max_matrix)
    else:
        print_matrices(new_allocated, new_need, new_available, max_matrix)