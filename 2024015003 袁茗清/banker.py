def is_safe(processes, avail, max_need, alloc):
    n = len(processes)
    m = len(avail)
    need = [[max_need[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]

    finish = [False] * n

    safe_seq = []

    work = avail[:]

    while len(safe_seq) < n:
        found = False
        for p in range(n):
            if not finish[p]:
                if all(need[p][j] <= work[j] for j in range(m)):
                    for j in range(m):
                        work[j] += alloc[p][j]
                    safe_seq.append(p)
                    finish[p] = True
                    found = True
        if not found:
            return None  

    return safe_seq


def banker_algorithm(processes, avail, max_need, alloc):
    safe_seq = is_safe(processes, avail, max_need, alloc)
    if not safe_seq:
        print("系统处于不安全状态")
        return

    print(f"安全序列为: {safe_seq}")

    n = len(processes)
    m = len(avail)

    # 初始化剩余可用资源
    work = avail[:]
    finish = [False] * n

    print("\n初始资源分配情况:")
    print_resources(avail, alloc, processes, finish)

    for process in safe_seq:
        print(f"\n正在执行进程 P{process}:")
        for j in range(m):
            work[j] += alloc[process][j]
            alloc[process][j] = 0
        finish[process] = True
        print_resources(work, alloc, processes, finish)


def print_resources(avail, alloc, processes, finish):
    print(f"Available: {avail}")
    print("Process Allocation Finish")
    for i in range(len(processes)):
        print(f"P{i}      {' '.join(map(str, alloc[i]))}     {finish[i]}")


def get_input():
    n = int(input("请输入进程的数量: "))
    m = int(input("请输入资源的种类数量: "))

    processes = [f"P{i}" for i in range(n)]
    avail = list(map(int, input(f"请输入可用资源的数量 (共 {m} 种): ").split()))

    print(f"请输入每个进程的最大需求矩阵 ({n} x {m}):")
    max_need = []
    for i in range(n):
        row = list(map(int, input(f"进程 P{i}: ").split()))
        max_need.append(row)

    print(f"请输入当前分配矩阵 ({n} x {m}):")
    alloc = []
    for i in range(n):
        row = list(map(int, input(f"进程 P{i}: ").split()))
        alloc.append(row)

    return processes, avail, max_need, alloc


if __name__ == "__main__":
    processes, avail, max_need, alloc = get_input()
    banker_algorithm(processes, avail, max_need, alloc)



