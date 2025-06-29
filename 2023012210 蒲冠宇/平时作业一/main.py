import copy

def is_system_safe(available_resources, allocated_matrix, need_matrix):
    """
    安全算法：判断系统是否处于安全状态
    :param available_resources: 可用资源列表
    :param allocated_matrix: 已分配资源矩阵
    :param need_matrix: 需求资源矩阵
    :return: (是否安全, 安全序列)
    """
    process_count = len(allocated_matrix)
    resource_types = len(available_resources)
    
    # 复制可用资源，避免修改原始数据
    work_resources = available_resources.copy()
    finish_status = [False] * process_count
    safe_sequence = []
    
    # 模拟资源分配过程，寻找安全序列
    while True:
        found = False
        for i in range(process_count):
            if not finish_status[i] and all(need_matrix[i][j] <= work_resources[j] for j in range(resource_types)):
                # 分配资源并回收
                for j in range(resource_types):
                    work_resources[j] += allocated_matrix[i][j]
                finish_status[i] = True
                safe_sequence.append(i)
                found = True
                break  # 重新开始扫描，确保找到最短安全序列
                
        if not found:
            break
    
    return (True, safe_sequence) if all(finish_status) else (False, None)

def banker_algorithm(max_demand, current_need, allocated, available, request, process_id):
    """
    银行家算法：处理资源请求并判断是否可以安全分配
    :param max_demand: 最大需求矩阵
    :param current_need: 当前需求矩阵
    :param allocated: 已分配资源矩阵
    :param available: 可用资源列表
    :param request: 资源请求列表
    :param process_id: 请求资源的进程ID
    :return: (分配结果, 更新后的最大需求矩阵, 已分配矩阵, 需求矩阵, 可用资源)
    """
    # 深拷贝防止修改原始数据
    new_max = copy.deepcopy(max_demand)
    new_need = copy.deepcopy(current_need)
    new_allocated = copy.deepcopy(allocated)
    new_available = copy.deepcopy(available)
    
    print("初始系统状态:")
    print("最大需求矩阵:", new_max)
    print("已分配资源:", new_allocated)
    print("需求矩阵:", new_need)
    print("可用资源:", new_available)
    print(f"进程 P{process_id} 请求资源:", request)
    print("-" * 50)
    
    # 步骤1: 验证请求合法性
    for j in range(len(new_available)):
        if request[j] > new_need[process_id][j]:
            print("请求被拒绝：请求量超过进程最大需求")
            return False, new_max, new_allocated, new_need, new_available
            
    for j in range(len(new_available)):
        if request[j] > new_available[j]:
            print("请求被拒绝：可用资源不足")
            return False, new_max, new_allocated, new_need, new_available
    
    # 步骤2: 尝试分配资源
    temp_available = [new_available[j] - request[j] for j in range(len(new_available))]
    temp_allocated = [row.copy() for row in new_allocated]
    temp_need = [row.copy() for row in new_need]
    
    for j in range(len(new_available)):
        temp_allocated[process_id][j] += request[j]
        temp_need[process_id][j] -= request[j]
    
    # 步骤3: 安全性检查
    is_safe, safety_sequence = is_system_safe(temp_available, temp_allocated, temp_need)
    
    if is_safe:
        # 分配成功，更新系统状态
        new_available = temp_available
        new_allocated = temp_allocated
        new_need = temp_need
        print(f"资源分配成功！系统处于安全状态，安全序列为: P{safety_sequence}")
        return True, new_max, new_allocated, new_need, new_available
    else:
        print("资源分配被拒绝：分配将导致系统进入不安全状态")
        return False, new_max, new_allocated, new_need, new_available

if __name__ == "__main__":
    # 测试用例：5个进程，3类资源
    max_demand = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    
    allocated_resources = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    
    current_need = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]
    
    available_resources = [3, 3, 2]
    resource_request = [1, 0, 2]  # 进程1请求资源
    process_id = 1
    
    # 执行银行家算法
    result, max_out, allocated_out, need_out, available_out = banker_algorithm(
        max_demand, current_need, allocated_resources, available_resources, 
        resource_request, process_id
    )
    
    # 输出最终状态
    print("\n系统最终状态:")
    print("最大需求矩阵:", max_out)
    print("已分配资源:", allocated_out)
    print("需求矩阵:", need_out)
    print("可用资源:", available_out)
    print("资源分配结果:", "成功" if result else "失败")
