# # 银行家算法

# 判断是否为安全序列
def is_safe_state(available, max_need, allocation):
    num_processes = len(max_need)
    num_resources = len(available)
    
    # 计算need矩阵
    need = [[max_need[i][j] - allocation[i][j] for j in range(num_resources)] for i in range(num_processes)]
    
    work = available[:]    # 工作向量，系统可提供给进程继续运行的资源数量
    finish = [False] * num_processes     # 系统是否有足够资源分配给进程
    safe_sequence = []    # 安全序列
    
    while len(safe_sequence) < num_processes:
        found = False
        for i in range(num_processes):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(num_resources)):
                    work = [work[j] + allocation[i][j] for j in range(num_resources)]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
        if not found:
            return False, []  # 处于不安全状态
    
    return True, safe_sequence

def banker_algorithm(max_need, need, available, allocation, request): 
    num_processes = len(max_need)
    num_resources = len(available)
    process_id = -1  # 假设请求是针对特定的流程

    for i in range(num_processes):
        if all(request[j] <= need[i][j] for j in range(num_resources)) and all(request[j] <= available[j] for j in range(num_resources)):
            process_id = i
            break

    if process_id == -1:
        return "错误：请求超出需求或可用资源", None, None, None, None
    
    
    if all(request[j] <= available[j] for j in range(num_resources)):
        
        # 临时分配请求的资源
        available_temp = [available[j] - request[j] for j in range(num_resources)]
        allocation_temp = [row[:] for row in allocation]
        need_temp = [row[:] for row in need]
        
        for j in range(num_resources):
            allocation_temp[process_id][j] += request[j]
            need_temp[process_id][j] -= request[j]
        
        # 检查假设分配后的系统安全性
        safe, _ = is_safe_state(available_temp, max_need, allocation_temp)
        if safe:
            available[:] = available_temp
            allocation[:] = allocation_temp
            need[:] = need_temp
            return "可以完成本次分配，系统处于安全状态", available, max_need, allocation, [[max_need[i][j] - allocation[i][j] for j in range(num_resources)] for i in range(num_processes)]
        else:
            return "不可以完成本次分配，系统处于不安全状态", available, max_need, allocation, need
    else:
        return "请求超出可用资源", available, max_need, allocation, need

# 样例
Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
Available = [3, 3, 2]
Allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
Request = [1, 0, 2]  

result, new_available, new_max, new_allocation, new_need = banker_algorithm(Max, Need, Available, Allocated, Request)
print(result)
if new_available is not None:
    print("New Available:", new_available)
    print("New Max:", new_max)
    print("New Allocation:", new_allocation)
    print("New Need:", new_need)