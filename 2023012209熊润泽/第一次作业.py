import numpy as np

def print_resources_status(available: np.ndarray, max_demand: np.ndarray, allocation: np.ndarray) -> None:
    print("\n进程\tMax\t\tAllocation\tNeed")
    for i in range(len(max_demand)):
        print(f"P{i}\t{max_demand[i]}\t\t{allocation[i]}\t\t{max_demand[i] - allocation[i]}")
    print(f"当前剩余资源: {available}")

def is_safe_state(available: np.ndarray, need: np.ndarray, allocation: np.ndarray) -> bool:
    n = len(need)
    work = available.copy()
    finish = np.zeros(n, dtype=bool)
    safe_seq = []
    
    while True:
        found = False
        for i in range(n):
            if not finish[i] and (need[i] <= work).all():
                work += allocation[i]
                finish[i] = True
                safe_seq.append(i)
                found = True
                break
        if not found:
            break
    
    if finish.all():
        print(f"安全序列: {[f'P{i}' for i in safe_seq]}")
        return True
    return False

def get_valid_input(prompt: str, m: int, max_vals: np.ndarray = None) -> np.ndarray:
    while True:
        try:
            input_str = input(prompt)
            values = np.array(input_str.split(), dtype=int)
            
            if len(values) != m:
                raise ValueError(f"必须提供{m}个整数")
                
            if (values < 0).any():
                raise ValueError("所有值必须是非负整数")
                
            if max_vals is not None and (values > max_vals).any():
                raise ValueError("输入值超过最大限制")
                
            return values
        except ValueError as e:
            print(f"输入错误：{str(e)}")

def main():
    m = int(input("资源种类: "))
    total_resources = get_valid_input(
        f"请输入{m}种资源的总数量（用空格分隔）: ", m
    )
    
    n = int(input("进程数量: "))
    max_demand = np.zeros((n, m), dtype=int)
    allocation = np.zeros((n, m), dtype=int)
    
    for i in range(n):
        max_demand[i] = get_valid_input(
            f"进程 P{i} 的最大需求矩阵向量（{m}个整数）: ", m
        )
    
    for i in range(n):
        allocation[i] = get_valid_input(
            f"进程 P{i} 的分配矩阵向量（{m}个整数）: ", m, max_demand[i]
        )
    
    available = total_resources - np.sum(allocation, axis=0)
    
    print_resources_status(available, max_demand, allocation)
    
    while (max_demand - allocation).any():
        request_input = input("\n输入请求 (格式: P0,1 2 3)，输入q退出: ")
        if request_input.lower() == 'q':
            break
            
        try:
            pid_part, request_part = request_input.split(',')
            pid = int(pid_part[1:])
            request = np.array(request_part.strip().split(), dtype=int)
            
            if pid < 0 or pid >= n:
                raise ValueError("无效的进程ID")
                
            if len(request) != m:
                raise ValueError(f"请求的资源数量必须为{m}个")
                
            need = max_demand[pid] - allocation[pid]
            if (request > need).any():
                raise ValueError("请求超过最大需求")
                
            if (request > available).any():
                raise ValueError("请求超过可用资源")
                
            available_temp = available - request
            allocation_temp = allocation.copy()
            allocation_temp[pid] += request
            need_temp = max_demand - allocation_temp
            
            if is_safe_state(available_temp, need_temp, allocation_temp):
                print("分配成功")
                available = available_temp
                allocation = allocation_temp
                print_resources_status(available, max_demand, allocation)
            else:
                print("分配失败：系统将进入不安全状态")
                
        except (ValueError, IndexError) as e:
            print(f"输入错误：{str(e)}")

if __name__ == '__main__':
    main()    
