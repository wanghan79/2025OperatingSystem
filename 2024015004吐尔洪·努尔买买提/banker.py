# 定义相关数据结构
max_matrix = [
    [0, 0, 4, 4],
    [2, 7, 5, 0],
    [3, 6, 10, 10],
    [0, 9, 8, 4],
    [0, 6, 6, 10]
]
need_matrix = [
    [0, 0, 1, 2],
    [1, 7, 5, 0],
    [2, 3, 5, 6],
    [0, 6, 5, 2],
    [0, 6, 5, 6]
]
available = [1, 6, 2, 2]
processes = ["P0", "P1", "P2", "P3", "P4"]


# 计算分配矩阵（Allocation = Max - Need）
def calculate_allocation():
    allocation_matrix = []
    for i in range(len(max_matrix)):
        allocation = [max_matrix[i][j] - need_matrix[i][j] for j in range(len(max_matrix[i]))]
        allocation_matrix.append(allocation)
    return allocation_matrix


# 银行家算法判断是否安全
def is_safe(allocation_matrix):
    work = available.copy()
    finish = [False] * len(processes)
    safe_sequence = []

    while True:
        found = False
        for i in range(len(processes)):
            if not finish[i] and all(need_matrix[i][j] <= work[j] for j in range(len(work))):
                # 分配资源
                for j in range(len(work)):
                    work[j] += allocation_matrix[i][j]
                finish[i] = True
                safe_sequence.append(processes[i])
                found = True
        if not found:
            break

    return all(finish), safe_sequence


# 处理请求
def handle_request(process_index, request):
    # 检查请求是否超过需求
    if any(request[j] > need_matrix[process_index][j] for j in range(len(request))):
        print("请求超过进程需求，无法分配")
        return available, need_matrix, allocation_matrix

    # 检查可用资源是否满足请求
    if any(request[j] > available[j] for j in range(len(request))):
        print("可用资源不足，无法分配")
        return available, need_matrix, allocation_matrix

    # 尝试分配资源
    new_available = [available[j] - request[j] for j in range(len(available))]
    new_need = [need_matrix[process_index][j] - request[j] for j in range(len(need_matrix[process_index]))]
    new_allocation = [allocation_matrix[process_index][j] + request[j] for j in range(len(allocation_matrix[process_index]))]

    # 更新矩阵
    available = new_available
    need_matrix[process_index] = new_need
    allocation_matrix[process_index] = new_allocation

    # 检查是否安全
    is_safe_state, safe_seq = is_safe(allocation_matrix)
    if is_safe_state:
        print("分配成功，安全序列为:", safe_seq)
    else:
        # 回滚资源分配
        available = [available[j] + request[j] for j in range(len(available))]
        need_matrix[process_index] = [need_matrix[process_index][j] + request[j] for j in range(len(need_matrix[process_index]))]
        allocation_matrix[process_index] = [allocation_matrix[process_index][j] - request[j] for j in range(len(allocation_matrix[process_index]))]
        print("分配后系统不安全，取消分配")

    return available, need_matrix, allocation_matrix


if __name__ == "__main__":
    allocation_matrix = calculate_allocation()
    print("分配矩阵:")
    for row in allocation_matrix:
        print(row)

    # 问题 (1) 判断是否安全
    is_safe_state, safe_sequence = is_safe(allocation_matrix)
    if is_safe_state:
        print("系统处于安全状态，安全序列为:", safe_sequence)
    else:
        print("系统处于不安全状态")

    # 问题 (2) 处理 P2 的请求 Request(1,2,2,2)
    p2_index = processes.index("P2")
    request = [1, 2, 2, 2]
    available, need_matrix, allocation_matrix = handle_request(p2_index, request)

    # 问题 (3) 检查是否立即进入死锁（分配后再次检查安全状态）
    is_safe_state_after, _ = is_safe(allocation_matrix)
    if not is_safe_state_after:
        print("系统立即满足 P2 请求后进入不安全状态，但不一定立即死锁，死锁需要后续进程请求等条件触发 ，不过当前安全检查不通过")
    else:
        print("系统立即满足 P2 请求后仍处于安全状态")