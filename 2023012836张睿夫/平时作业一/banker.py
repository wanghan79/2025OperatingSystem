import numpy as np

def print_state(*args):
    """打印当前系统状态"""
    available, max_table, allocation, need = args
    print("进程\tMax\tAllocation\tNeed")
    for i in range(len(max_table)):
        print("P{}\t{}\t{}\t{}".format(i, max_table[i], allocation[i], need[i]))
    print("当前剩余资源:", available)

def safety_check(*args):
    """安全检测算法"""
    available, need, allocation = args
    n = need.shape[0]
    work = available.copy()
    finish = np.array([False] * n, dtype=bool)
    safe_sequence = []

    while not (finish.all()):
        flag = False
        for i in range(n):
            if not finish[i] and (need[i] <= work).all():
                safe_sequence.append(i)
                work += allocation[i]
                finish[i] = True
                flag = True
                break
        if not flag:
            return False, []
    return True, safe_sequence

def find_safe_sequence(*args):
    """自动寻找安全序列"""
    available, need, allocation = args
    is_safe, safe_sequence = safety_check(available, need, allocation)
    if is_safe:
        print("安全序列:", safe_sequence)
    else:
        print("系统不安全，无法找到安全序列")

def check_request(*args):
    """单独判断某一条请求是否可以通过"""
    available, max_table, allocation, need, pid, request = args
    # 检查请求是否合法
    if (request > need[pid]).any():
        print("请求超过进程需求")
        return False
    if (request > available).any():
        print("请求超过可用资源")
        return False

    # 尝试分配资源
    available -= request
    allocation[pid] += request
    need[pid] -= request

    # 检查系统是否安全
    is_safe, safe_sequence = safety_check(available.copy(), need, allocation)
    if is_safe:
        print("请求通过，安全序列:", safe_sequence)
        print_state(available, max_table, allocation, need)
        return True
    else:
        print("请求不通过，系统不安全")
        # 回滚分配
        available += request
        allocation[pid] -= request
        need[pid] += request
        return False

def main():
    # 输入系统初始状态
    m = int(input("资源种类: "))
    available = np.array(input("剩余资源矩阵: ").split(), dtype=int)
    n = int(input("进程数量: "))
    max_table = np.zeros([n, m], dtype=int)
    allocation = np.zeros([n, m], dtype=int)

    for i in range(n):
        max_table[i] = np.array(input("进程 P{} 的最大需求矩阵向量：".format(i)).split(), dtype=int)

    for i in range(n):
        allocation[i] = np.array(input("进程 P{} 的分配矩阵向量：".format(i)).split(), dtype=int)
        if (max_table[i] < allocation[i]).any():
            print("输入错误：分配超过最大需求")
            i -= 1

    need = max_table - allocation
    print_state(available, max_table, allocation, need)

    # 选择模式
    while True:
        mode = input("请选择模式（1: 自动寻找安全序列, 2: 判断请求, q: 退出）: ")
        if mode == "1":
            find_safe_sequence(available, need, allocation)
        elif mode == "2":
            pid = int(input("输入进程号 (例如 0 表示 P0): "))
            request = np.array(input("输入请求资源 (例如 1 0 1): ").split(), dtype=int)
            check_request(available, max_table, allocation, need, pid, request)
        elif mode.lower() == "q":
            print("程序退出")
            break
        else:
            print("无效模式，请重新选择")

if __name__ == '__main__':
    main()
