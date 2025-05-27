import copy

def bankers_algorithm(Max, Need, Available, Allocated, Request, process_index):
    n = len(Max)  # 进程数
    m = len(Available)  # 资源种类数

    # 检查请求是否合法
    for j in range(m):
        if Request[j] > Need[process_index][j]:
            return False, Max, Need, Available, Allocated
    for j in range(m):
        if Request[j] > Available[j]:
            return False, Max, Need, Available, Allocated

    # 模拟分配
    work_allocated = copy.deepcopy(Allocated)
    work_available = Available.copy()
    work_need = copy.deepcopy(Need)

    for j in range(m):
        work_available[j] -= Request[j]
        work_allocated[process_index][j] += Request[j]
        work_need[process_index][j] -= Request[j]

    # 安全性检查
    work = work_available.copy()
    finish = [False] * n

    for _ in range(n):
        found = False
        for i in range(n):
            if not finish[i] and all(work_need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += work_allocated[i][j]
                finish[i] = True
                found = True
        if not found:
            break

    if all(finish):
        return True, Max, work_need, work_available, work_allocated
    else:
        return False, Max, Need, Available, Allocated


# 示例数据
Max = [[7, 5, 3],
       [3, 2, 2],
       [9, 0, 2],
       [2, 2, 2],
       [4, 3, 3]]

Allocated = [[0, 1, 0],
             [2, 0, 0],
             [3, 0, 2],
             [2, 1, 1],
             [0, 0, 2]]

Available = [3, 3, 2]

Need = [[7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]]

Request = [1, 0, 2]
process_index = 1

# 调用函数
can_allocate, newMax, newNeed, newAvailable, newAllocated = bankers_algorithm(
    Max, Need, Available, Allocated, Request, process_index
)

print("是否可以分配:", can_allocate)
print("分配后 Available:", newAvailable)
print("分配后 Allocated[1]:", newAllocated[1])
print("分配后 Need[1]:", newNeed[1])