
def initialize():
    available = [3, 3, 2]
    
    max_demand = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    
    need = []
    for i in range(len(max_demand)):
        need.append([max_demand[i][j] - allocation[i][j] for j in range(len(available))])
    
    return available, max_demand, allocation, need

def is_safe(available, allocation, need):
    n = len(allocation)
    m = len(available)
    
    work = available.copy()
    finish = [False] * n
    
    safe_sequence = []
    
    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        
        if not found:
            break
    
    if all(finish):
        print("系统处于安全状态，安全序列为:", safe_sequence)
        return True
    else:
        print("系统处于不安全状态")
        return False

def resource_request(available, allocation, need, process_num, request):
    m = len(available)
    
    if any(request[j] > need[process_num][j] for j in range(m)):
        print("错误：进程请求的资源超过其声明的最大需求")
        return False
    
    if any(request[j] > available[j] for j in range(m)):
        print("错误：请求的资源超过系统可用资源，进程必须等待")
        return False
    
    new_available = available.copy()
    new_allocation = [row.copy() for row in allocation]
    new_need = [row.copy() for row in need]
    
    for j in range(m):
        new_available[j] -= request[j]
        new_allocation[process_num][j] += request[j]
        new_need[process_num][j] -= request[j]
    
    if is_safe(new_available, new_allocation, new_need):
        for j in range(m):
            available[j] = new_available[j]
            allocation[process_num][j] = new_allocation[process_num][j]
            need[process_num][j] = new_need[process_num][j]
        print("资源分配成功")
        return True
    else:
        print("资源分配会导致系统进入不安全状态，拒绝分配")
        return False

def display_status(available, allocation, need):
    print("\n当前系统状态:")
    print("可用资源:", available)
    print("\n分配矩阵:")
    for row in allocation:
        print(row)
    print("\n需求矩阵:")
    for row in need:
        print(row)

def main():
    available, max_demand, allocation, need = initialize()
    
    while True:
        display_status(available, allocation, need)
        print("\n1. 请求资源")
        print("2. 检查安全性")
        print("3. 退出")
        choice = input("请选择操作: ")
        
        if choice == '1':
            process_num = int(input("请输入进程号(0开始): "))
            request = list(map(int, input("请输入请求资源(用空格分隔): ").split()))
            resource_request(available, allocation, need, process_num, request)
        elif choice == '2':
            is_safe(available.copy(), allocation, need)
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
