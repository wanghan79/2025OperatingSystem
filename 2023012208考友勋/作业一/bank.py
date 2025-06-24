import numpy as np

def banker_algorithm(Max, Need, Available, Allocated, Request, pid):
    """
    银行家算法实现，用于判断系统是否能安全分配资源
    
    参数:
        Max: 最大需求矩阵，二维数组，shape为(n_processes, n_resources)
        Need: 需求矩阵，二维数组
        Available: 可用资源向量，一维数组
        Allocated: 已分配资源矩阵，二维数组
        Request: 资源请求向量，一维数组
        pid: 发出请求的进程ID
        
    返回:
        元组 (can_allocate, Updated_Max, Updated_Need, Updated_Available, Updated_Allocated)
        can_allocate: 是否可以分配资源
    """
    n_processes, n_resources = Max.shape
    
    # 检查请求是否超过需求
    if np.any(Request > Need[pid]):
        print(f"错误: 进程 {pid} 的请求超过了其最大需求")
        return False, Max, Need, Available, Allocated
    
    # 检查请求是否超过可用资源
    if np.any(Request > Available):
        print(f"错误: 进程 {pid} 的请求超过了可用资源")
        return False, Max, Need, Available, Allocated
    
    # 尝试分配资源
    temp_available = Available - Request
    temp_allocated = Allocated.copy()
    temp_allocated[pid] += Request
    temp_need = Need.copy()
    temp_need[pid] -= Request
    
    # 安全性检查
    if is_safe_state(temp_available, temp_need, temp_allocated):
        print(f"资源分配安全，已分配给进程 {pid}")
        return True, Max, temp_need, temp_available, temp_allocated
    else:
        print(f"资源分配不安全，请求被拒绝")
        return False, Max, Need, Available, Allocated

def is_safe_state(Available, Need, Allocated):
    """检查系统是否处于安全状态"""
    n_processes, n_resources = Need.shape
    Work = Available.copy()
    Finish = np.zeros(n_processes, dtype=bool)
    SafeSequence = []
    
    # 寻找安全序列
    while not np.all(Finish):
        found = False
        for i in range(n_processes):
            if not Finish[i] and np.all(Need[i] <= Work):
                # 分配资源给进程i并回收
                Work += Allocated[i]
                Finish[i] = True
                SafeSequence.append(i)
                found = True
                break
        if not found:
            break  # 找不到满足条件的进程，退出循环
    
    if np.all(Finish):
        print(f"安全序列: {SafeSequence}")
        return True
    else:
        print("未找到安全序列")
        return False

# 示例使用
if __name__ == "__main__":
    # 示例数据
    Max = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    
    Allocated = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    
    Need = Max - Allocated
    Available = np.array([3, 3, 2])
    
    # 进程1请求资源 (1, 0, 2)
    Request = np.array([1, 0, 2])
    pid = 1
    
    # 执行银行家算法
    can_allocate, Max, Need, Available, Allocated = banker_algorithm(
        Max, Need, Available, Allocated, Request, pid
    )
    
    # 输出结果
    if can_allocate:
        print("\n分配后的矩阵:")
        print("Max:")
        print(Max)
        print("\nNeed:")
        print(Need)
        print("\nAvailable:")
        print(Available)
        print("\nAllocated:")
        print(Allocated)
