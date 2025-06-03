def print_matrix(title, matrix, processes, resources):
    print(f"\n{title}")
    header = "    " + " ".join([f"R{j}" for j in range(resources)])
    print(header)
    for i in range(processes):
        row = " ".join([f"{val:2d}" for val in matrix[i]])
        print(f"P{i}  {row}")

def safety_check(available, allocation, need):
    n_processes = len(allocation)
    n_resources = len(available)
    work = available.copy()
    finish = [False] * n_processes
    safe_sequence = []

    for _ in range(n_processes):
        found = False
        for i in range(n_processes):
            if not finish[i]:
                need_met = True
                for j in range(n_resources):
                    if need[i][j] > work[j]:
                        need_met = False
                        break
                if need_met:
                    for j in range(n_resources):
                        work[j] += allocation[i][j]
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

def banker_algorithm(process_id, request, available, max_matrix, allocation, need):
    n_resources = len(available)
    # Step 1: Check if request <= need
    for j in range(n_resources):
        if request[j] > need[process_id][j]:
            return False, "错误：请求超过进程需求。"
    # Step 2: Check if request <= available
    for j in range(n_resources):
        if request[j] > available[j]:
            return False, "错误：请求超过系统可用资源。"
    # Tentatively allocate resources
    new_available = [available[j] - request[j] for j in range(n_resources)]
    new_allocation = [row.copy() for row in allocation]
    new_need = [row.copy() for row in need]
    for j in range(n_resources):
        new_allocation[process_id][j] += request[j]
        new_need[process_id][j] -= request[j]
    # Check safety
    is_safe, safe_sequence = safety_check(new_available, new_allocation, new_need)
    if is_safe:
        return True, safe_sequence
    else:
        return False, "警告：分配后将导致系统不安全。"

if __name__ == "__main__":
    # 初始化
    available = [3, 3, 2]
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    need = [
        [7-0, 5-1, 3-0],
        [3-2, 2-0, 2-0],
        [9-3, 0-0, 2-2],
        [2-2, 2-1, 2-1],
        [4-0, 3-0, 3-2]
    ]
    processes = 5
    resources = 3

    # 初始状态
    print("="*50)
    print("初始系统状态：")
    print("\n可利用资源向量 Available:")
    print("R0 R1 R2")
    print(" ".join(f"{val:2d}" for val in available))

    print_matrix("最大需求矩阵 Max:", max_matrix, processes, resources)
    print_matrix("分配矩阵 Allocation:", allocation, processes, resources)
    print_matrix("需求矩阵 Need:", need, processes, resources)

    # 执行安全检测算法
    is_safe, safe_sequence = safety_check(available.copy(), allocation, need)
    print("\n" + "="*50)
    print("初始安全检测结果：")
    if is_safe:
        print("系统处于安全状态，安全序列为：", " → ".join(f"P{p}" for p in safe_sequence))
    else:
        print("系统处于不安全状态！")

    # 模拟银行家算法请求（P1请求[1,0,2]）
    print("\n" + "="*50)
    request = [1, 0, 2]
    pid = 1
    print(f"模拟请求：进程P{pid} 请求资源 {request}")
    success, result = banker_algorithm(pid, request, available, max_matrix, allocation, need)
    
    if success:
        print("请求安全，分配后安全序列为：", " → ".join(f"P{p}" for p in result))
    else:
        print(result)