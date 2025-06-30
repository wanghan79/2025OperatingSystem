import numpy as np


def banker_algorithm(Max, Allocated, Available, Request, process_num):
    Need = Max - Allocated

    if not (0 <= process_num < len(Allocated)):
        print("错误：进程编号无效")
        return False, Max, Allocated, Available, Need

    if not all(Request <= Need[process_num]):
        print("错误：请求超过进程最大需求")
        return False, Max, Allocated, Available, Need

    if not all(Request <= Available):
        print("错误：请求超过系统可用资源")
        return False, Max, Allocated, Available, Need

    temp_Available = Available - Request
    temp_Allocated = Allocated.copy()
    temp_Allocated[process_num] += Request
    temp_Need = Need.copy()
    temp_Need[process_num] -= Request

    work = temp_Available.copy()
    finish = [False] * len(Allocated)
    safe_sequence = []

    while True:
        found = False
        for i in range(len(Allocated)):
            if not finish[i] and all(temp_Need[i] <= work):
                work += temp_Allocated[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break

        if not found:
            break

    if all(finish):
        print("可以安全分配，安全序列：", safe_sequence)
        return True, Max, temp_Allocated, temp_Available, temp_Need
    else:
        print("无法安全分配，系统将处于不安全状态")
        return False, Max, Allocated, Available, Need


Max = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
Allocated = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
Available = np.array([3, 3, 2])
Request = np.array([1, 0, 2])
process_num = 1

result, new_Max, new_Allocated, new_Available, new_Need = banker_algorithm(Max, Allocated, Available, Request,
                                                                           process_num)

print("\n分配结果:", "成功" if result else "失败")
print("Max矩阵:\n", new_Max)
print("Allocated矩阵:\n", new_Allocated)
print("Available矩阵:\n", new_Available)
print("Need矩阵:\n", new_Need)