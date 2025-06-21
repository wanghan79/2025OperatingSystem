# 文件一: bankers_algorithm.py

import copy

def is_state_safe(available, need, allocated):
    """
    检查系统状态是否安全
    
    参数:
    available -- 当前可用资源向量
    need -- 每个进程的剩余需求矩阵
    allocated -- 每个进程的已分配资源矩阵
    
    返回:
    (安全状态, 安全序列) 元组
    """
    n = len(need)  # 进程数
    m = len(available)  # 资源种类数
    work = available.copy()  # 工作向量初始化为可用资源
    finish = [False] * n  # 标记进程是否完成
    safe_sequence = []  # 安全序列
    
    # 尝试找到安全序列
    for _ in range(n):
        found_process = False
        for i in range(n):
            # 检查进程i是否已完成且其资源需求是否小于等于当前可用资源
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                # 模拟进程执行完成：释放它占用的所有资源
                for j in range(m):
                    work[j] += allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found_process = True
                break
        
        # 如果一轮中没有找到符合条件的进程，提前退出循环
        if not found_process:
            break
    
    # 检查所有进程是否都已完成
    return all(finish), safe_sequence

def bankers_algorithm(max_claim, need, available, allocated, request, process_index):
    """
    银行家算法核心逻辑
    
    参数:
    max_claim -- 每个进程的最大需求矩阵
    need -- 每个进程的剩余需求矩阵
    available -- 当前可用资源向量
    allocated -- 每个进程的已分配资源矩阵
    request -- 资源请求向量
    process_index -- 请求资源的进程索引
    
    返回:
    (分配成功标志, 新Max矩阵, 新Need矩阵, 新Available向量, 新Allocated矩阵, 安全序列)
    """
    n = len(max_claim)  # 进程数
    m = len(available)  # 资源种类数
    
    # 1. 检查请求是否超过进程的最大需求
    if any(request[j] > max_claim[process_index][j] for j in range(m)):
        return False, max_claim, need, available, allocated, None, "错误：请求超过进程最大需求"
    
    # 2. 检查请求是否超过进程的剩余需求
    if any(request[j] > need[process_index][j] for j in range(m)):
        return False, max_claim, need, available, allocated, None, "错误：请求超过进程剩余需求"
    
    # 3. 检查请求是否超过当前可用资源
    if any(request[j] > available[j] for j in range(m)):
        return False, max_claim, need, available, allocated, None, "错误：请求超过系统可用资源"
    
    # 4. 创建临时状态进行试分配
    temp_available = available.copy()
    temp_allocated = copy.deepcopy(allocated)
    temp_need = copy.deepcopy(need)
    
    # 执行试分配
    for j in range(m):
        temp_available[j] -= request[j]
        temp_allocated[process_index][j] += request[j]
        temp_need[process_index][j] -= request[j]
    
    # 5. 对临时状态进行安全性检查
    is_safe, safe_sequence = is_state_safe(temp_available, temp_need, temp_allocated)
    
    # 6. 根据安全性检查结果确定是否分配
    if is_safe:
        # 安全：应用试分配结果
        return True, max_claim, temp_need, temp_available, temp_allocated, safe_sequence, "分配成功，系统安全"
    else:
        # 不安全：保持原状态不变
        return False, max_claim, need, available, allocated, None, "警告：分配将导致不安全状态"