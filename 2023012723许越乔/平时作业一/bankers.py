def bankers_algorithm(max_matrix, need_matrix, available, allocated_matrix, request):
    """
    银行家算法实现

    参数:
    max_matrix - 最大需求矩阵，二维列表
    need_matrix - 需求矩阵，二维列表
    available - 可用资源向量，一维列表
    allocated_matrix - 已分配资源矩阵，二维列表
    request - 资源请求向量，一维列表

    返回:
    是否可以分配，分配后的四个矩阵
    """
    # 检查请求是否超过需求
    for i in range(len(request)):
        if request[i] > need_matrix[0][i]:
            return False, max_matrix, need_matrix, available, allocated_matrix

    # 检查请求是否超过可用资源
    for i in range(len(request)):
        if request[i] > available[i]:
            return False, max_matrix, need_matrix, available, allocated_matrix

    # 尝试分配资源
    temp_available = available.copy()
    temp_allocated = [row.copy() for row in allocated_matrix]
    temp_need = [row.copy() for row in need_matrix]

    for i in range(len(request)):
        temp_available[i] -= request[i]
        temp_allocated[0][i] += request[i]
        temp_need[0][i] -= request[i]

    # 检查安全性
    safe, safe_sequence = is_safe_state(temp_available, temp_need, temp_allocated)

    if safe:
        return True, max_matrix, temp_need, temp_available, temp_allocated
    else:
        return False, max_matrix, need_matrix, available, allocated_matrix


def is_safe_state(available, need_matrix, allocated_matrix):
    """检查系统是否处于安全状态"""
    work = available.copy()
    finish = [False] * len(need_matrix)
    safe_sequence = []

    while True:
        found = False
        for i in range(len(need_matrix)):
            if not finish[i]:
                # 检查是否可以满足进程i的需求
                can_allocate = True
                for j in range(len(work)):
                    if need_matrix[i][j] > work[j]:
                        can_allocate = False
                        break

                if can_allocate:
                    # 分配资源并回收
                    for j in range(len(work)):
                        work[j] += allocated_matrix[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

        if not found:
            break

    # 检查是否所有进程都能完成
    for i in range(len(finish)):
        if not finish[i]:
            return False, []

    return True, safe_sequence


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
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    need_matrix = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]

    available = [3, 3, 2]

    # 进程0请求资源 [1, 0, 2]
    request = [1, 0, 2]

    # 调用银行家算法
    result, new_max, new_need, new_available, new_allocated = bankers_algorithm(
        max_matrix, need_matrix, available, allocated_matrix, request
    )

    print("是否可以分配:", result)
    if result:
        print("分配后的可用资源:", new_available)
        print("分配后的需求矩阵:", new_need)
        print("分配后的已分配矩阵:", new_allocated)
