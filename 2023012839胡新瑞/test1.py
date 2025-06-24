def bankers_algorithm(Max, Need, Available, Allocated, Request, process_id):
 
   
    for i in range(len(Request)):
        if Request[i] > Need[process_id][i]:
            print("错误：请求超过进程声明的最大需求")
            return False, Max, Need, Available, Allocated
    

    for i in range(len(Request)):
        if Request[i] > Available[i]:
            print("拒绝：可用资源不足")
            return False, Max, Need, Available, Allocated
    
  
    temp_Available = Available.copy()
    temp_Allocated = [row.copy() for row in Allocated]
    temp_Need = [row.copy() for row in Need]
    
    for i in range(len(Request)):
        temp_Available[i] -= Request[i]
        temp_Allocated[process_id][i] += Request[i]
        temp_Need[process_id][i] -= Request[i]
    

    def is_safe(avail, alloc, need):
        work = avail.copy()
        finish = [False] * len(alloc)
        safe_seq = []
        
      
        while True:
            found = False
            for i in range(len(alloc)):
                if not finish[i]:
                    # 检查该进程所有资源需求是否<=当前可用
                    satisfy = all(need[i][j] <= work[j] for j in range(len(work)))
                    if satisfy:
                        # 模拟资源释放
                        for j in range(len(work)):
                            work[j] += alloc[i][j]
                        finish[i] = True
                        safe_seq.append(i)
                        found = True
            
            if not found:
                break
        
    
        return all(finish), safe_seq
    
  
    safe, sequence = is_safe(temp_Available, temp_Allocated, temp_Need)
    
    if safe:
        print(f"允许分配，安全序列: {sequence}")
        return True, Max, temp_Need, temp_Available, temp_Allocated
    else:
        print("拒绝：分配后系统将处于不安全状态")
        return False, Max, Need, Available, Allocated



if __name__ == "__main__":
   
    Max = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3]   # P4
    ]
    
    Allocated = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]   # P4
    ]
    
   
    Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]
    
    Available = [3, 3, 2]  # 可用资源
    
    # 测试案例1：P1请求[1,0,2]
    print("测试案例1：P1请求[1,0,2]")
    result, new_Max, new_Need, new_Available, new_Allocated = bankers_algorithm(
        Max, Need, Available, Allocated, [1, 0, 2], 1
    )
    
    if result:
        print("\n分配后状态：")
        print("可用资源:", new_Available)
        print("已分配矩阵:")
        for row in new_Allocated:
            print(row)
        print("需求矩阵:")
        for row in new_Need:
            print(row)
