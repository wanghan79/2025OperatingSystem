def banker_algorithm(Max, Allocated, Need, Available, Request):

    import copy
    Max_c = copy.deepcopy(Max)
    Allocated_c = copy.deepcopy(Allocated)
    Need_c = copy.deepcopy(Need)
    Available_c = copy.deepcopy(Available)
    
    # 解析请求
    pid, req_vector = Request
    n = len(Max_c)   
    m = len(Available_c)
    
    if any(req_vector[j] > Need_c[pid][j] for j in range(m)):
        return False, Max, Allocated, Need, Available, "错误：请求超过声明的最大需求"
    
    if any(req_vector[j] > Available_c[j] for j in range(m)):
        return False, Max, Allocated, Need, Available, "错误：请求超过可用资源，进程需等待"
    
    for j in range(m):
        Available_c[j] -= req_vector[j]
        Allocated_c[pid][j] += req_vector[j]
        Need_c[pid][j] -= req_vector[j]
    
    # 初始化工作向量和完成标记
    Work = Available_c[:]
    Finish = [False] * n
    
    # 寻找可安全执行的进程
    found = True
    while found:
        found = False
        for i in range(n):
            if not Finish[i] and all(Need_c[i][j] <= Work[j] for j in range(m)):
                # 释放进程资源
                for j in range(m):
                    Work[j] += Allocated_c[i][j]
                Finish[i] = True
                found = True
    
    # 检查所有进程是否完成
    if all(Finish):
        return True, Max_c, Allocated_c, Need_c, Available_c, "分配成功！系统处于安全状态"
    else:
        # 回滚分配
        for j in range(m):
            Available_c[j] += req_vector[j]
            Allocated_c[pid][j] -= req_vector[j]
            Need_c[pid][j] += req_vector[j]
        return False, Max, Allocated, Need, Available, "拒绝分配：分配后系统将进入不安全状态"


def print_matrices(Max, Allocated, Need, Available, title=""):

    print(f"\n{title}")
    print(f"{'进程':<6} {'Max':<15} {'Allocated':<15} {'Need':<15}")
    
    n = len(Max)
    m = len(Max[0])
    
    # 打印每个进程的资源情况
    for i in range(n):
        max_str = " ".join(f"{Max[i][j]}" for j in range(m))
        alloc_str = " ".join(f"{Allocated[i][j]}" for j in range(m))
        need_str = " ".join(f"{Need[i][j]}" for j in range(m))
        print(f"P{i:<4} [{max_str}]  [{alloc_str}]  [{need_str}]")
    
    # 打印可用资源
    avail_str = " ".join(f"{Available[j]}" for j in range(m))
    print(f"\n可用资源: [{avail_str}]")


def run_banker_example():

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
    
    Need = [
        [7, 4, 3], 
        [1, 2, 2], 
        [6, 0, 0], 
        [0, 1, 1], 
        [4, 3, 1]  
    ]
    
    Available = [3, 3, 2]
    
    print_matrices(Max, Allocated, Need, Available, "初始状态")
    
    # 测试请求1: 进程1请求资源[1, 0, 2] - 应该成功
    Request1 = (1, [1, 0, 2])
    success, Max_new, Allocated_new, Need_new, Available_new, message = banker_algorithm(
        Max, Allocated, Need, Available, Request1
    )
    
    print(f"\n请求1: 进程1请求资源 [1, 0, 2] -> {message}")
    if success:
        print_matrices(Max_new, Allocated_new, Need_new, Available_new, "分配后状态")
    
    # 测试请求2: 进程0请求资源[0, 2, 0] - 应该失败（不安全状态）
    Request2 = (0, [0, 2, 0])
    success, Max_new2, Allocated_new2, Need_new2, Available_new2, message = banker_algorithm(
        Max, Allocated, Need, Available, Request2
    )
    
    print(f"\n请求2: 进程0请求资源 [0, 2, 0] -> {message}")
    
    # 测试请求3: 进程4请求资源[3, 3, 0] - 应该失败（超过最大需求）
    Request3 = (4, [3, 3, 0])
    success, Max_new3, Allocated_new3, Need_new3, Available_new3, message = banker_algorithm(
        Max, Allocated, Need, Available, Request3
    )
    
    print(f"\n请求3: 进程4请求资源 [3, 3, 0] -> {message}")
    
    # 测试请求4: 进程3请求资源[0, 1, 0] - 应该成功
    Request4 = (3, [0, 1, 0])
    success, Max_new4, Allocated_new4, Need_new4, Available_new4, message = banker_algorithm(
        Max, Allocated, Need, Available, Request4
    )
    
    print(f"\n请求4: 进程3请求资源 [0, 1, 0] -> {message}")
    if success:
        print_matrices(Max_new4, Allocated_new4, Need_new4, Available_new4, "分配后状态")


if __name__ == "__main__":
    run_banker_example()
