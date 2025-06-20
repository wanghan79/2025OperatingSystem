def banker_algorithm(Max, Need, Available, Allocated, Request, process_id):
    # 检查请求是否超过当前需求
    for i in range(len(Request)):
        if Request[i] > Need[process_id][i]:
            print(f"进程 {process_id} 请求的资源超过了当前需求，无法分配。")
            return False, Max, Need, Available, Allocated

    # 检查请求是否超过可用资源
    for i in range(len(Request)):
        if Request[i] > Available[i]:
            print(f"进程 {process_id} 请求的资源超过了可用资源，无法分配。")
            return False, Max, Need, Available, Allocated

    # 尝试分配资源
    Available_temp = Available[:]
    Allocated_temp = [row[:] for row in Allocated]
    Need_temp = [row[:] for row in Need]

    # 更新临时矩阵
    for i in range(len(Request)):
        Available_temp[i] -= Request[i]
        Allocated_temp[process_id][i] += Request[i]
        Need_temp[process_id][i] -= Request[i]

    # 检查是否安全
    Finish = [False] * len(Max)
    Work = Available_temp[:]
    safe_sequence = []

    while True:
        found = False
        for i in range(len(Max)):
            if not Finish[i]:
                # 检查是否可以满足进程i的需求
                if all(Need_temp[i][j] <= Work[j] for j in range(len(Work))):
                    # 找到一个可满足的进程
                    for j in range(len(Work)):
                        Work[j] += Allocated_temp[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
        if not found:
            break

    # 检查是否所有进程都完成了
    if all(Finish):
        print("可以安全分配，安全序列：", safe_sequence)
        return True, Max, Need_temp, Available_temp, Allocated_temp
    else:
        print("无法安全分配，系统可能进入不安全状态。")
        return False, Max, Need, Available, Allocated


# 示例
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

Available = [10, 5, 7]

Request = [1, 0, 2]  # 假设是第一个进程的请求
process_id = 0  # 请求资源的进程编号

can_allocate, Max, Need, Available, Allocated = banker_algorithm(Max, Need, Available, Allocated, Request, process_id)
print("是否可以分配：", can_allocate)
print("分配后的Max矩阵：", Max)
print("分配后的Need矩阵：", Need)
print("分配后的Available向量：", Available)
print("分配后的Allocated矩阵：", Allocated)