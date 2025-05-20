"""
@Author: Zhang Gaosheng
@Version: 1.0
@Description: 这里封装了银行家算法和安全检测的函数，以及打印矩阵的函数。
"""

def safety_check(**kwargs):
    """
        Input :
            available: 可用资源向量
            allocation: 分配矩阵
            need: 需求矩阵
        Function :
            检查系统是否处于安全状态
    """
    # 1. 获取参数
    available = kwargs['available']
    allocation = kwargs['allocation']
    need = kwargs['need']

    # 2. 初始化变量
    n = len(allocation) # 进程数
    m = len(available) # 资源数
    work = available.copy()
    finish = [False] * n
    safe_sequence = []

    # 3. 循环检查
    for _ in range(n):
        found = False
        for i in range(n):

            # 4. 检查是否是为完成且需求小于等于可用资源向量
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            break

    # 5. 返回结果
    if all(finish):
        return True, safe_sequence
    else:
        return False, []

def banker_algorithm(**kwargs):
    """
        Input :
            args: 请求进程的ID和请求资源向量
            available: 可用资源向量
            allocation: 分配矩阵
            need: 需求矩阵
        Function :
            银行家算法处理请求
    """
    # 1. 获取参数
    pid = kwargs['process_id']
    request = kwargs['request']
    available = kwargs['available']
    allocation = kwargs['allocation']
    need = kwargs['need']

    # 2. 保存原始数据，以便回滚
    original_avail = available.copy()
    original_alloc = [row.copy() for row in allocation]
    original_need = [row.copy() for row in need]

    # 3. 如果请求超过最大需求，则返回失败
    if any(request[j] > need[pid][j] for j in range(len(request))):
        return False, "失败：请求超过最大需求", original_avail, original_alloc, original_need, []
    
    # 4. 如果请求超过可用资源，则返回失败
    if any(request[j] > available[j] for j in range(len(request))):
        return False, "失败：请求超过可用资源", original_avail, original_alloc, original_need, []
    
    # 5. 从可用资源向量中减去请求向量
    new_avail = [available[j] - request[j] for j in range(len(available))]

    # 6. 从分配矩阵中增加请求向量
    new_alloc = [row.copy() for row in allocation]
    new_alloc[pid] = [new_alloc[pid][j] + request[j] for j in range(len(request))]

    # 7. 从需求矩阵中减去请求向量
    new_need = [row.copy() for row in need]
    new_need[pid] = [new_need[pid][j] - request[j] for j in range(len(request))]

    # 8. 执行安全检测
    to_safe_data = {
        'available': new_avail,
        'allocation': new_alloc,
        'need': new_need
    }
    is_safe, safe_seq = safety_check(**to_safe_data)
    if is_safe:
        return True, "成功：请求被允许", new_avail, new_alloc, new_need, safe_seq
    else:
        return False, "失败：导致不安全状态", original_avail, original_alloc, original_need, []
    
def print_matrix(**kwargs):
    """
        Input :
            title: 表格标题
            matrix: 需要打印的矩阵
            resource_names: 资源名称列表
            process_names: 进程名称列表
        Function :
            打印矩阵
    """
    # 1. 获取参数
    title = kwargs['title']
    matrix = kwargs['matrix']
    resource_names = kwargs['resource_names']
    process_names = kwargs['process_names']

    # 2. 打印矩阵
    print(f"\n{title}:")
    header = "     " + "   ".join(resource_names)
    print(header)
    for idx, row in enumerate(matrix):
        process = process_names[idx]
        formatted_row = "  ".join(f"{val:2}" for val in row)
        print(f"{process}: {formatted_row}")