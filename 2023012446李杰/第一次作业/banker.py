import numpy as np

def bankers_algorithm(Max, Need, Available, Allocated, Request, pid):
    """
    银行家算法实现
    参数:
    - Max: 最大需求矩阵 (n×m)
    - Need: 需求矩阵 (n×m)
    - Available: 可用资源向量 (1×m)
    - Allocated: 已分配资源矩阵 (n×m)
    - Request: 请求资源向量 (1×m)
    - pid: 发出请求的进程编号 (0-based)

    返回:
    - 分配是否成功（True/False）
    - 若成功，返回更新后的 (Max, Need, Available, Allocated)
    """
    n, m = len(Max), len(Max[0])
    
    # 转为 numpy 数组以便于处理
    Max = np.array(Max)
    Need = np.array(Need)
    Available = np.array(Available)
    Allocated = np.array(Allocated)
    Request = np.array(Request)

    # Step 1: 检查 Request <= Need
    if np.any(Request > Need[pid]):
        print(f"Error: 请求超过最大需求 Request > Need[{pid}]")
        return False, Max, Need, Available, Allocated

    # Step 2: 检查 Request <= Available
    if np.any(Request > Available):
        print("当前资源不足，进程需等待。")
        return False, Max, Need, Available, Allocated

    # Step 3: 试分配资源
    Available_temp = Available - Request
    Allocated_temp = Allocated.copy()
    Allocated_temp[pid] += Request
    Need_temp = Need.copy()
    Need_temp[pid] -= Request

    # Step 4: 安全性检查
    Finish = [False] * n
    Work = Available_temp.copy()

    while True:
        found = False
        for i in range(n):
            if not Finish[i] and np.all(Need_temp[i] <= Work):
                Work += Allocated_temp[i]
                Finish[i] = True
                found = True
        if not found:
            break

    if all(Finish):
        print("请求可以满足，系统处于安全状态。")
        return True, Max.tolist(), Need_temp.tolist(), Available_temp.tolist(), Allocated_temp.tolist()
    else:
        print("请求后系统不安全，拒绝分配。")
        return False, Max.tolist(), Need.tolist(), Available.tolist(), Allocated.tolist()
