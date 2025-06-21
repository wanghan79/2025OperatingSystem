# 作业一：银行家算法
def banker_algorithm(max_matrix, need_matrix, available, allocated, request, pid):

    # 检查请求合法性
    for i in range(len(request)):
        if request[i] > need_matrix[pid][i] or request[i] > available[i]:
            return False, {}

    # 模拟分配后的状态
    new_available = [available[i] - request[i] for i in range(len(available))]
    new_allocated = [row[:] for row in allocated]
    new_need = [row[:] for row in need_matrix]

    for i in range(len(request)):
        new_allocated[pid][i] += request[i]
        new_need[pid][i] -= request[i]

    # 安全性检查
    work = new_available[:]
    finish = [False] * len(allocated)
    safe_sequence = []

    for _ in range(len(allocated)):
        found = False
        for i in range(len(allocated)):
            if not finish[i]:
                can_complete = all(new_need[i][j] <= work[j] for j in range(len(work)))
                if can_complete:
                    for j in range(len(work)):
                        work[j] += new_allocated[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
        if not found:
            return False, {}

    return True, {
        'Max': max_matrix,
        'Allocated': new_allocated,
        'Need': new_need,
        'Available': new_available,
        'SafeSequence': safe_sequence
    }


def print_system_state(max_matrix, allocated, need_matrix, available):
    print("系统当前状态:")
    print("进程\tMax\t\tAllocated\tNeed")
    for i in range(len(max_matrix)):
        print(f"P{i}\t{max_matrix[i]}\t{allocated[i]}\t\t{need_matrix[i]}")
    print(f"Available: {available}")

if __name__ == "__main__":
    # 测试银行家算法
    print("=== 银行家算法测试 ===")

    # 初始系统状态
    max_matrix = [[3, 2, 2], [6, 1, 3], [3, 1, 4]]
    allocated = [[1, 0, 0], [5, 1, 2], [2, 1, 1]]
    need_matrix = [[2, 2, 2], [1, 0, 1], [1, 0, 3]]
    available = [2, 1, 2]

    print_system_state(max_matrix, allocated, need_matrix, available)

    # 测试请求1：进程1请求资源[1, 0, 1]
    request = [1, 0, 1]
    process_id = 1

    print(f"进程P{process_id}请求资源: {request}")
    success, result = banker_algorithm(max_matrix, need_matrix, available, allocated, request, process_id)

    if success:
        print("分配成功!")
        print(f"安全序列: {result['SafeSequence']}")
        print(f"分配后可用资源: {result['Available']}")
        print("分配后系统状态:")
        print_system_state(result['Max'], result['Allocated'], result['Need'], result['Available'])
    else:
        print("分配失败! 系统将处于不安全状态")

    print("\n" + "=" * 50)

    # 测试请求2：进程0请求资源[1, 1, 0]
    request2 = [1, 1, 0]
    process_id2 = 0

    print(f"进程P{process_id2}请求资源: {request2}")
    success2, result2 = banker_algorithm(max_matrix, need_matrix, available, allocated, request2, process_id2)

    if success2:
        print("分配成功!")
        print(f"安全序列: {result2['SafeSequence']}")
        print(f"分配后可用资源: {result2['Available']}")
    else:
        print("分配失败! 系统将处于不安全状态")