import copy

def banker_algorithm(max_demand, need_matrix, available_resources, allocated_resources, resource_request):
    """
    实现银行家算法的函数。

    参数:
    max_demand: 二维列表，表示每个进程的最大资源需求矩阵。
    need_matrix: 二维列表，表示每个进程还需要的资源数量矩阵。
    available_resources: 一维列表，表示当前系统可用资源数量。
    allocated_resources: 二维列表，表示已分配给各进程的资源数量矩阵。
    resource_request: 一维列表，表示资源申请。

    返回:
    字典，包含是否安全以及分配后的资源状态：
    {
        'safe': True/False,
        'available': 新的可用资源向量,
        'allocated': 新的已分配资源矩阵,
        'need': 新的需求资源矩阵
    }
    """
    # 检查输入是否合法
    if len(available_resources) != len(resource_request):
        raise ValueError("可用资源和请求资源的维度不匹配")

    for i in range(len(max_demand)):
        if len(max_demand[i]) != len(resource_request):
            raise ValueError("最大需求矩阵的行维度与资源类型不匹配")
        if len(need_matrix[i]) != len(resource_request):
            raise ValueError("需求矩阵的行维度与资源类型不匹配")
        if len(allocated_resources[i]) != len(resource_request):
            raise ValueError("已分配资源矩阵的行维度与资源类型不匹配")

    # 深拷贝以避免修改原始数据
    temp_available = copy.deepcopy(available_resources)
    temp_allocated = copy.deepcopy(allocated_resources)
    temp_need = copy.deepcopy(need_matrix)

    # 检查请求是否超过该进程的需求
    if any(resource_request[i] > temp_need[-1][i] for i in range(len(resource_request))):
        return {
            'safe': False,
            'available': available_resources,
            'allocated': allocated_resources,
            'need': need_matrix
        }

    # 检查请求是否超过系统可用资源
    if any(resource_request[i] > temp_available[i] for i in range(len(resource_request))):
        return {
            'safe': False,
            'available': available_resources,
            'allocated': allocated_resources,
            'need': need_matrix
        }

    # 模拟分配
    for i in range(len(resource_request)):
        temp_available[i] -= resource_request[i]
        temp_allocated[-1][i] += resource_request[i]
        temp_need[-1][i] -= resource_request[i]

    # 检查系统是否处于安全状态
    work = temp_available.copy()
    process_finished = [False] * len(max_demand)

    while True:
        found = False
        for i in range(len(max_demand)):
            if not process_finished[i]:
                if all(temp_need[i][j] <= work[j] for j in range(len(work))):
                    process_finished[i] = True
                    found = True
                    for j in range(len(work)):
                        work[j] += temp_allocated[i][j]
                    break  # 重新开始查找可执行的进程

        if not found:
            break

    # 判断是否所有进程都完成
    if all(process_finished):
        # 分配安全，更新原始数据
        for i in range(len(resource_request)):
            available_resources[i] -= resource_request[i]
            allocated_resources[-1][i] += resource_request[i]
            need_matrix[-1][i] -= resource_request[i]

        return {
            'safe': True,
            'available': available_resources,
            'allocated': allocated_resources,
            'need': need_matrix
        }
    else:
        # 不安全，不更新资源
        return {
            'safe': False,
            'available': available_resources,
            'allocated': allocated_resources,
            'need': need_matrix
        }

# 示例用法
if __name__ == "__main__":
    # 示例数据
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

    need_matrix = [
        [7 - 0, 5 - 1, 3 - 0],
        [3 - 2, 2 - 0, 2 - 0],
        [9 - 3, 0 - 0, 2 - 2],
        [2 - 2, 2 - 1, 2 - 1],
        [4 - 0, 3 - 0, 3 - 2]
    ]

    available_resources = [10, 5, 7]
    resource_request = [1, 0, 2]

    # 调用银行家算法
    result = banker_algorithm(max_demand, need_matrix, available_resources, allocated_resources, resource_request)

    # 输出结果
    if result['safe']:
        print("资源可以安全分配！")
        print("新的可用资源:", result['available'])
        print("新的已分配资源:")
        for row in result['allocated']:
            print(row)
        print("新的需求资源:")
        for row in result['need']:
            print(row)
    else:
        print("资源分配后系统不安全，无法进行分配。")