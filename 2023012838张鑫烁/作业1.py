import numpy as np

def banker_algorithm(Max, Need, Available, Allocated, Request, process_id):
    """
    银行家算法实现
    
    参数:
    Max: 最大需求矩阵 (n_processes x n_resources)
    Need: 需求矩阵 (n_processes x n_resources)
    Available: 可用资源向量 (n_resources,)
    Allocated: 已分配矩阵 (n_processes x n_resources)
    Request: 请求资源向量 (n_resources,)
    process_id: 发出请求的进程ID
    
    返回:
    can_allocate: 布尔值，表示是否可以分配
    Max_new: 分配后的Max矩阵
    Need_new: 分配后的Need矩阵
    Available_new: 分配后的Available向量
    Allocated_new: 分配后的Allocated矩阵
    """
    
    # 转换为numpy数组以便计算
    Max = np.array(Max)
    Need = np.array(Need)
    Available = np.array(Available)
    Allocated = np.array(Allocated)
    Request = np.array(Request)
    
    n_processes = Max.shape[0]
    n_resources = Max.shape[1]
    
    # 验证Need矩阵是否正确（Need = Max - Allocated）
    if not np.array_equal(Need, Max - Allocated):
        print("警告：提供的Need矩阵与Max-Allocated不一致")
    
    # 步骤1: 检查请求是否合法
    if np.any(Request > Need[process_id]):
        print(f"错误：进程 {process_id} 的请求超过了其最大需求")
        return False, Max.tolist(), Need.tolist(), Available.tolist(), Allocated.tolist()
    
    if np.any(Request > Available):
        print(f"错误：请求的资源超过了当前可用资源")
        return False, Max.tolist(), Need.tolist(), Available.tolist(), Allocated.tolist()
    
    # 步骤2: 尝试分配资源
    # 创建副本进行临时分配
    Available_temp = Available.copy()
    Allocated_temp = Allocated.copy()
    Need_temp = Need.copy()
    
    # 执行临时分配
    Available_temp = Available_temp - Request
    Allocated_temp[process_id] = Allocated_temp[process_id] + Request
    Need_temp[process_id] = Need_temp[process_id] - Request
    
    # 步骤3: 执行安全性检查
    is_safe, safe_sequence = safety_check(Available_temp, Need_temp, Allocated_temp)
    
    if is_safe:
        print(f"请求可以被安全分配")
        print(f"安全序列: {safe_sequence}")
        # 返回更新后的矩阵
        return True, Max.tolist(), Need_temp.tolist(), Available_temp.tolist(), Allocated_temp.tolist()
    else:
        print(f"请求不能被安全分配，系统将进入不安全状态")
        # 返回原始矩阵
        return False, Max.tolist(), Need.tolist(), Available.tolist(), Allocated.tolist()

def safety_check(Available, Need, Allocated):
    """
    安全性检查算法
    
    参数:
    Available: 可用资源向量
    Need: 需求矩阵
    Allocated: 已分配矩阵
    
    返回:
    is_safe: 布尔值，表示系统是否处于安全状态
    safe_sequence: 安全序列（如果存在）
    """
    n_processes = Need.shape[0]
    n_resources = Need.shape[1]
    
    # 初始化
    Work = Available.copy()
    Finish = [False] * n_processes
    safe_sequence = []
    
    # 寻找安全序列
    while len(safe_sequence) < n_processes:
        found = False
        
        for i in range(n_processes):
            if not Finish[i] and np.all(Need[i] <= Work):
                # 找到一个可以完成的进程
                Work = Work + Allocated[i]
                Finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        
        if not found:
            # 没有找到可以完成的进程，系统不安全
            return False, []
    
    return True, safe_sequence

def print_result(can_allocate, Max, Need, Available, Allocated):
    """
    打印结果
    """
    print("\n" + "="*50)
    if can_allocate:
        print("分配成功！分配后的系统状态:")
    else:
        print("分配失败！当前系统状态:")
    print("="*50)
    
    print("\nMax矩阵:")
    for row in Max:
        print(" ".join(f"{val:3d}" for val in row))
    
    print("\nNeed矩阵:")
    for row in Need:
        print(" ".join(f"{val:3d}" for val in row))
    
    print("\nAvailable向量:")
    print(" ".join(f"{val:3d}" for val in Available))
    
    print("\nAllocated矩阵:")
    for row in Allocated:
        print(" ".join(f"{val:3d}" for val in row))

# 示例使用
def example_usage():
    """
    演示银行家算法的使用
    """
    # 定义系统状态
    # 5个进程，3种资源类型
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    
    Allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    
    # 计算Need矩阵
    Need = []
    for i in range(len(Max)):
        need_row = []
        for j in range(len(Max[0])):
            need_row.append(Max[i][j] - Allocated[i][j])
        Need.append(need_row)
    
    Available = [3, 3, 2]
    
    # 进程1请求资源[1, 0, 2]
    Request = [1, 0, 2]
    process_id = 1
    
    print("银行家算法演示")
    print(f"\n进程 {process_id} 请求资源: {Request}")
    
    # 执行银行家算法
    can_allocate, Max_new, Need_new, Available_new, Allocated_new = banker_algorithm(
        Max, Need, Available, Allocated, Request, process_id
    )
    
    # 打印结果
    print_result(can_allocate, Max_new, Need_new, Available_new, Allocated_new)

# 简化版本的调用示例
def simple_example():
    """
    更简单的调用示例
    """
    # 系统状态
    Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    Allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
    Available = [3, 3, 2]
    Request = [1, 0, 2]
    process_id = 1
    
    # 调用银行家算法
    result = banker_algorithm(Max, Need, Available, Allocated, Request, process_id)
    
    # 解包结果
    can_allocate, Max_new, Need_new, Available_new, Allocated_new = result
    
    print(f"\n是否可以分配: {can_allocate}")
    if can_allocate:
        print("分配后的矩阵已更新")

if __name__ == "__main__":
    example_usage()
    print("\n" + "="*70 + "\n")
    simple_example()