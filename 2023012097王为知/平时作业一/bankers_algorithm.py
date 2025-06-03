"""
@Author: Weizhi Wang
@Date: 2025-05-15
@Description: 银行家算法模块实现资源分配和安全性检查，避免死锁
"""

import numpy as np

def bankers_algorithm(Max, Need, Available, Allocated, Request, pid):
    """银行家算法核心逻辑"""
    n, m = Max.shape
    
    # 1. 检查请求是否超过需求
    if np.any(Request > Need[pid]):
        print(f"错误：进程 {pid} 的请求超过最大需求")
        return False, Available, Max, Allocated, Need
    
    # 2. 检查请求是否超过可用资源
    if np.any(Request > Available):
        print(f"错误：进程 {pid} 的请求超过当前可用资源")
        return False, Available, Max, Allocated, Need
    
    # 3. 尝试分配资源（临时状态）
    Available_temp = Available - Request
    Allocated_temp = Allocated.copy()
    Allocated_temp[pid] += Request
    Need_temp = Need.copy()
    Need_temp[pid] -= Request
    
    # 4. 安全性检查
    if is_safe_state(Available_temp, Need_temp, Allocated_temp):
        print(f"资源分配成功，安全序列为：{safe_sequence}")
        return True, Available_temp, Max, Allocated_temp, Need_temp
    else:
        print("资源分配会导致不安全状态，请求被拒绝")
        return False, Available, Max, Allocated, Need

def is_safe_state(Available, Need, Allocated):
    """安全性检查，返回是否安全及安全序列"""
    global safe_sequence
    n, m = Need.shape
    Work = Available.copy()
    Finish = np.zeros(n, dtype=bool)
    safe_sequence = []
    
    # 寻找安全序列
    for _ in range(n):
        for i in range(n):
            if not Finish[i] and np.all(Need[i] <= Work):
                Work += Allocated[i]
                Finish[i] = True
                safe_sequence.append(i)
                break
        else:  # 未找到可执行进程
            return False
    
    return True

def print_state(Available, Max, Allocated, Need):
    """打印系统状态"""
    print("\n当前系统状态：")
    print(f"可用资源：{Available}")
    print("最大需求矩阵（Max）：")
    print(Max)
    print("已分配矩阵（Allocated）：")
    print(Allocated)
    print("需求矩阵（Need）：")
    print(Need)
