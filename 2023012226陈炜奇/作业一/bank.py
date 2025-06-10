def vector_less_equal(v1, v2):
    return all(x <= y for x, y in zip(v1, v2))

def vector_add(v1, v2):
    return [x + y for x, y in zip(v1, v2)]

def vector_sub(v1, v2):
    return [x - y for x, y in zip(v1, v2)]

def banker_algorithm(Max, Need, Available, Allocated, Request):
    new_Max = [row[:] for row in Max]
    new_Need = [row[:] for row in Need]
    new_Available = Available[:]
    new_Allocated = [row[:] for row in Allocated]

    pid, req_vector = Request
    n = len(Max)
    m = len(Available)

    if not vector_less_equal(req_vector, new_Need[pid]):
        print(f"错误：进程{pid}请求的资源超过其需求")
        return False, new_Max, new_Need, new_Available, new_Allocated

    if not vector_less_equal(req_vector, new_Available):
        print(f"错误：进程{pid}请求的资源超过可用资源")
        return False, new_Max, new_Need, new_Available, new_Allocated

    new_Available = vector_sub(new_Available, req_vector)
    new_Allocated[pid] = vector_add(new_Allocated[pid], req_vector)
    new_Need[pid] = vector_sub(new_Need[pid], req_vector)

    work = new_Available[:]
    finish = [False] * n

    found = True
    while found:
        found = False
        for i in range(n):
            if not finish[i] and vector_less_equal(new_Need[i], work):
                # 找到可执行的进程
                work = vector_add(work, new_Allocated[i])
                finish[i] = True
                found = True  # 需要重新扫描所有进程
    if all(finish):
        print(f"安全：进程{pid}的请求被批准")
        return True, new_Max, new_Need, new_Available, new_Allocated
    else:
        print(f"不安全：进程{pid}的请求被拒绝")
        # 恢复原始矩阵
        return False, Max, Need, Available, Allocated

# 示例数据
Max = [
    [7, 5, 3],  # P0
    [3, 2, 2],  # P1
    [9, 0, 2],  # P2
    [2, 2, 2],  # P3
    [4, 3, 3]   # P4
]

Allocated = [
    [0, 1, 0],  # P0
    [2, 0, 0],  # P1
    [3, 0, 2],  # P2
    [2, 1, 1],  # P3
    [0, 0, 2]   # P4
]

Need = [
    [7, 4, 3],  # P0
    [1, 2, 2],  # P1
    [6, 0, 0],  # P2
    [0, 1, 1],  # P3
    [4, 3, 1]   # P4
]

Available = [3, 3, 2]  # 可用资源

# 测试请求: 进程1请求[1, 0, 2]
Request = (1, [1, 0, 2])

# 执行银行家算法
result = banker_algorithm(Max, Need, Available, Allocated, Request)
print("\n分配结果:", result[0])
print("更新后的矩阵:")
print("Max:", result[1])
print("Need:", result[2])
print("Available:", result[3])
print("Allocated:", result[4])
