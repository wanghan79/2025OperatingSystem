def banker_algorithm(Max, Allocation, Available, Request, process_id):
    n = len(Max)        
    m = len(Max[0])    
    Need = [[Max[i][j] - Allocation[i][j] for j in range(m)] for i in range(n)]

    # 检查Request是否小于等于Need
    if any(Request[j] > Need[process_id][j] for j in range(m)):
        return False, Max, Need, Available, Allocation, "Error: Request > Need"

    # 检查Request是否小于等于Available
    if any(Request[j] > Available[j] for j in range(m)):
        return False, Max, Need, Available, Allocation, "Error: Request > Available"

    # 分配资源
    Available_tmp = Available[:]
    Allocation_tmp = [row[:] for row in Allocation]
    Need_tmp = [row[:] for row in Need]

    for j in range(m):
        Available_tmp[j] -= Request[j]
        Allocation_tmp[process_id][j] += Request[j]
        Need_tmp[process_id][j] -= Request[j]

    #  安全性检查
    Finish = [False] * n
    Work = Available_tmp[:]
    safe_sequence = []

    while True:
        found = False
        for i in range(n):
            if not Finish[i] and all(Need_tmp[i][j] <= Work[j] for j in range(m)):
                for j in range(m):
                    Work[j] += Allocation_tmp[i][j]
                Finish[i] = True
                safe_sequence.append(i)
                found = True
        if not found:
            break

    if all(Finish):
        return True, Max, Need_tmp, Available_tmp, Allocation_tmp, f"Safe sequence: {safe_sequence}"
    else:
        return False, Max, Need, Available, Allocation, "Unsafe: request denied"

# 调用
Max = [[7,5,3], [3,2,2], [9,0,2], [2,2,2], [4,3,3]]
Allocation = [[0,1,0], [2,0,0], [3,0,2], [2,1,1], [0,0,2]]
Available = [3,3,2]
Request = [1,0,2]
process_id = 1

result = banker_algorithm(Max, Allocation, Available, Request, process_id)
for item in result:
    print(item)
