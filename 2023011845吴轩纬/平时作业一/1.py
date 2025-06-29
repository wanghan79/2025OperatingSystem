import copy

def isSafe(Available, Need, Allocation):
    n, m = len(Need), len(Available)
    finished = [False] * n
    Work = Available[:]
    safe_sequence = []
    
    while True:
        found = False
        for i in range(n):
            if not finished[i] and all(Need[i][j] <= Work[j] for j in range(m)):
                Work = [Work[j] + Allocation[i][j] for j in range(m)]
                finished[i] = True
                safe_sequence.append(i)
                found = True
        if not found:
            break
    
    is_safe = all(finished)
    return is_safe, safe_sequence if is_safe else []


def banker_algorithm(Max, Need, Available, Allocation, Request, pid):
    n, m = len(Max), len(Available)
    
    if any(Request[j] > Need[pid][j] for j in range(m)):
        return {
            "state": False,
            "info": "资源请求超过进程最大需求"
        }
    
    if any(Request[j] > Available[j] for j in range(m)):
        return {
            "state": False,
            "info": "资源不足，进程需要等待"
        }

    AvailableNew = [Available[j] - Request[j] for j in range(m)]
    AllocationNew = copy.deepcopy(Allocation)
    AllocationNew[pid] = [Allocation[pid][j] + Request[j] for j in range(m)]
    NeedNew = copy.deepcopy(Need)
    NeedNew[pid] = [Need[pid][j] - Request[j] for j in range(m)]
    
    # 安全性检查
    is_safe, safe_sequence = isSafe(AvailableNew, NeedNew, AllocationNew)
    if is_safe:
        return {
            "state": True,
            "info": {
                "Available": AvailableNew,
                "Allocation": AllocationNew,
                "Need": NeedNew,
                "Max": Max,  
                "SafeSequence": safe_sequence
            }
        }
    else:
        return {
            "state": False,
            "info": "请求后系统不安全，拒绝分配"
        }


def main(Max, Need, Available, Allocation, Request, pid):
    print("当前系统状态:")
    print("Available:", Available)
    print("Allocation:")
    for row in Allocation:
        print(" ", row)
    print("Need:")
    for row in Need:
        print(" ", row)
    print(f"进程 P{pid} 请求资源: {Request}")
    
    res = banker_algorithm(Max, Need, Available, Allocation, Request, pid)
    state, result = res["state"], res["info"]

    print("\n分配结果:")
    if state:
        print("请求可以被安全满足")
        print("分配后 Available:", result["Available"])
        print("分配后 Allocation:")
        for row in result["Allocation"]:
            print(" ", row)
        print("分配后 Need:")
        for row in result["Need"]:
            print(" ", row)
        print("安全序列:", ["P"+str(i) for i in result["SafeSequence"]])
    else:
        print("请求被拒绝：", result)


if __name__ == '__main__':

    Available = [3, 3, 2]

    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    Allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    Need = [[Max[i][j] - Allocation[i][j] for j in range(3)] for i in range(5)]

    Request = [1, 0, 2]  
    pid = 1  


    main(Max, Need, Available, Allocation, Request, pid)

    print("\n" + "="*50 + "\n")
    
    Available = [1, 0, 0]

    Max = [
        [2, 2, 2], 
        [3, 2, 2],  
        [2, 2, 2],  
    ]

    Allocation = [
        [1, 0, 0],
        [1, 1, 0],
        [1, 0, 1]
    ]

    Need = [[Max[i][j] - Allocation[i][j] for j in range(3)] for i in range(3)]

    Request = [1, 0, 0]  
    pid = 1

    main(Max, Need, Available, Allocation, Request, pid)


