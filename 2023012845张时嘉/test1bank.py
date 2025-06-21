def banker_algorithm(Max, Need, Available, Allocated, Request, process_id):
    
    work = Available.copy()
    finish = [False] * len(Need)
    safe_sequence = []
    
    if (Request > Need[process_id]).any():
        return False, None, None, None, None, "请求超过最大需求"
    
    if (Request > work).any():
        return False, None, None, None, None, "可用资源不足"
    
    temp_allocated = Allocated.copy()
    temp_allocated[process_id] += Request
    temp_need = Need.copy()
    temp_need[process_id] -= Request
    temp_available = work - Request
    
    while True:
        found = False
        for i in range(len(finish)):
            if not finish[i] and (temp_need[i] <= work).all():
                work += temp_allocated[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True
        if not found:
            break
    
    if all(finish):
        Allocated[process_id] += Request
        Need[process_id] -= Request
        Available -= Request
        return True, Allocated, Need, Available, safe_sequence, "分配安全"
    else:
        return False, None, None, None, None, "分配不安全"

if __name__ == "__main__":
    Max = [[7, 5, 3, 4],   
           [3, 2, 2, 2],   
           [9, 0, 1, 3]]   
    
    Allocated = [[0, 1, 0, 0],  
                 [2, 0, 0, 1],  
                 [3, 0, 1, 0]]  
    
    Available = [3, 3, 2, 1]  
    Need = [[row[0]-allocated[0], row[1]-allocated[1], row[2]-allocated[2], row[3]-allocated[3]] 
            for row, allocated in zip(Max, Allocated)]
    
    Request = [1, 0, 0, 2]
    process_id = 0
    
    result, new_allocated, new_need, new_available, sequence, msg = \
        banker_algorithm(Max, Need, Available, Allocated, Request, process_id)
    
    print(f"分配结果：{result}")
    print(f"消息：{msg}")
    if result:
        print("安全序列：", sequence)
        print("新分配矩阵：", new_allocated)
        print("新需求矩阵：", new_need)
        print("新可用资源：", new_available)
