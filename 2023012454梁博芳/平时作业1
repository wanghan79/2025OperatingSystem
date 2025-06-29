import copy

"""
此为 操作系统课平时作业一：银行家算法

作者：梁博芳
用途：操作系统课平时作业一
"""

def is_safe(Available, Need, Allocation):
    """
    安全性检测函数，判断系统是否处于安全状态

    参数:
        Available: 当前可用资源向量
        Need: 每个进程尚需资源矩阵
        Allocation: 当前资源分配矩阵

    返回:
        bool: 系统是否处于安全状态
    """
    n = len(Need)  # 进程数量
    m = len(Available)  # 资源种类数
    Work = Available[:]
    finished = [False] * n
    while True:
        found = False
        for i in range(n):
            if not finished[i] and all(Need[i][j] <= Work[j] for j in range(m)):
                # 可以释放该进程资源
                Work = [Work[j] + Allocation[i][j] for j in range(m)]
                finished[i] = True
                found = True
        if not found:
            break
    return all(finished)


def banker(Max, Need, Available, Allocation, Request, pid):
    """
    银行家算法核心逻辑

    参数:
        Max: 每个进程的最大资源需求矩阵
        Need: 每个进程的剩余需求矩阵（Max - Allocation）
        Available: 当前可用资源向量
        Allocation: 当前资源分配矩阵
        Request: 请求资源向量
        pid: 请求进程编号

    返回:
        dict: 包含分配结果的状态信息
    """
    m = len(Available)

    # 检查请求是否超过进程所需
    if any(Request[j] > Need[pid][j] for j in range(m)):
        return {
            "state": False,
            "info": "请求超出该进程所需资源"
        }

    # 检查请求是否超过当前可用资源
    if any(Request[j] > Available[j] for j in range(m)):
        return {
            "state": False,
            "info": "系统当前资源不足"
        }

    # 尝试分配资源
    new_Available = [Available[j] - Request[j] for j in range(m)]
    new_Allocation = copy.deepcopy(Allocation)
    new_Allocation[pid] = [new_Allocation[pid][j] + Request[j] for j in range(m)]
    new_Need = copy.deepcopy(Need)
    new_Need[pid] = [new_Need[pid][j] - Request[j] for j in range(m)]

    # 判断新状态是否安全
    if is_safe(new_Available, new_Need, new_Allocation):
        return {
            "state": True,
            "info": {
                "Available": new_Available,
                "Allocation": new_Allocation,
                "Need": new_Need,
                "Max": Max
            }
        }
    else:
        return {
            "state": False,
            "info": "请求后系统不安全，拒绝分配"
        }


def print_matrix(matrix):
    """打印二维矩阵"""
    for row in matrix:
        print("  ", row)


def main():
    print("=== 银行家算法模拟程序 ===")

    # 输入示例数据或手动输入
    use_example = input("使用默认示例？(y/n): ").lower() == 'y'

    if use_example:
        # 示例数据
        Available = [3, 3, 2]
        Max = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]
        Allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]
        Need = [[Max[i][j] - Allocation[i][j] for j in range(len(Available))] for i in range(len(Max))]
        Request = [1, 0, 2]
        pid = 1
    else:
        # 手动输入
        n = int(input("请输入进程数量: "))
        m = int(input("请输入资源种类数量: "))
        Available = list(map(int, input(f"请输入初始可用资源向量 (共 {m} 个数字): ").split()))
        Max = []
        Allocation = []
        print("请输入每个进程的最大资源需求:")
        for i in range(n):
            Max.append(list(map(int, input(f"P{i} Max: ").split())))
        print("请输入当前资源分配情况:")
        for i in range(n):
            Allocation.append(list(map(int, input(f"P{i} Allocation: ").split())))
        Need = [[Max[i][j] - Allocation[i][j] for j in range(m)] for i in range(n)]
        pid = int(input("请输入请求进程编号: "))
        Request = list(map(int, input("请输入请求资源向量: ").split()))

    result = banker(Max, Need, Available, Allocation, Request, pid)

    if result["state"]:
        print("\n✅ 请求可以被安全满足！新的系统状态为：")
        res_info = result["info"]
        print("Available:", res_info["Available"])
        print("Allocation:")
        print_matrix(res_info["Allocation"])
        print("Need:")
        print_matrix(res_info["Need"])
    else:
        print("\n❌ 请求被拒绝：", result["info"])


if __name__ == "__main__":
    main()

