import numpy as np

def is_safe_state(available, allocated, need):
    num_processes, num_resources = need.shape
    work = available.copy()
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        progress_made = False
        for i in range(num_processes):
            if not finish[i] and all(need[i] <= work):
                work += allocated[i]
                finish[i] = True
                safe_sequence.append(i)
                progress_made = True
                break
        if not progress_made:
            return False, []

    return True, safe_sequence

def banker's_algorithm(max_resources, allocated, available, request):
    num_processes, num_resources = max_resources.shape
    need = max_resources - allocated

    if any(request > need[0]) or any(request > available):
        return False, available, allocated, need

    available_new = available - request
    allocated_new = allocated.copy()
    allocated_new[0] += request

    safe, safe_sequence = is_safe_state(available_new, allocated_new, need)
    if not safe:
        return False, available, allocated, need

    available = available_new
    allocated = allocated_new
    need = max_resources - allocated

    return True, available, allocated, need

max_resources = np.array([[7, 5, 3],
                          [3, 2, 2],
                          [9, 0, 2]])

allocated = np.array([[0, 1, 0],
                      [2, 0, 0],
                      [3, 0, 3]])

available = np.array([3, 3, 2])

request = np.array([1, 0, 2])

can_allocate, available_new, allocated_new, need_new = banker's_algorithm(max_resources, allocated, available, request)

if can_allocate:
    print(f"可用资源：{available_new}")
    print(f"已分配资源：{allocated_new}")
    print(f"Need矩阵：{need_new}")
else:
    print("请求无法被满足，系统可能进入死锁状态。")
