def banker_algorithm(processes, resources, Max, Allocated, Available, Request_p, Request):
    """
    银行家算法实现
    
    参数:
        processes: 进程数量
        resources: 资源种类数量
        Max: 最大需求矩阵 (processes × resources)
        Allocated: 已分配矩阵 (processes × resources)
        Available: 可用资源向量 (resources)
        Request_p: 请求资源的进程索引
        Request: 请求资源向量 (resources)
    
    返回:
        bool: 是否能够安全分配
        str: 说明信息
        dict: 分配后的矩阵 (如果分配成功)
    """
    # 1. 检查请求是否小于等于Need
    Need = [[Max[i][j] - Allocated[i][j] for j in range(resources)] for i in range(processes)]
    
    for j in range(resources):
        if Request[j] > Need[Request_p][j]:
            return False, f"错误：进程{Request_p}请求的资源超过其最大需求", None
    
    # 2. 检查请求是否小于等于Available
    for j in range(resources):
        if Request[j] > Available[j]:
            return False, f"错误：进程{Request_p}请求的资源超过系统可用资源", None
    
    # 3. 尝试分配资源
    # 保存原始状态以便回滚
    old_Available = Available.copy()
    old_Allocated = [row.copy() for row in Allocated]
    old_Need = [row.copy() for row in Need]
    
    # 模拟分配
    for j in range(resources):
        Available[j] -= Request[j]
        Allocated[Request_p][j] += Request[j]
        Need[Request_p][j] -= Request[j]
    
    # 4. 安全检查
    Work = Available.copy()
    Finish = [False] * processes
    safe_sequence = []
    
    while True:
        # 找到一个满足条件的进程
        found = False
        for i in range(processes):
            if not Finish[i]:
                # 检查Need[i] <= Work
                can_allocate = True
                for j in range(resources):
                    if Need[i][j] > Work[j]:
                        can_allocate = False
                        break
                
                if can_allocate:
                    # 模拟执行完成，释放资源
                    for j in range(resources):
                        Work[j] += Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True
        
        if not found:
            break
    
    # 检查是否所有进程都完成
    if all(Finish):
        # 分配成功
        result = {
            'Max': Max,
            'Allocated': Allocated,
            'Need': Need,
            'Available': Available,
            'SafeSequence': safe_sequence
        }
        return True, f"分配成功，安全序列: {safe_sequence}", result
    else:
        # 分配不安全，回滚
        Available = old_Available
        Allocated = old_Allocated
        Need = old_Need
        return False, "分配失败：系统将进入不安全状态", None


# 示例用法
if __name__ == "__main__":
    # 示例数据
    processes = 5
    resources = 3
    
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
    
    Available = [3, 3, 2]
    
    # 进程1请求资源 (1, 0, 2)
    Request_p = 1
    Request = [1, 0, 2]
    
    # 运行银行家算法
    success, message, result = banker_algorithm(processes, resources, Max, Allocated, Available, Request_p, Request)
    
    print(message)
    if success:
        print("\n分配后的矩阵:")
        print("Max矩阵:")
        for row in result['Max']:
            print(row)
        
        print("\nAllocated矩阵:")
        for row in result['Allocated']:
            print(row)
        
        print("\nNeed矩阵:")
        for row in result['Need']:
            print(row)
        
        print("\nAvailable向量:")
        print(result['Available'])
        
        print("\n安全序列:")
        print(result['SafeSequence'])