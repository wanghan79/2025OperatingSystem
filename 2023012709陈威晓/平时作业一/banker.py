def check_safety(available, allocated, need):
    n_processes = len(allocated)
    n_resources = len(available)
    work = available.copy()
    finish = [False] * n_processes
    safe_sequence = []

    while True:
        found = False
        for i in range(n_processes):
            if not finish[i]:
                can_run = True
                for j in range(n_resources):
                    if need[i][j] > work[j]:
                        can_run = False
                        break
                if can_run:
                    for j in range(n_resources):
                        work[j] += allocated[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
        if not found:
            break

    if all(finish):
        return True, safe_sequence
    else:
        return False, []


def bankers_algorithm(Max, Need, Available, Allocated, process_id, request):
    # 验证请求是否合法
    for j in range(len(request)):
        if request[j] > Need[process_id][j]:
            print("Error: Request exceeds need.")
            return False, Max, Need, Available, Allocated
    for j in range(len(request)):
        if request[j] > Available[j]:
            print("Error: Insufficient available resources.")
            return False, Max, Need, Available, Allocated

    # 保存原始状态
    old_available = Available.copy()
    old_allocated = [row.copy() for row in Allocated]
    old_need = [row.copy() for row in Need]

    # 试分配
    new_available = [old_available[j] - request[j] for j in range(len(request))]
    new_allocated = [row.copy() for row in old_allocated]
    for j in range(len(request)):
        new_allocated[process_id][j] += request[j]
    new_need = [row.copy() for row in old_need]
    for j in range(len(request)):
        new_need[process_id][j] -= request[j]

    # 安全性检查
    is_safe, safe_sequence = check_safety(new_available, new_allocated, new_need)

    if is_safe:
        print("请求安全，分配成功。安全序列：", safe_sequence)
        return True, Max, new_need, new_available, new_allocated
    else:
        print("请求不安全，拒绝分配。")
        return False, Max, old_need, old_available, old_allocated


# 示例用法
if __name__ == "__main__":
    # 初始矩阵
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    Allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    Need = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]
    Available = [3, 3, 2]
    process_id = 1
    request = [1, 0, 2]

    # 调用银行家算法
    result, new_Max, new_Need, new_Available, new_Allocated = bankers_algorithm(
        Max, Need, Available, Allocated, process_id, request
    )

    # 输出结果
    print("\n分配结果:", result)
    print("Max矩阵保持不变:")
    for row in new_Max:
        print(row)
    print("\n新的Need矩阵:")
    for row in new_Need:
        print(row)
    print("\n新的Available矩阵:")
    print(new_Available)
    print("\n新的Allocated矩阵:")
    for row in new_Allocated:
        print(row)