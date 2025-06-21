# 文件二: main_program.py

from bankers_algorithm import bankers_algorithm

def print_system_state(available, max_claim, allocated, need):
    """打印系统当前状态"""
    n = len(max_claim)  # 进程数
    m = len(available)  # 资源种类数
    
    print("\n" + "="*70)
    print("当前系统状态".center(70))
    print("="*70)
    
    # 显示可用资源
    print("\n可用资源向量:")
    print("  ".join(f"资源{j+1}: {available[j]}" for j in range(m)))
    
    # 显示表头
    header = f"{'进程':<6}"
    for j in range(m):
        header += f"{'Max':<8}{'Allocated':<10}{'Need':<10}" if j == 0 else ""
    print("\n" + header)
    print("-" * 70)
    
    # 显示每个进程的资源信息
    for i in range(n):
        row = f"P{i:<4}"
        for j in range(m):
            row += f"{max_claim[i][j]:<8}{allocated[i][j]:<10}{need[i][j]:<10}"
        print(row)
    
    print("-" * 70)

if __name__ == "__main__":
    # 系统初始状态：5个进程，3种资源
    MAX_CLAIM = [
        [7, 5, 3],   # 进程0的最大需求
        [3, 2, 2],   # 进程1的最大需求
        [9, 0, 2],   # 进程2的最大需求
        [2, 2, 2],   # 进程3的最大需求
        [4, 3, 3]    # 进程4的最大需求
    ]
    
    ALLOCATED = [
        [0, 1, 0],   # 进程0已分配资源
        [2, 0, 0],   # 进程1已分配资源
        [3, 0, 2],   # 进程2已分配资源
        [2, 1, 1],   # 进程3已分配资源
        [0, 0, 2]    # 进程4已分配资源
    ]
    
    AVAILABLE = [3, 3, 2]  # 系统可用资源
    
    # 计算初始需求矩阵（剩余需求）
    NEED = [
        [MAX_CLAIM[i][j] - ALLOCATED[i][j] for j in range(3)]
        for i in range(5)
    ]
    
    # 显示初始系统状态
    print("初始系统状态:")
    print_system_state(AVAILABLE, MAX_CLAIM, ALLOCATED, NEED)
    
    # 测试1: 安全请求 - 进程1请求 [1, 0, 2]
    print("\n" + "="*70)
    print("测试1: 进程1请求资源 [1, 0, 2]".center(70))
    print("="*70)
    
    REQUEST1 = [1, 0, 2]
    PID1 = 1
    
    # 执行银行家算法
    result, max_claim1, need1, available1, allocated1, seq1, msg = bankers_algorithm(
        MAX_CLAIM, NEED, AVAILABLE, ALLOCATED, REQUEST1, PID1
    )
    
    # 处理结果
    print(f"\n{msg}")
    if result:
        print(f"安全序列: {' → '.join(f'P{p}' for p in seq1)}")
        print_system_state(available1, max_claim1, allocated1, need1)
        # 更新状态以进行后续测试
        MAX_CLAIM = max_claim1
        NEED = need1
        AVAILABLE = available1
        ALLOCATED = allocated1
    else:
        print_system_state(AVAILABLE, MAX_CLAIM, ALLOCATED, NEED)
    
    # 测试2: 安全请求 - 进程3请求 [0, 1, 0]
    print("\n" + "="*70)
    print("测试2: 进程3请求资源 [0, 1, 0]".center(70))
    print("="*70)
    
    REQUEST2 = [0, 1, 0]
    PID2 = 3
    
    # 执行银行家算法
    result, max_claim2, need2, available2, allocated2, seq2, msg = bankers_algorithm(
        MAX_CLAIM, NEED, AVAILABLE, ALLOCATED, REQUEST2, PID2
    )
    
    # 处理结果
    print(f"\n{msg}")
    if result:
        print(f"安全序列: {' → '.join(f'P{p}' for p in seq2)}")
        print_system_state(available2, max_claim2, allocated2, need2)
        # 更新状态以进行后续测试
        MAX_CLAIM = max_claim2
        NEED = need2
        AVAILABLE = available2
        ALLOCATED = allocated2
    else:
        print_system_state(AVAILABLE, MAX_CLAIM, ALLOCATED, NEED)
    
    # 测试3: 不安全请求 - 进程4请求 [3, 3, 1]
    print("\n" + "="*70)
    print("测试3: 进程4请求资源 [3, 3, 1]".center(70))
    print("="*70)
    
    REQUEST3 = [3, 3, 1]
    PID3 = 4
    
    # 执行银行家算法
    result, max_claim3, need3, available3, allocated3, seq3, msg = bankers_algorithm(
        MAX_CLAIM, NEED, AVAILABLE, ALLOCATED, REQUEST3, PID3
    )
    
    # 处理结果
    print(f"\n{msg}")
    if result:
        print(f"安全序列: {' → '.join(f'P{p}' for p in seq3)}")
        print_system_state(available3, max_claim3, allocated3, need3)
    else:
        print_system_state(AVAILABLE, MAX_CLAIM, ALLOCATED, NEED)
    
    print("\n所有测试完成")