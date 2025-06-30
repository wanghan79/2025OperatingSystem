from typing import List, Tuple


def banker_algorithm(
        Max: List[List[int]],
        Allocation: List[List[int]],
        Available: List[int],
        Request: List[int]
) -> Tuple[bool, List[List[int]], List[int]]:
    """
    :param Max:        n×m 最大需求矩阵
    :param Allocation: n×m 已分配矩阵
    :param Available:  1×m 当前可用向量
    :param Request:    1×m 某进程一次资源请求向量
    :return:           (safe?, new_Allocation, new_Available)
    """
    n, m = len(Max), len(Max[0])
    Need = [[Max[i][j] - Allocation[i][j] for j in range(m)] for i in range(n)]

    # 找到发起请求的进程：第一个 Need ≥ Request 的进程
    pid = next((i for i in range(n)
                if all(Request[j] <= Need[i][j] for j in range(m))), None)
    if pid is None:
        raise ValueError("Request 与任何进程的 Need 不匹配")

    if any(Request[j] > Available[j] for j in range(m)):
        return False, Allocation, Available       # 资源不足，立即拒绝

    # 试分配
    Avail_tmp = [Available[j] - Request[j] for j in range(m)]
    Alloc_tmp = [row[:] for row in Allocation]
    Alloc_tmp[pid] = [Alloc_tmp[pid][j] + Request[j] for j in range(m)]
    Need_tmp = [[Max[i][j] - Alloc_tmp[i][j] for j in range(m)] for i in range(n)]

    # 安全性检查
    Work = Avail_tmp[:]
    Finish = [False] * n
    while True:
        progressed = False
        for i in range(n):
            if not Finish[i] and all(Need_tmp[i][j] <= Work[j] for j in range(m)):
                Work = [Work[j] + Alloc_tmp[i][j] for j in range(m)]
                Finish[i] = True
                progressed = True
        if not progressed:
            break
    safe = all(Finish)
    return safe, (Alloc_tmp if safe else Allocation), (Avail_tmp if safe else Available)


# ----------------------------- DEMO -----------------------------
if __name__ == "__main__":
    Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2]]
    Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2]]
    Available = [3, 3, 2]
    Request = [1, 0, 2]

    ok, new_alloc, new_avail = banker_algorithm(Max, Allocation, Available, Request)
    print("安全可分配？", ok)
    print("新的 Allocation:", new_alloc)
    print("新的 Available :", new_avail)
