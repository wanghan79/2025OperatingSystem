def banker_algorithm(Max, Need, Available, Allocated, Request):
    pid, request = Request
    n = len(Max)
    m = len(Available)

    original_Need = [row[:] for row in Need]
    original_Available = Available[:]
    original_Allocated = [row[:] for row in Allocated]

    if any(request[j] > Need[pid][j] for j in range(m)):
        return "分配失败：请求超过需求", Max, original_Need, original_Available, original_Allocated

    if any(request[j] > Available[j] for j in range(m)):
        return "分配失败：请求超过可用资源", Max, original_Need, original_Available, original_Allocated

    new_Available = [Available[j] - request[j] for j in range(m)]
    new_Allocated = [row[:] for row in Allocated]
    for j in range(m):
        new_Allocated[pid][j] += request[j]
    new_Need = [row[:] for row in Need]
    for j in range(m):
        new_Need[pid][j] -= request[j]

    work = new_Available[:]
    finish = [False] * n
    safe_sequence = []

    found = True
    while found:
        found = False
        for i in range(n):
            if not finish[i] and all(new_Need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += new_Allocated[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True

    if all(finish):
        return (f"分配成功！安全序列: {safe_sequence}",
                Max, new_Need, new_Available, new_Allocated)
    else:
        return "分配失败：系统将进入不安全状态", Max, original_Need, original_Available, original_Allocated


if __name__ == "__main__":
    Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    Allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
    Available = [3, 3, 2]
    Request = (1, [1, 0, 2])

    result, Max_out, Need_out, Available_out, Allocated_out = banker_algorithm(
        Max, Need, Available, Allocated, Request
    )

    # 优化输出
    print(result)
    print("\n分配后系统状态：\n")

    # 找出每列的最大宽度以便对齐
    width = 5  # 设置每列的默认宽度

    # 打印表头
    header = " Max" + " " * (width * len(Max[0]) - 4) + "| Allocated" + " " * (width * len(Allocated[0]) - 10) + "| Need" + " " * (width * len(Need[0]) - 5) + "| Available"
    print(header)
    print("-" * len(header))

    # 打印每行内容
    available_str = "".join(f"{num:<{width}}" for num in Available_out)
    for max_row, allocated_row, need_row in zip(Max_out, Allocated_out, Need_out):
        max_str = "".join(f"{num:<{width}}" for num in max_row)
        allocated_str = "".join(f"{num:<{width}}" for num in allocated_row)
        need_str = "".join(f"{num:<{width}}" for num in need_row)
        print(f"{max_str}|{allocated_str}|{need_str}|{available_str}")