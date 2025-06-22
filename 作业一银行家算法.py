def banker_algorithm(Max, Need, Available, Allocated, Request):
    for i in range(len(Request)):
        if Request[i] > Need[0][i]:
            return False, Max, Need, Available, Allocated, "请求的资源超过了最大需求"

    for i in range(len(Request)):
        if Request[i] > Available[i]:
            return False, Max, Need, Available, Allocated, "请求的资源超过了可用资源"

    Available_temp = [Available[i] - Request[i] for i in range(len(Available))]
    Allocated_temp = [Allocated[0][i] + Request[i] for i in range(len(Request))]
    Need_temp = [Need[0][i] - Request[i] for i in range(len(Request))]

    Work = Available_temp.copy()
    Finish = [False] * len(Max)
    Sequence = []

    while True:
        found = False
        for i in range(len(Max)):
            if not Finish[i]:
                if all(Need_temp[i][j] <= Work[j] for j in range(len(Work))):
                    Work = [Work[j] + Allocated_temp[i][j] for j in range(len(Work))]
                    Finish[i] = True
                    Sequence.append(i)
                    found = True
                    break
        if not found:
            break
    if all(Finish):
        return True, Max, [Need_temp], Available_temp, [Allocated_temp], "可以分配，系统处于安全状态", Sequence
    else:
        return False, Max, Need, Available, Allocated, "不能分配，系统不处于安全状态"

Max = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]

Need = [
    [0, 0, 0],
    [2, 0, 0],
    [3, 0, 2],
    [1, 1, 1],
    [0, 0, 2]
]

Available = [10, 5, 7]
Allocated = [
    [0, 1, 0],
    [2, 0, 0   ],
 [3, 0, 2],
    [2, 1, 1],
    [0, 0, 1]
]

Request = [1, 0, 2]

can_allocate, Max, Need, Available, Allocated, message, sequence = banker_algorithm(Max, Need, Available, Allocated, Request)

print("是否可以分配:", can_allocate)
print("分配后的 Max 矩阵:", Max)
print("分配后的 Need 矩阵:", Need)
print("分配后的 Available 向量:", Available)
print("分配后的 Allocated 矩阵:", Allocated)
print("消息:", message)
if can_allocate:
    print("安全序列:", sequence)