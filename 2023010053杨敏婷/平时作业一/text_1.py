def banker_algorithm(processes, resources, Max, Allocation, Available, Request, process_id):
    """
    银行家算法实现
    """

    #检查请求是否小于等于Need
    for i in range(len(resources)):
        if Request[i] > Max[process_id][i] - Allocation[process_id][i]:
            print(f"错误：进程P{process_id}请求的资源超过其最大需求")
            return False, Max, Allocation, Available

    #检查请求是否小于等于Available
    for i in range(len(resources)):
        if Request[i] > Available[i]:
            print(f"错误：没有足够的资源分配给进程P{process_id}")
            return False, Max, Allocation, Available

    #尝试分配资源
    old_Available = Available.copy()
    old_Allocation = [row.copy() for row in Allocation]

    #模拟分配
    for i in range(len(resources)):
        Available[i] -= Request[i]
        Allocation[process_id][i] += Request[i]

    #检查安全性
    if is_safe(processes, resources, Max, Allocation, Available):
        print(f"请求可以立即被满足，系统处于安全状态")
        #更新Need矩阵
        Need = calculate_need(Max, Allocation)
        return True, Max, Need, Allocation, Available
    else:
        print(f"分配后系统将处于不安全状态，拒绝请求")
        return False, Max, calculate_need(Max, old_Allocation), old_Allocation, old_Available


def is_safe(processes, resources, Max, Allocation, Available):
    """
    检查系统是否处于安全状态
    """
    num_processes = len(processes)
    num_resources = len(resources)

    #计算Need矩阵
    Need = calculate_need(Max, Allocation)

    #初始化工作向量
    Work = Available.copy()

    #初始化Finish标记
    Finish = [False] * num_processes

    #安全序列
    safe_sequence = []

    #寻找可以满足的进程
    while True:
        found = False
        for i in range(num_processes):
            if not Finish[i]:
                #检查Need[i] <= Work
                can_allocate = True
                for j in range(num_resources):
                    if Need[i][j] > Work[j]:
                        can_allocate = False
                        break

                if can_allocate:
                    #模拟执行并释放资源
                    for j in range(num_resources):
                        Work[j] += Allocation[i][j]
                    Finish[i] = True
                    safe_sequence.append(f"P{i}")
                    found = True

        #如果没有找到可以满足的进程，退出循环
        if not found:
            break

    #检查所有进程是否完成
    if all(Finish):
        print(f"系统处于安全状态，安全序列: {' -> '.join(safe_sequence)}")
        return True
    else:
        print("系统将处于不安全状态")
        return False


def calculate_need(Max, Allocation):
    """
    计算Need矩阵
    """
    Need = []
    for i in range(len(Max)):
        need_row = []
        for j in range(len(Max[i])):
            need_row.append(Max[i][j] - Allocation[i][j])
        Need.append(need_row)
    return Need


def print_state(processes, resources, Max, Need, Allocation, Available):
    """
    打印当前系统状态
    """
    print("\n当前系统状态:")
    print("进程\tMax\t\tAllocation\tNeed\t\tAvailable")

    for i in range(len(processes)):
        print(f"P{i}\t{Max[i]}\t{Allocation[i]}\t{Need[i]}", end="")
        if i == 0:
            print(f"\t{Available}")
        else:
            print()

    print("\n")


#示例使用
if __name__ == "__main__":
    #定义进程和资源
    processes = [0, 1, 2, 3, 4]
    resources = ['A', 'B', 'C']

    #初始矩阵定义
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    Allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    Available = [3, 3, 2]

    #计算初始Need矩阵
    Need = calculate_need(Max, Allocation)

    #打印初始状态
    print("初始状态:")
    print_state(processes, resources, Max, Need, Allocation, Available)

    #进程1请求资源 [1, 0, 2]
    Request = [1, 0, 2]
    process_id = 1
    print(f"进程P{process_id}请求资源: {Request}")

    success, Max, Need, Allocation, Available = banker_algorithm(
        processes, resources, Max, Allocation, Available, Request, process_id
    )

    print_state(processes, resources, Max, Need, Allocation, Available)

    #进程4请求资源 [3, 3, 0]
    Request = [3, 3, 0]
    process_id = 4
    print(f"进程P{process_id}请求资源: {Request}")

    success, Max, Need, Allocation, Available = banker_algorithm(
        processes, resources, Max, Allocation, Available, Request, process_id
    )

    print_state(processes, resources, Max, Need, Allocation, Available)