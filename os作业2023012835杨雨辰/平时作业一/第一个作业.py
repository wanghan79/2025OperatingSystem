import numpy as np


def bankers_algorithm(Max, Need, Available, Allocated, Request, process_id):
    """
    实现银行家算法来判断资源请求是否可以安全分配

    参数:
    Max (np.ndarray): 最大需求矩阵，形状为 (n_processes, n_resources)
    Need (np.ndarray): 需求矩阵，形状为 (n_processes, n_resources)
    Available (np.ndarray): 可用资源向量，形状为 (n_resources,)
    Allocated (np.ndarray): 已分配资源矩阵，形状为 (n_processes, n_resources)
    Request (np.ndarray): 资源请求向量，形状为 (n_resources,)
    process_id (int): 请求资源的进程编号

    返回:
    tuple: (是否可以分配, 分配后的 Available, 分配后的 Allocated,
           分配后的 Need, 分配后的 Max)
    """
    n_processes, n_resources = Max.shape

    # 步骤 1: 检查请求是否超过需求
    if np.any(Request > Need[process_id]):
        return False, Available, Allocated, Need, Max

    # 步骤 2: 检查请求是否超过可用资源
    if np.any(Request > Available):
        return False, Available, Allocated, Need, Max

    # 步骤 3: 尝试分配资源
    Available_temp = Available - Request
    Allocated_temp = Allocated.copy()
    Allocated_temp[process_id] += Request
    Need_temp = Need.copy()
    Need_temp[process_id] -= Request

    # 步骤 4: 执行安全性检查
    def is_safe(available, allocated, need):
        work = available.copy()
        finish = np.zeros(n_processes, dtype=bool)
        safe_sequence = []

        while True:
            found = False
            for i in range(n_processes):
                if not finish[i] and np.all(need[i] <= work):
                    work += allocated[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
            if not found:
                break

        return np.all(finish), safe_sequence

    safe, sequence = is_safe(Available_temp, Allocated_temp, Need_temp)

    if safe:
        # 如果安全，则更新并返回新状态
        return True, Available_temp, Allocated_temp, Need_temp, Max
    else:
        # 如果不安全，则返回原始状态
        return False, Available, Allocated, Need, Max


# 示例使用
if __name__ == "__main__":
    # 初始化矩阵
    Max = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])

    Allocated = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])

    Need = Max - Allocated
    Available = np.array([3, 3, 2])

    # 进程 1 请求资源 [1, 0, 2]
    Request = np.array([1, 0, 2])
    process_id = 1

    # 执行银行家算法
    can_allocate, new_Available, new_Allocated, new_Need, new_Max = bankers_algorithm(
        Max, Need, Available, Allocated, Request, process_id
    )

    # 输出结果
    print(f"是否可以分配: {can_allocate}")
    if can_allocate:
        print("\n分配后的矩阵:")
        print("可用资源 (Available):")
        print(new_Available)
        print("\n已分配资源 (Allocated):")
        print(new_Allocated)
        print("\n需求矩阵 (Need):")
        print(new_Need)
        print("\n最大需求矩阵 (Max):")
        print(new_Max)