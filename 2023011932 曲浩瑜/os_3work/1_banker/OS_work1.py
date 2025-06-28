import numpy as np

def banker_algorithm(**kwargs):
    """
    模拟银行家算法，判断资源请求是否可以安全地批准。
    函数接收关键词参数，包括：
    - max_matrix (np.ndarray): 各进程对每种资源的最大需求矩阵。
    - need_matrix (np.ndarray): 各进程对每种资源的剩余需求矩阵。
    - available_vector (np.ndarray): 每种资源的可用实例数量向量。
    - allocated_matrix (np.ndarray): 当前分配给各进程的每种资源数量矩阵。
    - process_id (int): 提出请求的进程ID。
    - request_vector (np.ndarray): 指定进程的请求向量。
    """
    # 从 kwargs 中提取参数
    max_matrix = kwargs.get('max_matrix')
    need_matrix = kwargs.get('need_matrix')
    available_vector = kwargs.get('available_vector')
    allocated_matrix = kwargs.get('allocated_matrix')
    process_id = kwargs.get('process_id')
    request_vector = kwargs.get('request_vector')

    # 检查所有必需参数是否都已提供
    required_params = ['max_matrix', 'need_matrix', 'available_vector',
                       'allocated_matrix', 'process_id', 'request_vector']
    for param in required_params:
        if kwargs.get(param) is None:
            print(f"错误: 缺少必需的关键词参数 '{param}'。")
            return False, {}

    num_processes, num_resources = max_matrix.shape

    # 1. 检查请求是否超过进程的Need
    if not all(request_vector[i] <= need_matrix[process_id][i] for i in range(num_resources)):
        print(f"\n进程 {process_id} 的请求超过了其声明的最大需求。")
        return False, {
            "Available": available_vector,
            "Allocated": allocated_matrix,
            "Need": need_matrix,
            "Max": max_matrix
        }

    # 2. 检查请求是否超过可用资源
    if not all(request_vector[i] <= available_vector[i] for i in range(num_resources)):
        print(f"\n进程 {process_id} 的请求超过了当前可用资源。进程必须等待。")
        return False, {
            "Available": available_vector,
            "Allocated": allocated_matrix,
            "Need": need_matrix,
            "Max": max_matrix
        }

    # 3. 尝试分配资源并进行安全性检查
    temp_available = np.copy(available_vector)
    temp_allocated = np.copy(allocated_matrix)
    temp_need = np.copy(need_matrix)

    for i in range(num_resources):
        temp_available[i] -= request_vector[i]
        temp_allocated[process_id][i] += request_vector[i]
        temp_need[process_id][i] -= request_vector[i]

    # 执行安全性检查
    if is_safe(temp_available, temp_need, temp_allocated, num_processes, num_resources):
        print(f"\n资源已安全地分配给进程 {process_id}。")
        return True, {
            "Available": temp_available,
            "Allocated": temp_allocated,
            "Need": temp_need,
            "Max": max_matrix
        }
    else:
        print(f"\n资源分配给进程 {process_id} 会导致系统进入不安全状态。分配被拒绝。")
        return False, {
            "Available": available_vector, # 返回原始状态
            "Allocated": allocated_matrix,
            "Need": need_matrix,
            "Max": max_matrix
        }

def is_safe(available, need, allocation, num_processes, num_resources):
    """
    使用银行家安全算法检查系统是否处于安全状态。

    参数:
        available (np.ndarray): 当前可用资源。
        need (np.ndarray): 各进程的剩余需求。
        allocation (np.ndarray): 分配给各进程的资源。
        num_processes (int): 进程数量。
        num_resources (int): 资源种类数量。

    返回:
        bool: 如果系统处于安全状态，则为True；否则为False。
    """
    work = np.copy(available)
    finish = np.full(num_processes, False)
    safe_sequence = []

    while True:
        found_process = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                # 如果进程i可以运行
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found_process = True
        if not found_process:
            break

    if all(finish):
        print(f"找到安全序列: {safe_sequence}")
        return True
    else:
        print("未找到安全序列。")
        return False


def main():
    # 初始系统状态
    initial_available = np.array([3, 3, 2])  # 可用资源A, B, C
    initial_max = np.array(
        [[7, 5, 3],  # P0 最大需求
         [3, 2, 2],  # P1 最大需求
         [9, 0, 2],  # P2 最大需求
         [2, 2, 2],  # P3 最大需求
         [4, 3, 3]]  # P4 最大需求
    )
    initial_allocated = np.array(
        [[0, 1, 0],  # P0 已分配
         [2, 0, 0],  # P1 已分配
         [3, 0, 2],  # P2 已分配
         [2, 1, 1],  # P3 已分配
         [0, 0, 2]]  # P4 已分配
    )
    initial_need = initial_max - initial_allocated

    num_processes = initial_max.shape[0]
    num_resources = initial_max.shape[1]

    print("--- 初始系统状态 ---")
    print("Available (可用资源):\n", initial_available)
    print("Max (最大需求):\n", initial_max)
    print("Allocated (已分配资源):\n", initial_allocated)
    print("Need (仍需资源):\n", initial_need)
    print("--------------------\n")

    # 获取用户输入的资源请求
    try:
        process_id_input = int(input(f"请输入提出请求的进程ID (0 到 {num_processes - 1}): "))
        if not (0 <= process_id_input < num_processes):
            raise ValueError("无效的进程ID。")

        request_input = []
        for i in range(num_resources):
            request_val = int(input(f"请输入对资源 {chr(ord('A') + i)} 的请求量: "))
            request_input.append(request_val)
        request_vector_input = np.array(request_input)

    except ValueError as e:
        print(f"错误: {e}")
        return

    # 调用银行家算法函数，现在以关键词参数形式传递
    can_allocate, updated_matrices = banker_algorithm(
        max_matrix=initial_max,
        need_matrix=initial_need,
        available_vector=initial_available,
        allocated_matrix=initial_allocated,
        process_id=process_id_input,
        request_vector=request_vector_input
    )

    print("\n--- 最终系统状态 ---")
    print("Max (最大需求):\n", updated_matrices["Max"])
    print("Available (可用资源):\n", updated_matrices["Available"])
    print("Allocated (已分配资源):\n", updated_matrices["Allocated"])
    print("Need (仍需资源):\n", updated_matrices["Need"])
    print("----------------------")

if __name__ == '__main__':
    main()