def banker_algorithm(Max, Allocated, Need, Available, Request, process_id):
    """
    银行家算法实现
    参数:
        Max: 最大需求矩阵 (n x m)
        Allocated: 已分配矩阵 (n x m)
        Need: 需求矩阵 (n x m)
        Available: 可用资源向量 (m)
        Request: 资源请求向量 (m)
        process_id: 请求资源的进程ID
    返回:
        bool: 是否安全
        str: 说明信息
        (更新后的Max, Allocated, Need, Available) 或原始矩阵
    """
    import numpy as np
    n, m = len(Max), len(Available)
    
    # Step 1: 检查请求是否小于等于需求
    if not all(Request[i] <= Need[process_id][i] for i in range(m)):
        return False, "Error: Request exceeds need", (Max, Allocated, Need, Available)
    
    # Step 2: 检查请求是否小于等于可用资源
    if not all(Request[i] <= Available[i] for i in range(m)):
        return False, "Request exceeds available resources", (Max, Allocated, Need, Available)
    
    # 尝试分配资源
    new_Available = Available - Request
    new_Allocated = Allocated.copy()
    new_Need = Need.copy()
    new_Allocated[process_id] += Request
    new_Need[process_id] -= Request
    
    # Step 3: 安全性检查
    work = new_Available.copy()
    finish = [False] * n
    safe_sequence = []
    
    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(new_Need[i][j] <= work[j] for j in range(m)):
                work += new_Allocated[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        
        if not found:
            break
    
    # 判断系统是否安全
    if all(finish):
        return True, f"Safe state! Sequence: {safe_sequence}", (Max, new_Allocated, new_Need, new_Available)
    else:
        return False, "Unsafe state! Reverting allocation", (Max, Allocated, Need, Available)

# 使用示例
if __name__ == "__main__":
    import numpy as np
    # 示例数据
    Max = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
    Allocated = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
    Need = Max - Allocated
    Available = np.array([3, 3, 2])
    Request = np.array([1, 0, 2])
    process_id = 1
    
    safe, msg, (new_Max, new_Allocated, new_Need, new_Available) = banker_algorithm(
        Max, Allocated, Need, Available, Request, process_id
    )
    
    print(f"安全状态: {safe}\n{msg}")
    print("\n更新后的矩阵:")
    print("Max:\n", new_Max)
    print("Allocated:\n", new_Allocated)
    print("Need:\n", new_Need)
    print("Available:\n", new_Available)