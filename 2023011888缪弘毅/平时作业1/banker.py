import copy

# 银行家算法函数
# 参数说明：
# Max: 每个进程最大资源需求矩阵
# Need: 每个进程还需资源矩阵（Need = Max - Allocated）
# Available: 当前系统可用的资源向量
# Allocated: 每个进程当前已分配的资源矩阵
# Request: 一个元组 (进程编号, 该进程对资源的请求向量)
def banker_algorithm(Max, Need, Available, Allocated, Request):
    process_index, request = Request  # 请求的进程编号及其请求向量
    num_resources = len(Available)    # 系统中资源的种类数

    # 第一步：检查请求是否超过该进程的最大需求（Need）
    if any(request[i] > Need[process_index][i] for i in range(num_resources)):
        return False, "Error: Request exceeds maximum need.", Max, Need, Available, Allocated

    # 第二步：检查请求是否超过当前系统可用资源
    if any(request[i] > Available[i] for i in range(num_resources)):
        return False, "Error: Not enough available resources.", Max, Need, Available, Allocated

    # 第三步：假设分配资源，更新 Available、Allocated 和 Need 的副本
    Available_copy = copy.deepcopy(Available)
    Allocated_copy = copy.deepcopy(Allocated)
    Need_copy = copy.deepcopy(Need)

    for i in range(num_resources):
        Available_copy[i] -= request[i]                      # 系统资源减少
        Allocated_copy[process_index][i] += request[i]       # 该进程获得资源
        Need_copy[process_index][i] -= request[i]            # 该进程剩余需求减少

    # 第四步：安全性检查，判断系统是否仍处于安全状态
    Work = Available_copy[:]             # 可用资源临时工作副本
    Finish = [False] * len(Max)          # 标记每个进程是否能完成

    while True:
        found = False
        for i in range(len(Max)):
            # 如果进程尚未完成，且其剩余需求小于等于当前可用资源
            if not Finish[i] and all(Need_copy[i][j] <= Work[j] for j in range(num_resources)):
                # 模拟该进程完成后释放资源
                for j in range(num_resources):
                    Work[j] += Allocated_copy[i][j]
                Finish[i] = True
                found = True  # 有进程可以完成
        if not found:
            break  # 没有任何进程可以完成，退出

    # 如果所有进程都能完成，说明是安全状态
    if all(Finish):
        return True, "Request can be safely granted.", Max, Need_copy, Available_copy, Allocated_copy
    else:
        return False, "Request would lead to unsafe state.", Max, Need, Available, Allocated


# ---------------------- 以下为示例数据和调用 -----------------------

# Max：每个进程最多需要的资源
Max = [[7, 5, 3],
       [3, 2, 2],
       [9, 0, 2],
       [2, 2, 2],
       [4, 3, 3]]

# Allocated：当前分配给每个进程的资源
Allocated = [[0, 1, 0],
             [2, 0, 0],
             [3, 0, 2],
             [2, 1, 1],
             [0, 0, 2]]

# Need：每个进程还需资源（= Max - Allocated）
Need = [[7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]]

# Available：当前系统可用资源
Available = [3, 3, 2]

# Request：进程1请求 [1, 0, 2] 的资源
Request = (1, [1, 0, 2])

# 执行银行家算法
result, message, Max_new, Need_new, Avail_new, Alloc_new = banker_algorithm(Max, Need, Available, Allocated, Request)

# 输出结果
print("是否可以分配资源:", result)

print("\nMax:")
for row in Max_new:
    print(row)

print("\nAvailable:", Avail_new)

print("\nNeed:")
for row in Need_new:
    print(row)

print("\nAllocated:")
for row in Alloc_new:
    print(row)
