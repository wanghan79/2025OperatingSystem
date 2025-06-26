import copy


def banker_algorithm(Max, Need, Available, Allocated, Request):

    # 深拷贝输入数据，避免修改原始数据
    Max = copy.deepcopy(Max)
    Need = copy.deepcopy(Need)
    Available = copy.deepcopy(Available)
    Allocated = copy.deepcopy(Allocated)

    pid, request = Request
    n = len(Max)  # 进程数
    m = len(Available)  # 资源种类数

    # 步骤1: 验证请求是否小于等于需求
    for j in range(m):
        if request[j] > Need[pid][j]:
            return {
                'allocation_possible': False,
                'safe_state': False,
                'safe_sequence': None,
                'message': f"错误：请求超过进程 {pid} 的最大需求（资源 {j}）",
                'Available': Available,
                'Need': Need,
                'Allocated': Allocated,
                'Max': Max
            }

    # 步骤2: 验证请求是否小于等于可用资源
    for j in range(m):
        if request[j] > Available[j]:
            return {
                'allocation_possible': False,
                'safe_state': False,
                'safe_sequence': None,
                'message': f"错误：请求超过可用资源（资源 {j}）",
                'Available': Available,
                'Need': Need,
                'Allocated': Allocated,
                'Max': Max
            }

    # 步骤3: 尝试分配资源
    old_Available = copy.deepcopy(Available)
    old_Need = copy.deepcopy(Need)
    old_Allocated = copy.deepcopy(Allocated)

    # 更新矩阵
    for j in range(m):
        Available[j] -= request[j]
        Allocated[pid][j] += request[j]
        Need[pid][j] -= request[j]

    # 步骤4: 安全性检查
    Work = copy.deepcopy(Available)
    Finish = [False] * n
    safe_sequence = []

    # 查找可安全执行的进程
    while True:
        found = False
        for i in range(n):
            if not Finish[i]:
                # 检查资源是否满足
                resource_ok = True
                for j in range(m):
                    if Need[i][j] > Work[j]:
                        resource_ok = False
                        break

                # 如果资源满足则执行进程
                if resource_ok:
                    # 释放资源
                    for j in range(m):
                        Work[j] += Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break

        if not found:
            break

    # 判断系统是否安全
    if all(Finish):
        return {
            'allocation_possible': True,
            'safe_state': True,
            'safe_sequence': safe_sequence,
            'message': "分配成功！系统处于安全状态。",
            'Available': Available,
            'Need': Need,
            'Allocated': Allocated,
            'Max': Max
        }
    else:
        # 不安全则回滚分配
        return {
            'allocation_possible': False,
            'safe_state': False,
            'safe_sequence': None,
            'message': "分配失败：系统将进入不安全状态",
            'Available': old_Available,
            'Need': old_Need,
            'Allocated': old_Allocated,
            'Max': Max
        }


# 测试示例
if __name__ == "__main__":
    # 示例数据（5个进程，3类资源）
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    Allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    # 计算需求矩阵 Need = Max - Allocated
    Need = []
    for i in range(len(Max)):
        row = []
        for j in range(len(Max[0])):
            row.append(Max[i][j] - Allocated[i][j])
        Need.append(row)

    Available = [3, 3, 2]  # 可用资源

    # 测试请求：进程1请求资源 [1, 0, 2]
    Request = (1, [1, 0, 2])

    # 执行银行家算法
    result = banker_algorithm(Max, Need, Available, Allocated, Request)

    # 打印结果
    print("===== 银行家算法结果 =====")
    print(f"请求是否允许: {'是' if result['allocation_possible'] else '否'}")
    print(f"系统安全: {'是' if result['safe_state'] else '否'}")
    print(f"信息: {result['message']}")
    if result['safe_sequence']:
        print(f"安全序列: {result['safe_sequence']}")

    print("\n更新后的矩阵:")
    print("可用资源 (Available):", result['Available'])
    print("\n分配矩阵 (Allocated):")
    for row in result['Allocated']:
        print(row)
    print("\n需求矩阵 (Need):")
    for row in result['Need']:
        print(row)
    print("\n最大需求矩阵 (Max):")
    for row in result['Max']:
        print(row)