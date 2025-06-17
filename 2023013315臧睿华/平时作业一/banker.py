# coding:utf-8
"""
  Author:  臧睿华
  Purpose: 银行家算法实现
  Created: 5/6/2025
"""
def banker_algorithm(processes, resources, Max, Allocated, Available, Request, process_id):
    """
    银行家算法实现
    
    参数:
        processes: 进程数量
        resources: 资源种类数量
        Max: 最大需求矩阵 (processes x resources)
        Allocated: 已分配矩阵 (processes x resources)
        Available: 可用资源向量 (resources)
        Request: 请求资源向量 (resources)
        process_id: 请求资源的进程ID
        
    返回:
        (是否能分配, 新的Allocated, 新的Need, 新的Available)
    """
    # 1. 检查请求是否小于等于Need
    Need = [[Max[i][j] - Allocated[i][j] for j in range(resources)] for i in range(processes)]
    
    for j in range(resources):
        if Request[j] > Need[process_id][j]:
            return (False, "错误：请求的资源超过了声明的最大需求", Allocated, Need, Available)
    
    # 2. 检查请求是否小于等于Available
    for j in range(resources):
        if Request[j] > Available[j]:
            return (False, "错误：资源不足，请等待", Allocated, Need, Available)
    
    # 3. 尝试分配资源
    new_Allocated = [row[:] for row in Allocated]
    new_Need = [row[:] for row in Need]
    new_Available = Available[:]
    
    for j in range(resources):
        new_Allocated[process_id][j] += Request[j]
        new_Need[process_id][j] -= Request[j]
        new_Available[j] -= Request[j]
    
    # 4. 检查安全性
    Work = new_Available[:]
    Finish = [False] * processes
    
    # 寻找可以完成的进程
    safe_sequence = []
    count = 0
    
    while count < processes:
        found = False
        for i in range(processes):
            if not Finish[i]:
                # 检查该进程的所有资源需求是否小于等于Work
                can_execute = True
                for j in range(resources):
                    if new_Need[i][j] > Work[j]:
                        can_execute = False
                        break
                
                if can_execute:
                    # 执行该进程并释放资源
                    for j in range(resources):
                        Work[j] += new_Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    count += 1
                    found = True
        
        if not found:
            break  # 没有找到可以执行的进程
    
    # 如果所有进程都能完成，则是安全状态
    if all(Finish):
        return (True, "可以安全分配，安全序列: " + str(safe_sequence), new_Allocated, new_Need, new_Available)
    else:
        # 回滚分配
        return (False, "分配会导致系统进入不安全状态", Allocated, Need, Available)


# 示例使用
if __name__ == "__main__":
    # 示例数据
    processes = 5
    resources = 3
    
    # 最大需求矩阵
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    
    # 已分配矩阵
    Allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    
    # 可用资源
    Available = [3, 3, 2]
    
    # 进程1请求资源
    Request = [1, 0, 2]
    process_id = 1
    
    # 运行银行家算法
    can_allocate, message, new_Allocated, new_Need, new_Available = banker_algorithm(
        processes, resources, Max, Allocated, Available, Request, process_id
    )
    
    # 输出结果
    print("分配结果:", "可以分配" if can_allocate else "不能分配")
    print("消息:", message)
    print("\n分配后的矩阵:")
    print("Allocated:")
    for row in new_Allocated:
        print(row)
    print("\nNeed:")
    for row in new_Need:
        print(row)
    print("\nAvailable:", new_Available)