import numpy as np

def banker_algorithm(Max, Need, Available, Allocated, Request, process_id):
    Max = np.array(Max)
    Need = np.array(Need)
    Available = np.array(Available)
    Allocated = np.array(Allocated)
    Request = np.array(Request)

    # 检查请求是否小于 Need
    if not np.all(Request <= Need[process_id]):
        return False, "错误：请求超出了规定的需求范围。"

    # 检查请求是否小于 Available
    if not np.all(Request <= Available):
        return False, "错误：请求超出可用资源。v"

    # 尝试分配
    Available_temp = Available - Request
    Allocated_temp = Allocated.copy()
    Allocated_temp[process_id] += Request
    Need_temp = Need.copy()
    Need_temp[process_id] -= Request

    # 安全性检查
    Finish = [False] * len(Allocated)
    Work = Available_temp.copy()

    while True:
        found = False
        for i in range(len(Finish)):
            if not Finish[i] and np.all(Need_temp[i] <= Work):
                Work += Allocated_temp[i]
                Finish[i] = True
                found = True
        if not found:
            break

    if all(Finish):
        return True, {
            "Available": Available_temp.tolist(),
            "Allocated": Allocated_temp.tolist(),
            "Need": Need_temp.tolist(),
            "Max": Max.tolist()
        }
    else:
        return False, "Request leads to unsafe state. Cannot allocate."
