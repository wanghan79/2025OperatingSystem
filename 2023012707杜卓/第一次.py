import numpy as np

def bankers_algorithm(Max, Need, Available, Allocated, Request, process_id):
    """
    银行家算法模拟函数
    
    参数:
    Max (np.ndarray): 最大需求矩阵，形状为 (n_processes, n_resources)
    Need (np.ndarray): 还需要的资源矩阵，形状为 (n_processes, n_resources)
    Available (np.ndarray): 可用资源向量，形状为 (n_resources,)
    Allocated (np.ndarray): 已分配资源矩阵，形状为 (n_processes, n_resources)
    Request (np.ndarray): 请求的资源向量，形状为 (n_resources,)
    process_id (int): 请求资源的进程ID
    
    返回:
    tuple: (是否可以分配, 分配后的Available, 分配后的Allocated, 分配后的Need, 分配后的Max)
    """
    n_processes, n_resources = Max.shape
    
    # 检查请求是否超过需求
    if np.any(Request > Need[process_id]):
        return False, Available, Allocated, Need, Max
    
    # 检查请求是否超过可用资源
    if np.any(Request > Available):
        return False, Available, Allocated, Need, Max
    
    # 尝试分配资源
    Available_temp = Available - Request
    Allocated_temp = Allocated.copy()
    Allocated_temp[process_id] += Request
    Need_temp = Need.copy()
    Need_temp[process_id] -= Request
    
    # 安全性检查
    def is_safe(state_Available, state_Allocated, state_Need):
        Work = state_Available.copy()
        Finish = np.zeros(n_processes, dtype=bool)
        safe_sequence = []
        
        while True:
            found = False
            for i in range(n_processes):
                if not Finish[i] and np.all(state_Need[i] <= Work):
                    Work += state_Allocated[i]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
            if not found:
                break
        
        return np.all(Finish), safe_sequence
    
    safe, safe_sequence = is_safe(Available_temp, Allocated_temp, Need_temp)
    
    if safe:
        return True, Available_temp, Allocated_temp, Need_temp, Max
    else:
        return False, Available, Allocated, Need, Max

# 交互式输入
def main():
    n_processes = int(input("请输入进程数量: "))
    n_resources = int(input("请输入资源种类数量: "))
    
    print("\n=== 输入最大需求矩阵 Max ===")
    Max = np.zeros((n_processes, n_resources), dtype=int)
    for i in range(n_processes):
        Max[i] = list(map(int, input(f"请输入进程 {i} 的最大需求 ({n_resources} 个整数，用空格分隔): ").split()))
    
    print("\n=== 输入已分配资源矩阵 Allocated ===")
    Allocated = np.zeros((n_processes, n_resources), dtype=int)
    for i in range(n_processes):
        Allocated[i] = list(map(int, input(f"请输入进程 {i} 的已分配资源 ({n_resources} 个整数，用空格分隔): ").split()))
    
    Need = Max - Allocated
    
    print("\n=== 输入可用资源向量 Available ===")
    Available = np.array(list(map(int, input(f"请输入可用资源 ({n_resources} 个整数，用空格分隔): ").split())))
    
    print("\n=== 输入资源请求 ===")
    process_id = int(input("请输入请求资源的进程ID (0-{}): ".format(n_processes - 1)))
    Request = np.array(list(map(int, input(f"请输入请求的资源 ({n_resources} 个整数，用空格分隔): ").split())))
    
    can_allocate, new_Available, new_Allocated, new_Need, new_Max = bankers_algorithm(
        Max, Need, Available, Allocated, Request, process_id
    )
    
    print(f"\n是否可以分配: {can_allocate}")
    if can_allocate:
        print("\n分配后的矩阵:")
        print("可用资源 (Available):")
        print(new_Available)
        print("\n已分配资源 (Allocated):")
        print(new_Allocated)
        print("\n还需要的资源 (Need):")
        print(new_Need)
        print("\n最大需求 (Max):")
        print(new_Max)

if __name__ == "__main__":
    main() 