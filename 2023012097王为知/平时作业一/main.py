"""
@Author: Weizhi Wang
@Date: 2025-05-15
@Description: 模拟实现银行家算法，要求封装成一个函数，
能够接收 Max、Need、Available、Allocated 矩阵，
以及资源申请 Request, 使用银行家算法计算后输出是否能够分配，以及分配后的四个矩阵。
"""

import numpy as np
from bankers_algorithm import bankers_algorithm, print_state

if __name__ == "__main__":
    # 经典5进程3资源数据（A, B, C）
    Max = np.array([
        [7, 5, 3],   # 进程0
        [3, 2, 2],   # 进程1
        [9, 0, 2],   # 进程2
        [2, 2, 2],   # 进程3
        [4, 3, 3]    # 进程4
    ])
    
    Allocated = np.array([
        [0, 1, 0],   # 进程0已分配
        [2, 0, 0],   # 进程1已分配
        [3, 0, 2],   # 进程2已分配
        [2, 1, 1],   # 进程3已分配
        [0, 0, 2]    # 进程4已分配
    ])
    
    Need = Max - Allocated  # 计算需求矩阵
    Available = np.array([3, 3, 2])  # 初始可用资源
    
    print("【初始状态】")
    print_state(Available, Max, Allocated, Need)
    
    # 进程3请求资源 [0, 1, 0]
    Request = np.array([0, 1, 0])
    pid = 3  # 进程3
    
    print(f"\n【进程 {pid} 请求资源】{Request}")
    result, Avail_new, Max_new, Alloc_new, Need_new = bankers_algorithm(
        Max, Need, Available, Allocated, Request, pid
    )
    
    if result:
        print("\n【分配后状态】")
        print_state(Avail_new, Max_new, Alloc_new, Need_new)
