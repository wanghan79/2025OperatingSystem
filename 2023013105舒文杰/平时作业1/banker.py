import numpy as np

def is_safe_state(available, need, allocation):
    """
    安全性检查函数：判断当前资源分配是否安全。
    :param available: 当前可用资源列表
    :param need: 每个进程剩余的资源需求
    :param allocation: 当前资源分配情况
    :return: (是否安全, 安全执行序列)
    """
    num_processes = allocation.shape[0]
    work = available.copy()
    finished = [False] * num_processes
    sequence = []

    while True:
        progress = False
        for pid in range(num_processes):
            if not finished[pid] and np.all(need[pid] <= work):
                work += allocation[pid]
                finished[pid] = True
                sequence.append(pid)
                progress = True
        if not progress:
            break

    return all(finished), sequence


def banker_algorithm(max_demand, allocation, available, request, pid):
    """
    银行家算法主函数
    :param max_demand: 每个进程的最大需求矩阵
    :param allocation: 当前资源分配矩阵
    :param available: 可用资源列表
    :param request: 当前进程的资源请求
    :param pid: 当前请求资源的进程编号
    :return: (是否允许分配, 结果或错误提示)
    """
    max_demand = max_demand.copy()
    allocation = allocation.copy()
    available = available.copy()
    request = request.copy()

    need = max_demand - allocation

    if not np.all(request <= need[pid]):
        return False, "请求超过进程最大需求"

    if not np.all(request <= available):
        return False, "系统资源不足，无法满足请求"

    # 试探性分配资源
    available -= request
    allocation[pid] += request
    need[pid] -= request

    safe, sequence = is_safe_state(available, need, allocation)

    if safe:
        return True, {
            "Max": max_demand,
            "Need": need,
            "Available": available,
            "Allocation": allocation,
            "SafeSequence": sequence
        }
    else:
        # 回滚
        allocation[pid] -= request
        available += request
        need[pid] += request
        return False, "请求会导致系统进入不安全状态，已拒绝"


# 示例测试
if __name__ == "__main__":
    available = np.array([3, 3, 2])
    max_matrix = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    allocation_matrix = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    request_vector = np.array([1, 1, 2])
    current_pid = 1

    ok, result = banker_algorithm(max_matrix, allocation_matrix, available, request_vector, current_pid)

    if ok:
        print("资源已成功分配！")
        print("安全执行序列：", result["SafeSequence"])
        print("新的 Available：", result["Available"])
        print("新的 Allocation：\n", result["Allocation"])
        print("新的 Need：\n", result["Need"])
    else:
        print("资源请求失败：", result)
