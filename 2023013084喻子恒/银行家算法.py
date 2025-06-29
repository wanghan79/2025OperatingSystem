def bankers_algorithm(Max, Need, Available, Allocated, Request):
    """
    Max: 最大资源需求矩阵
    Need: 前需求矩阵
    Available: 可用资源向量
    Allocated: 已分配资源矩阵
    Request: 资源申请向量

    返回:
    Tuple (是否可以分配, 更新后的Available, 更新后的Need, 更新后的Allocated)
    """

    # 检查请求是否合法
    if len(Request) != len(Available):
        print("非法请求")
        return False, Available, Need, Allocated

    # 检查请求是否满足
    for i in range(len(Request)):
        if Request[i] > Need[i]:
            print("资源超限")
            return False, Available, Need, Allocated

    # 检查能否满足请求
    temp_available = Available.copy()
    temp_need = [n.copy() for n in Need]
    temp_allocated = [a.copy() for a in Allocated]

    # 创建请求副本并计算新的Available
    temp_available = [temp_available[i] - Request[i] for i in range(len(temp_available))]

    # 创建请求副本并计算新的Need和Allocated
    process_index = None
    for i in range(len(temp_need)):
        if all(temp_need[i][j] >= Request[j] for j in range(len(temp_available))):
            process_index = i
            break

    if process_index is None:
        print("拒绝，可用资源不足")
        return False, Available, Need, Allocated

    # 更新Available
    temp_available = [temp_available[i] + Allocated[process_index][i] for i in range(len(temp_available))]

    # 更新Need
    temp_need[process_index] = [0] * len(temp_available)

    # 更新Allocated
    temp_allocated[process_index] = [0] * len(temp_available)

    # 安全检查
    work = temp_available.copy()
    finish = [False] * len(temp_need)

    # 查找满足条件的进程
    while True:
        found = False
        for i in range(len(temp_need)):
            if not finish[i]:
                # 检查是否满足工作条件
                if all(temp_need[i][j] <= work[j] for j in range(len(work))):
                    # 更新work
                    work = [work[j] + temp_allocated[i][j] for j in range(len(work))]
                    finish[i] = True
                    found = True

        if not found:
            break

    # 检查是否所有进程都完成
    if all(finish):
        print("安全")
        return True, temp_available, temp_need, temp_allocated
    else:
        print("不安全")
        return False, Available, Need, Allocated

# 示例调用
if __name__ == "__main__":
    # 定义相关矩阵
    Max = [
        [8, 5, 2],
        [3, 6, 2],
        [7, 1, 3]
    ]

    Need = [
        [3, 1, 2],
        [2, 1, 0],
        [5, 0, 2]
    ]

    Allocated = [
        [4, 6, 2],
        [3, 1, 2],
        [9, 0, 2]
    ]

    Available = [10, 5, 7]

    Request = [2, 2, 0]

    # 执行银行家算法
    success, new_available, new_need, new_allocated = bankers_algorithm(
        Max, Need, Available, Allocated, Request
    )

    #输出部分
    print(f"\n是否可以分配: {success}")

    print(f"\n新的Available: {new_available}")

    print("\n新的Need:")
    for row in new_need:
        print(row)

    print("\n新的Allocated:")
    for row in new_allocated:
        print(row)
