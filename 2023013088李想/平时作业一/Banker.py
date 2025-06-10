def banker_algorithm(Max, Need, Available, Allocated, Request):
    """
    使用银行家算法判断是否可以安全地分配资源。

    参数:
    Max (List[List[int]]): 每个进程的最大资源需求矩阵
    Need (List[List[int]]): 每个进程仍需的资源矩阵（输入后会被修改）
    Available (List[int]): 当前可用资源向量（输入后会被修改）
    Allocated (List[List[int]]): 已分配资源矩阵（输入后会被修改）
    Request (List[int]): 当前进程提出的资源请求向量

    返回:
    Dict: {'safe': True/False, 'Available': List, 'Allocated': List[List], 'Need': List[List]}
    """
    num_processes = len(Max)
    num_resources = len(Available)

    # 深拷贝以避免修改原始数据
    import copy
    available = copy.deepcopy(Available)
    allocated = copy.deepcopy(Allocated)
    need = copy.deepcopy(Need)

    # 1. 检查请求是否超过当前最大需求
    for j in range(num_resources):
        if Request[j] > need[0][j]:  # 假设是第0个进程发出请求，可根据需要扩展为指定进程
            raise ValueError("请求超过了该进程的最大需求。")

    # 2. 检查是否有足够资源可用
    for j in range(num_resources):
        if Request[j] > available[j]:
            raise ValueError("没有足够的资源可供分配。")

    # 3. 模拟分配资源
    for j in range(num_resources):
        available[j] -= Request[j]
        allocated[0][j] += Request[j]  # 同样假设是第0个进程
        need[0][j] -= Request[j]

    # 4. 检查系统是否处于安全状态
    def is_safe_state(available_, allocated_, need_):
        work = available_.copy()
        finish = [False] * num_processes
        safe_sequence = []

        while len(safe_sequence) < num_processes:
            found = False
            for i in range(num_processes):
                if not finish[i] and all(n <= w for n, w in zip(need_[i], work)):
                    work = [work[j] + allocated_[i][j] for j in range(num_resources)]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
            if not found:
                return False
        return True

    if is_safe_state(available, allocated, need):
        return {
            'safe': True,
            'Available': available,
            'Allocated': allocated,
            'Need': need
        }
    else:
        return {
            'safe': False,
            'Available': Available,
            'Allocated': Allocated,
            'Need': Need
        }

# 示例数据
Max = [
    [1, 1, 3],
    [3, 2, 2],
    [4, 0, 2],
    [2, 2, 2],
    [1, 1, 3]
]

Allocated = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

Available = [3, 3, 2]

# 计算初始Need矩阵
Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Available))] for i in range(len(Max))]

# 资源请求：例如第一个进程请求 [1, 0, 2]
Request = [1, 0, 2]

# 调用函数
result = banker_algorithm(Max, Need, Available, Allocated, Request)

# 输出结果
if result['safe']:
    print("资源可以安全分配！")
    print("新的 Available:", result['Available'])
    print("新的 Allocated:", result['Allocated'])
    print("新的 Need:", result['Need'])
else:
    print("资源分配后系统不安全，无法进行分配。")
