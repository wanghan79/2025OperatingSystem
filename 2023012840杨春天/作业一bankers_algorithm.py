import numpy as np

def bankers_algorithm(Max, Need, Available, Allocated, Request, pid):
    """
    实现银行家算法，判断系统是否能安全分配资源
    
    参数:
    Max (np.ndarray): 最大需求矩阵，形状为 (n_processes, n_resources)
    Need (np.ndarray): 需求矩阵，形状为 (n_processes, n_resources)
    Available (np.ndarray): 可用资源向量，形状为 (n_resources,)
    Allocated (np.ndarray): 已分配资源矩阵，形状为 (n_processes, n_resources)
    Request (np.ndarray): 请求资源向量，形状为 (n_resources,)
    pid (int): 请求进程的 ID
    
    返回:
    tuple: (是否可以分配, Available, Max, Allocated, Need)
    """
    n_processes, n_resources = Max.shape
    
    # 步骤 1: 检查请求是否超过需求
    if np.any(Request > Need[pid]):
        print(f"错误: 进程 {pid} 的请求超过了其最大需求")
        return False, Available, Max, Allocated, Need
    
    # 步骤 2: 检查请求是否超过可用资源
    if np.any(Request > Available):
        print(f"错误: 进程 {pid} 的请求超过了当前可用资源")
        return False, Available, Max, Allocated, Need
    
    # 步骤 3: 尝试分配资源
    Available_temp = Available - Request
    Allocated_temp = Allocated.copy()
    Allocated_temp[pid] += Request
    Need_temp = Need.copy()
    Need_temp[pid] -= Request
    
    # 步骤 4: 执行安全性检查
    safe, safe_sequence = is_safe_state(Available_temp, Max, Need_temp, Allocated_temp)
    
    if safe:
        print(f"资源分配成功，系统处于安全状态，安全序列为: {safe_sequence}")
        return True, Available_temp, Max, Allocated_temp, Need_temp
    else:
        print(f"资源分配失败，系统将进入不安全状态")
        return False, Available, Max, Allocated, Need

def is_safe_state(Available, Max, Need, Allocated):
    """
    检查系统是否处于安全状态
    
    参数:
    Available (np.ndarray): 可用资源向量
    Max (np.ndarray): 最大需求矩阵
    Need (np.ndarray): 需求矩阵
    Allocated (np.ndarray): 已分配资源矩阵
    
    返回:
    tuple: (是否安全, 安全序列)
    """
    n_processes, n_resources = Max.shape
    Work = Available.copy()
    Finish = np.zeros(n_processes, dtype=bool)
    SafeSequence = []
    
    while True:
        found = False
        for i in range(n_processes):
            if not Finish[i] and np.all(Need[i] <= Work):
                Work += Allocated[i]
                Finish[i] = True
                SafeSequence.append(i)
                found = True
                break
        if not found:
            break
    
    return np.all(Finish), SafeSequence

# 示例使用
if __name__ == "__main__":
    # 初始化矩阵
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
    
    # 模拟进程 1 请求资源 [1, 0, 2]
    Request = np.array([1, 0, 2])
    pid = 1
    
    can_allocate, Available_new, Max_new, Allocated_new, Need_new = bankers_algorithm(
        Max, Need, Available, Allocated, Request, pid
    )
    
    if can_allocate:
        print("分配后的矩阵:")
        print("Available:", Available_new)
        print("Max:\n", Max_new)
        print("Allocated:\n", Allocated_new)
        print("Need:\n", Need_new)    