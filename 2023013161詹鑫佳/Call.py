import BankerAlgorithm

# 系统初始状态
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

# 计算 Need 矩阵
Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]

# 多组测试用例
test_cases = [
    {"Request": [1, 0, 2], "process_id": 1, "description": "Case 1: 正常安全请求"},
    {"Request": [7, 0, 0], "process_id": 1, "description": "Case 2: 请求超出 Need"},
    {"Request": [3, 3, 2], "process_id": 1, "description": "Case 3: 请求等于 Available，但不安全"},
    {"Request": [0, 1, 1], "process_id": 2, "description": "Case 4: 进程 P2 请求资源"},
    {"Request": [0, 0, 1], "process_id": 4, "description": "Case 5: 进程 P4 小幅度请求"}
]

# 执行所有测试用例
for case in test_cases:
    print("\n" + "-"*50)
    print(f"正在执行：{case['description']}")
    Request = case["Request"]
    process_id = case["process_id"]

    result, data = BankerAlgorithm.banker_algorithm(Max, Need, Available, Allocated, Request, process_id)

    if result:
        print("✅ 系统可满足请求。")
        print("新的 Available:", data["Available"])
        print("新的 Allocated:", data["Allocated"])
        print("新的 Need:", data["Need"])
        print("新的 Max:", data["Max"])
    else:
        print("❌", data)
