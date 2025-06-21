"""
银行家算法
参数:
  Max: 每个进程对资源的最大需求矩阵
  Need: 每个进程对资源的需求矩阵
  Available: 当前可用的资源向量
  Allocated: 当前已分配的资源矩阵
  process_index: 进程索引号
  Request: 当前请求的资源向量
输入：
  Max, Need, Available, Allocated, process_index, Request
输出：
  Max, Need, Available, Allocated
"""
def bankers(Max, Need, Available, Allocated, process_index, Request):
    num_processes = len(Max)
    num_resources = len(Available)

    # 检查Request与Available数匹配
    if len(Request) != num_resources:
        raise ValueError("请求的资源向量与当前可用资源向量不匹配")

    # 检查Request是否超过Available
    if any(Request[i] > Available[i] for i in range(num_resources)):
        return False, Max, Need, Available, Allocated

    # 检查Request是否超过Need
    if any(Request[i] > Need[process_index][i] for i in range(num_resources)):
        return False, Max, Need, Available, Allocated

    temp_Allocated = [row[:] for row in Allocated]
    temp_Need = [row[:] for row in Need]
    temp_Available = list(Available)

    for i in range(num_resources):
        temp_Allocated[process_index][i] += Request[i]
        temp_Need[process_index][i] -= Request[i]
        temp_Available[i] -= Request[i]

    # 安全性检查
    work = list(temp_Available)
    finish = [False] * num_processes

    while True:
        found = False
        for i in range(num_processes):
            if not finish[i] and all(temp_Need[i][j] <= work[j] for j in range(num_resources)):
                for j in range(num_resources):
                    work[j] += temp_Allocated[i][j]
                finish[i] = True
                found = True
        if not found:
            break

    if all(finish):
        return True, Max, temp_Need, temp_Available, temp_Allocated
    else:
        return False, Max, Need, Available, Allocated


if __name__ == "__main__":
    # 传入的数据
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    Need = [
        [7, 0, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]
    Available = [3, 99, 2]
    Allocated = [
        [0, 9, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    process_index = 1
    Request = [1, 0, 2]

    # 算法调用
    safe, new_Max, new_Need, new_Available, new_Allocated = bankers(
        Max, Need, Available, Allocated, process_index, Request
    )

    if safe:
        print("系统处于安全状态。此时：")
        print("最大需求矩阵:", new_Max)
        print("需求矩阵:", new_Need)
        print("可利用矩阵:", new_Available)
        print("分配矩阵:", new_Allocated)
    else:
        print("系统处于不安全状态。")
