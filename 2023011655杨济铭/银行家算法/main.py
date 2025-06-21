import copy


def safety_algorithm(Available, Allocated, Need):
    n = len(Allocated)  # 进程数
    m = len(Available)  # 资源种类数
    Work = Available[:]  # 复制可用资源
    Finish = [False] * n  # 初始化完成标记
    safe_sequence = []  # 安全序列

    # 尝试寻找可执行的进程
    while True:
        found = False
        for i in range(n):
            if not Finish[i]:
                # 检查当前进程的需求是否小于等于可用资源
                if all(Need[i][j] <= Work[j] for j in range(m)):
                    # 执行进程并释放资源
                    for j in range(m):
                        Work[j] += Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break  # 找到后重新开始扫描

        if not found:
            break

    return (True, safe_sequence) if all(Finish) else (False, None)


def banker_algorithm(Max, Need, Allocated, Available, Request, process_index):
    # 深拷贝输入矩阵以防止修改原始数据
    new_Max = copy.deepcopy(Max)
    new_Need = copy.deepcopy(Need)
    new_Allocated = copy.deepcopy(Allocated)
    new_Available = copy.deepcopy(Available)
    n_process = len(new_Allocated)
    m_res = len(new_Available)

    print("初始状态:")
    print("Max:", new_Max)
    print("Allocated:", new_Allocated)
    print("Need:", new_Need)
    print("Available:", new_Available)
    print("进程 P{} 请求资源:".format(process_index), Request)
    print("-" * 50)

    # 步骤1: 检查请求是否有效
    for j in range(m_res):
        if Request[j] > new_Need[process_index][j]:
            print("拒绝原因: 请求资源超过进程声明的最大需求")
            return False, new_Max, new_Allocated, new_Need, new_Available
    for j in range(m_res):
        if Request[j] > new_Available[j]:
            print("拒绝原因: 请求资源超过当前可用资源")
            return False, new_Max, new_Allocated, new_Need, new_Available

    # 步骤2: 尝试分配资源（临时修改状态）
    temp_Available = [new_Available[j] - Request[j] for j in range(m_res)]
    temp_Allocated = [row[:] for row in new_Allocated]  # 二维列表深拷贝
    temp_Need = [row[:] for row in new_Need]

    for j in range(m_res):
        temp_Allocated[process_index][j] += Request[j]
        temp_Need[process_index][j] -= Request[j]

    # 步骤3: 安全性检查
    safe, safe_sequence = safety_algorithm(temp_Available, temp_Allocated, temp_Need)

    if safe:
        # 分配成功，应用状态更新
        new_Available = temp_Available
        new_Allocated = temp_Allocated
        new_Need = temp_Need
        print("分配成功！系统安全，安全序列为:", safe_sequence)
        return True, new_Max, new_Allocated, new_Need, new_Available
    else:
        print("拒绝原因: 分配后系统将进入不安全状态")
        return False, new_Max, new_Allocated, new_Need, new_Available


# 测试用例
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
    Need = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]
    Available = [3, 3, 2]
    Request = [1, 0, 2]  # 进程1的请求
    process_index = 1

    # 调用银行家算法
    success, Max_out, Allocated_out, Need_out, Available_out = banker_algorithm(
        Max, Need, Allocated, Available, Request, process_index
    )

    # 输出最终状态
    print("\n最终状态:")
    print("Max:", Max_out)
    print("Allocated:", Allocated_out)
    print("Need:", Need_out)
    print("Available:", Available_out)
    print("分配结果:", "成功" if success else "失败")