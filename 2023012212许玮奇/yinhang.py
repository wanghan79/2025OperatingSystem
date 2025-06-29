# -*- coding: utf-8 -*-
import numpy as np

def print_resources_status(available: np.ndarray, max_table: np.ndarray, 
                           allocation: np.ndarray, need: np.ndarray) -> None:
    """打印当前资源状态和各进程信息"""
    print("\n进程\tMax\t\tAllocation\tNeed")
    for i in range(len(max_table)):
        print(f"P{i}\t{max_table[i]}\t\t{allocation[i]}\t\t{need[i]}")
    print(f"当前剩余资源: {available}")

def is_safe_state(available: np.ndarray, need: np.ndarray, 
                  allocation: np.ndarray) -> bool:
    """检查系统是否处于安全状态，返回安全序列或False"""
    n = len(need)
    work = available.copy()
    finish = np.zeros(n, dtype=bool)
    safe_sequence = []
    
    while not finish.all():
        found = False
        for i in range(n):
            if not finish[i] and (need[i] <= work).all():
                # 找到一个满足条件的进程
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            return False
    
    print(f"安全序列: {[f'P{i}' for i in safe_sequence]}")
    return True

def get_valid_input(prompt: str, validation_func, error_msg: str) -> np.ndarray:
    """获取并验证用户输入"""
    while True:
        try:
            input_str = input(prompt)
            values = np.array(input_str.split(), dtype=int)
            if validation_func(values):
                return values
            else:
                print(error_msg)
        except ValueError:
            print("输入格式错误，请重新输入。")

def main():
    # 获取资源信息
    m = int(input("资源种类: "))
    available = get_valid_input(
        f"请输入{m}种资源的数量（用空格分隔）: ",  # 修正此处
        lambda x: len(x) == m and (x >= 0).all(),
        f"输入错误：必须提供{m}个非负整数。"
    )
    
    # 获取进程信息
    n = int(input("进程数量: "))
    max_table = np.zeros((n, m), dtype=int)
    allocation = np.zeros((n, m), dtype=int)
    
    # 输入最大需求矩阵
    for i in range(n):
        max_table[i] = get_valid_input(
            f"进程 P{i} 的最大需求矩阵向量（{m}个整数）: ",
            lambda x: len(x) == m and (x >= 0).all(),
            f"输入错误：必须提供{m}个非负整数。"
        )
    
    # 输入分配矩阵
    for i in range(n):
        allocation[i] = get_valid_input(
            f"进程 P{i} 的分配矩阵向量（{m}个整数）: ",
            lambda x: len(x) == m and (x >= 0).all() and (x <= max_table[i]).all(),
            f"输入错误：必须提供{m}个非负整数，且每个值不能超过最大需求。"
        )
    
    # 计算需求矩阵和可用资源
    need = max_table - allocation
    available = available - np.sum(allocation, axis=0)
    
    print_resources_status(available, max_table, allocation, need)
    
    # 主循环处理资源请求
    while (need != 0).any():
        request_input = input("\n输入请求 (格式: P0,1 2 3)，输入q退出: ")
        if request_input.lower() == 'q':
            break
            
        try:
            pid_part, request_part = request_input.split(',')
            pid = int(pid_part[1:])
            request = np.array(request_part.strip().split(), dtype=int)
            
            # 验证请求有效性
            if pid < 0 or pid >= n:
                print("错误：无效的进程ID")
                continue
                
            if len(request) != m:
                print(f"错误：请求的资源数量必须为{m}个")
                continue
                
            if (request > need[pid]).any():
                print("错误：请求超过最大需求")
                continue
                
            if (request > available).any():
                print("错误：请求超过可用资源")
                continue
                
            # 尝试分配资源
            available_temp = available - request
            allocation_temp = allocation.copy()
            allocation_temp[pid] += request
            need_temp = need.copy()
            need_temp[pid] -= request
            
            # 检查安全性
            if is_safe_state(available_temp, need_temp, allocation_temp):
                print("分配成功")
                available = available_temp
                allocation = allocation_temp
                need = need_temp
                print_resources_status(available, max_table, allocation, need)
            else:
                print("分配失败：系统将进入不安全状态")
                
        except (ValueError, IndexError):
            print("输入格式错误，请使用格式: P0,1 2 3")

if __name__ == '__main__':
    main()
