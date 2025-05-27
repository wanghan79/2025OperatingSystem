def banker_algorithm(Max, Need, Available, Allocated, Request):
    num_processes = len(Max)
    num_resources = len(Available)

    # 检查请求是否超过进程的最大需求
    for i in range(num_resources):
        if Request[i] > Need[0][i]:
            print("错误：请求超过了进程的最大需求。")
            return False, Max, Need, Available, Allocated

    # 检查请求是否超过可用资源
    for i in range(num_resources):
        if Request[i] > Available[i]:
            print("错误：请求超过了可用资源。")
            return False, Max, Need, Available, Allocated

    # 尝试分配资源
    new_Available = [Available[i] - Request[i] for i in range(num_resources)]
    new_Allocated = [Allocated[j][:] for j in range(num_processes)]
    new_Allocated[0] = [new_Allocated[0][i] + Request[i] for i in range(num_resources)]
    new_Need = [[Max[j][i] - new_Allocated[j][i] for i in range(num_resources)] for j in range(num_processes)]

    # 检查系统是否处于安全状态
    def is_safe(avail, max_need, alloc):
        work = avail[:]
        finish = [False] * num_processes
        safe_sequence = []

        while True:
            found = False
            for i in range(num_processes):
                if not finish[i] and all([max_need[i][j] - alloc[i][j] <= work[j] for j in range(num_resources)]):
                    for j in range(num_resources):
                        work[j] += alloc[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
            if not found:
                break

        return all(finish)

    if is_safe(new_Available, Max, new_Allocated):
        print("请求被批准，系统仍处于安全状态。")
        return True, Max, new_Need, new_Available, new_Allocated
    else:
        print("请求被拒绝，系统将进入不安全状态。")
        return False, Max, Need, Available, Allocated


# 获取用户输入
num_processes = int(input("请输入进程的数量: "))
num_resources = int(input("请输入资源的种类数量: "))

print("请输入 Max 矩阵（每行用空格分隔，按行输入）:")
Max = []
for _ in range(num_processes):
    row = list(map(int, input().split()))
    Max.append(row)

print("请输入 Allocated 矩阵（每行用空格分隔，按行输入）:")
Allocated = []
for _ in range(num_processes):
    row = list(map(int, input().split()))
    Allocated.append(row)

# 计算 Need 矩阵
Need = [[Max[i][j] - Allocated[i][j] for j in range(num_resources)] for i in range(num_processes)]

print("请输入 Available 矩阵（用空格分隔）:")
Available = list(map(int, input().split()))

print("请输入资源请求 Request（用空格分隔）:")
Request = list(map(int, input().split()))

can_allocate, new_Max, new_Need, new_Available, new_Allocated = banker_algorithm(Max, Need, Available, Allocated, Request)
print("是否能够分配:", can_allocate)
print("分配后的 Max 矩阵:", new_Max)
print("分配后的 Need 矩阵:", new_Need)
print("分配后的 Available 矩阵:", new_Available)
print("分配后的 Allocated 矩阵:", new_Allocated)
    