import copy

def input_matrix(rows, cols, name):
    matrix = []
    print(f"\n请输入{name}矩阵（每行用空格分隔）:")
    for i in range(rows):
        while True:
            row = input(f"进程{i} > ").split()
            if len(row) != cols:
                print(f"错误：需要输入{cols}个数值")
                continue
            try:
                matrix.append([int(x) for x in row])
                break
            except ValueError:
                print("错误：请输入整数")
    return matrix


def input_vector(length, name):
    while True:
        values = input(f"\n请输入{name}向量（用空格分隔）> ").split()
        if len(values) != length:
            print(f"错误：需要输入{length}个数值")
            continue
        try:
            return [int(x) for x in values]
        except ValueError:
            print("错误：请输入整数")


def banker_algorithm(processes, max_res, allocated, available, request=None, pid=None):
    if request is not None and pid is not None:
        if any(request[i] > (max_res[pid][i] - allocated[pid][i]) for i in range(len(request))):
            return False, [], f"进程{pid}请求超过最大需求"

        if any(request[i] > available[i] for i in range(len(request))):
            return False, [], f"可用资源不足"

        new_alloc = copy.deepcopy(allocated)
        new_avail = copy.deepcopy(available)
        new_alloc[pid] = [new_alloc[pid][i] + request[i] for i in range(len(request))]
        new_avail = [new_avail[i] - request[i] for i in range(len(request))]
    else:
        new_alloc = allocated
        new_avail = available

    need = []
    for i in range(processes):
        need.append([max_res[i][j] - new_alloc[i][j] for j in range(len(max_res[i]))])

    work = copy.deepcopy(new_avail)
    finish = [False] * processes
    safe_sequence = []

    while True:
        found = False
        for i in range(processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                work = [work[j] + new_alloc[i][j] for j in range(len(work))]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            break

    if all(finish):
        return (True, safe_sequence, "安全") if request is None else (True, safe_sequence, "允许分配")
    else:
        return (False, [], "系统不安全") if request is None else (False, [], "分配会导致系统不安全")


if __name__ == "__main__":
    processes = int(input("请输入进程数: "))
    resource_types = int(input("请输入资源类型数: "))
    max_res = input_matrix(processes, resource_types, "最大需求")
    allocated = input_matrix(processes, resource_types, "已分配")
    available = input_vector(resource_types, "可用资源")
    is_safe, sequence, msg = banker_algorithm(processes, max_res, allocated, available)
    print(f"\n安全状态: {is_safe}")
    print(f"安全序列: {sequence}")
    print(f"详细信息: {msg}")

    print("\n========== 当前系统资源状态 ==========")

    print("\n【Max 最大需求矩阵】：")
    for row in max_res:
        print(" ", row)

    print("\n【Allocation 已分配矩阵】：")
    for row in allocated:
        print(" ", row)

    # 计算并打印 Need 矩阵
    need = [[max_res[i][j] - allocated[i][j] for j in range(resource_types)] for i in range(processes)]
    print("\n【Need 剩余需求矩阵】：")
    for row in need:
        print(" ", row)

    print("\n【Available 可用资源向量】：")
    print(" ", available)

