import BankerAlgorithm

Max = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]

Allocated = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

Available = [3, 3, 2]

# 计算 Need
Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]

Request = [1, 0, 2]  # P1 请求
process_id = 1

result, data = BankerAlgorithm.banker_algorithm(Max, Need, Available, Allocated, Request, process_id)
if result:
    print("✅ 系统可满足请求。")
    print("新的 Available:", data["Available"])
    print("新的 Allocated:", data["Allocated"])
    print("新的 Need:", data["Need"])
    print("新的 Max:", data["Max"])
else:
    print("❌", data)
