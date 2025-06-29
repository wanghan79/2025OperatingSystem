import numpy as np

def banker_algorithm(Max, Need, Available, Allocated, Request, process_id):
    """
    实现银行家算法，用于判断是否可以安全地分配资源给一个进程。

    参数:
    Max (list of lists): 每个进程对每种资源的最大需求矩阵
    Need (list of lists): 每个进程对每种资源的当前需求矩阵
    Available (list): 当前可用资源向量
    Allocated (list of lists): 当前每个进程已分配的资源矩阵
    Request (list): 请求资源的向量
    process_id (int): 发出请求的进程的ID

    返回:
    tuple: 如果请求可以安全处理，则返回True和更新后的状态；否则返回False和错误信息
    """

    # 将输入转换为NumPy数组以便进行向量化操作
    Max = np.array(Max)
    Need = np.array(Need)
    Available = np.array(Available)
    Allocated = np.array(Allocated)
    Request = np.array(Request)

    # 检查请求是否小于或等于该进程的需求
    if not np.all(Request <= Need[process_id]):
        return False, "错误：请求超出了规定的需求范围。"

    # 检查请求是否小于或等于当前可用资源
    if not np.all(Request <= Available):
        return False, "错误：请求超出可用资源。"

    # 创建临时变量来模拟资源分配
    Available_temp = Available - Request  # 更新可用资源
    Allocated_temp = Allocated.copy()  # 复制当前分配情况以避免修改原始数据
    Allocated_temp[process_id] += Request  # 更新该进程已分配的资源
    Need_temp = Need.copy()  # 复制当前需求情况以避免修改原始数据
    Need_temp[process_id] -= Request  # 更新该进程的需求

    # 安全性检查：确保系统仍然处于安全状态
    Finish = [False] * len(Allocated)  # 跟踪每个进程是否已完成
    Work = Available_temp.copy()  # 工作向量表示当前可用资源

    while True:
        found = False
        for i in range(len(Finish)):
            if not Finish[i] and np.all(Need_temp[i] <= Work):
                # 如果该进程的需求可以被满足，则假设它完成并释放其资源
                Work += Allocated_temp[i]
                Finish[i] = True
                found = True
        if not found:
            break  # 如果没有找到可以完成的进程，退出循环

    # 如果所有进程都可以完成，则系统处于安全状态
    if all(Finish):
        return True, {
            "Available": Available_temp.tolist(),  # 转换回列表格式以便输出
            "Allocated": Allocated_temp.tolist(),
            "Need": Need_temp.tolist(),
            "Max": Max.tolist()
        }
    else:
        return False, "此次请求会使系统进入不安全状态，拒绝分配资源。"
