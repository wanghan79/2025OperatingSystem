def input_matrix(rows, cols, name):
    """输入矩阵数据"""
    matrix = []
    print(f"\n请输入 {name} 矩阵 ({rows}x{cols}):")
    for i in range(rows):
        row = input(f"第 {i+1} 行 (用空格分隔 {cols} 个数字): ").split()
        row = [int(x) for x in row]
        if len(row) != cols:
            raise ValueError(f"每行必须输入 {cols} 个数字！")
        matrix.append(row)
    return matrix

def input_vector(length, name):
    """输入向量数据"""
    print(f"\n请输入 {name} 向量 ({length} 个数字，用空格分隔):")
    vector = input().split()
    vector = [int(x) for x in vector]
    if len(vector) != length:
        raise ValueError(f"必须输入 {length} 个数字！")
    return vector

def print_matrix(matrix, name):
    """打印矩阵"""
    print(f"\n{name}:")
    for row in matrix:
        print(" ".join(map(str, row)))

def print_vector(vector, name):
    """打印向量"""
    print(f"\n{name}:")
    print(" ".join(map(str, vector)))

def banker_algorithm(Max, Need, Available, Allocated, Request, process_idx):
    # 检查 Request <= Need[process_idx]

    if not all(Request[i] <= Need[process_idx][i] for i in range(len(Request))):
        return False, Max, Need, Available, Allocated

    # 检查 Request <= Available

    if not all(Request[i] <= Available[i] for i in range(len(Request))):
        return False, Max, Need, Available, Allocated

    # 模拟分配

    temp_available = Available.copy()
    temp_allocated = [row.copy() for row in Allocated]
    temp_need = [row.copy() for row in Need]

    for i in range(len(Request)):
        temp_available[i] -= Request[i]
        temp_allocated[process_idx][i] += Request[i]
        temp_need[process_idx][i] -= Request[i]

    # 安全性检查

    work = temp_available.copy()
    finish = [False] * len(Max)
    safe_sequence = []

    while True:
        found = False
        for i in range(len(Max)):
            if not finish[i] and all(temp_need[i][j] <= work[j] for j in range(len(work))):
                for j in range(len(work)):
                    work[j] += temp_allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            break

    if all(finish):
        return True, Max, temp_need, temp_available, temp_allocated, safe_sequence
    else:
        return False, Max, Need, Available, Allocated, []

def main():
    print("===== 银行家算法 =====")
    try:
        # 输入进程数和资源数
        n_processes = int(input("\n请输入进程数: "))
        n_resources = int(input("请输入资源种类数: "))

        # 输入矩阵和向量
        Max = input_matrix(n_processes, n_resources, "Max")
        Allocated = input_matrix(n_processes, n_resources, "Allocated")
        Available = input_vector(n_resources, "Available")

        # 计算 Need 矩阵
        Need = []
        for i in range(n_processes):
            Need.append([Max[i][j] - Allocated[i][j] for j in range(n_resources)])

        # 显示初始状态
        print("\n===== 初始状态 =====")
        print_matrix(Max, "Max")
        print_matrix(Allocated, "Allocated")
        print_matrix(Need, "Need")
        print_vector(Available, "Available")

        # 输入请求
        process_idx = int(input("\n请输入请求的进程索引 (0开始): "))
        Request = input_vector(n_resources, "Request")

        # 执行银行家算法
        is_safe, new_Max, new_Need, new_Available, new_Allocated, safe_seq = banker_algorithm(
            Max, Need, Available, Allocated, Request, process_idx
        )

        # 输出结果
        print("\n===== 分配结果 =====")
        print("是否安全分配:", "是" if is_safe else "否")
        if is_safe:
            print("安全序列:", " -> ".join(map(str, safe_seq)))
        print_matrix(new_Allocated, "分配后的 Allocated")
        print_matrix(new_Need, "分配后的 Need")
        print_vector(new_Available, "分配后的 Available")

    except ValueError as e:
        print(f"输入错误: {e}")

if __name__ == "__main__":
    main()