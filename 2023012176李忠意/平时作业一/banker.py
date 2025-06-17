import copy

def safety_check(*args):
    """
    安全性检测算法（Safety Algorithm）
    参数：
        allocated: 已分配矩阵（list of list of int）
        need:    需求矩阵（list of list of int）
        available: 可用资源向量（list of int）
    返回：
        (is_safe, safe_sequence)
        is_safe: bool, 是否是一个安全状态
        safe_sequence: 若安全，返回一个安全序列列表，否则返回None
    """
    allocated, need, available = args
    # 初始化
    work = available.copy()
    finish = [False] * len(allocated)
    safe_sequence = []

    while True:
        allocated_this_round = False
        for i in range(len(allocated)):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                # 模拟进程i完成，释放资源
                for j in range(len(work)):
                    work[j] += allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                allocated_this_round = True
        if not allocated_this_round:
            break

    if all(finish):
        return True, safe_sequence
    else:
        return False, None


def bankers_algorithm(*args):
    """
    银行家算法（Banker's Algorithm）
    参数：
        max_matrix:   最大需求矩阵（list of list of int）
        need_matrix:  需求矩阵（list of list of int）
        available:    可用资源向量（list of int）
        allocated:    已分配矩阵（list of list of int）
        request:      请求资源向量（list of int）
        pid:          请求进程号（int）
    返回：
        (allocated_flag, (new_allocated, new_need, new_available, new_max), safe_sequence)
        allocated_flag: bool, 请求是否被批准
        new_allocated, new_need, new_available, new_max: 若批准，则返回更新后的矩阵和向量；否则返回原始状态
        safe_sequence: 若批准且安全，则返回一个安全序列，否则为None
    """
    max_matrix, need_matrix, available, allocated, request, pid = args
    # 深拷贝避免修改原始数据
    new_allocated = copy.deepcopy(allocated)
    new_need = copy.deepcopy(need_matrix)
    new_available = available.copy()
    new_max = copy.deepcopy(max_matrix)

    # 检查请求是否小于等于need
    if any(request[j] > new_need[pid][j] for j in range(len(request))):
        print(f"Error: 请求超过进程{pid}的需求")
        return False, (allocated, need_matrix, available, max_matrix), None
    # 检查请求是否小于等于available
    if any(request[j] > new_available[j] for j in range(len(request))):
        print(f"Error: 资源不足，无法满足进程{pid}的请求")
        return False, (allocated, need_matrix, available, max_matrix), None

    # 试探性分配
    for j in range(len(request)):
        new_available[j] -= request[j]
        new_allocated[pid][j] += request[j]
        new_need[pid][j] -= request[j]

    # 安全性检测
    is_safe, safe_sequence = safety_check(new_allocated, new_need, new_available)
    if is_safe:
        print(f"请求被批准，系统处于安全状态。安全序列: {safe_sequence}")
        return True, (new_allocated, new_need, new_available, new_max), safe_sequence
    else:
        print("请求被拒绝，系统处于不安全状态，回滚。")
        return False, (allocated, need_matrix, available, max_matrix), None


if __name__ == "__main__":
    max_matrix = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    need_matrix = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
    available = [3, 3, 2]
    request = [1, 0, 2]
    pid = 1

    # 调用银行家算法
    result, matrices, seq = bankers_algorithm(max_matrix, need_matrix, available, allocated, request, pid)
    print("分配结果：", result)
    if result:
        new_alloc, new_need, new_avail, _ = matrices
        print("Updated Allocated:", new_alloc)
        print("Updated Need:", new_need)
        print("Updated Available:", new_avail)
