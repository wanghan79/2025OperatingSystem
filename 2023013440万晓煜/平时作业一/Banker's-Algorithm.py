import numpy as np

def safe(Available, Need, Allocation):
    """
    安全检测算法：检查系统是否处于安全状态。
    :param Available: 可用资源向量
    :param Need: 最大需求矩阵
    :param Allocation: 分配矩阵
    :return: 如果系统安全，返回 (True, 安全序列)；否则返回 (False, [])。
    """
    processes = Allocation.shape[0]
    work = Available.copy() 
    finish = np.zeros(processes, dtype=bool) 
    safearray = [] 

    while True:
        found = False 
        for i in range(processes):
            if not finish[i] and np.all(Need[i] - Allocation[i] <= work):
                work += Allocation[i] 
                finish[i] = True 
                safearray.append(i)  
                found = True 
        if not found:
            break

    if np.all(finish):
        return True, safearray
    else:
        return False, []

def bankers(Max, Allocation, Available, Request, process_id):
    """
    银行家算法：处理进程的资源请求，封装为函数
    :param Max: 最大需求矩阵
    :param Allocation: 分配矩阵
    :param Available: 可用资源向量
    :param Request: 请求向量
    :param process_id: 请求资源的进程ID
    :return: 如果请求可以，返回 (True, Max, Need, Available, Allocation, 安全序列)；
             否则返回 (False, Max, Need, Available, Allocation, 错误信息)
    """
    Max = Max.copy()
    Allocation = Allocation.copy()
    Available = Available.copy()
    Request = Request.copy()

    Need = Max - Allocation  
    if not np.all(Request <= Need[process_id]):
        return False, Max, Need, Available, Allocation, "超过了其最大需求"
    if not np.all(Request <= Available):
        return False, Max, Need, Available, Allocation, "资源不足"
    Available -= Request 
    Allocation[process_id] += Request 
    Need[process_id] -= Request  
    #在这里调用了安全算法
    safe_state, safearray = safe(Available, Need, Allocation)
    if safe_state:
        return True, Max, Need, Available, Allocation, safearray  
    else:
        Available += Request
        Allocation[process_id] -= Request
        Need[process_id] += Request
        return False, Max, Need, Available, Allocation, "系统不安全状态"

# 样例
if __name__ == "__main__":
    Available = np.array([3, 3, 2])
    max_demand = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    Allocation = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    # 进程1
    request = np.array([1, 1, 2])
    process_id = 1  # 进程ID
    # 使用银行家算法
    result, max_after, Need_after, Available_after, Allocation_after, msg = bankers(
        max_demand, Allocation, Available, request, process_id)

    if result:
        print("可以分配资源，安全序列是:", msg)
    else:
        print("不能分配资源，因为", msg)

    print("\n分配后的 Max 矩阵:")
    print(max_after)
    print("\n分配后的 Need 矩阵:")
    print(Need_after)
    print("\n分配后的 Available 向量:")
    print(Available_after)
    print("\n分配后的 Allocation 矩阵:")
    print(Allocation_after)
 