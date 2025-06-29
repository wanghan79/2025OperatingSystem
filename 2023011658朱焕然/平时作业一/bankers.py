def bankers(Max, Allocation, Available, Request, pid):
    n = len(Max)       # 进程数
    m = len(Max[0])    # 资源种类数

    # 计算 Need
    Need = [[Max[i][j] - Allocation[i][j] for j in range(m)] for i in range(n)]

    # 检查 Request <= Need[pid]
    for j in range(m):
        if Request[j] > Need[pid][j]:
            print("错误：请求的资源超过最大需求")
            return False

    # 检查 Request <= Available
    for j in range(m):
        if Request[j] > Available[j]:
            print("请求资源不足，进程需等待。")
            return False

    # 试探分配
    for j in range(m):
        Available[j] -= Request[j]
        Allocation[pid][j] += Request[j]
        Need[pid][j] -= Request[j]

    # 安全性检查
    Work = Available[:]
    Finish = [False] * n

    while True:
        found = False
        for i in range(n):
            if not Finish[i] and all(Need[i][j] <= Work[j] for j in range(m)):
                # 模拟进程完成
                for j in range(m):
                    Work[j] += Allocation[i][j]
                Finish[i] = True
                found = True
        if not found:
            break

    if all(Finish):
        print("请求可以被满足。")
        print("新的 Available:", Available)
        print("新的 Allocation:", Allocation)
        print("新的 Need:", Need)
        return True
    else:
        # 回滚
        for j in range(m):
            Available[j] += Request[j]
            Allocation[pid][j] -= Request[j]
            Need[pid][j] += Request[j]
        print("请求无法满足，被拒绝，已回滚。")
        return False
