import numpy as np


def printt(available, max_table, allocation, need):
    print("进程\tMax\tAllocation\tNeed")
    for i in range(5):
        print("P{}\t{}\t{}\t{}".format(i, max_table[i], allocation[i], need[i]))
    print("当前剩余资源:", available)


def anquan(work, need, allocation):
    n = need.shape[0]
    finish = np.array([False] * n, dtype=bool)
    while not (finish.all()):
        flag = False
        for i in range(n):
            if not finish[i] and (need[i] <= work).all():
                print("安全序列P{}".format(i), end=',')
                flag = True
                work += allocation[i]
                finish[i] = True
                break
        if not flag: return False
    print()
    return True


def main():
    m = int(input("资源种类: "))
    tt = input("各类资源的数量：").split()
    available = np.array(tt, dtype=int)
    n = int(input("进程数量: "))
    max = np.zeros([n, m], dtype=int)
    allocation = np.zeros([n, m], dtype=int)

    for i in range(n):
        tt = input("进程 P{} 的最大需求矩阵向量：".format(i)).split()
        max[i] = np.array(tt, dtype=int)
        if (available < max[i]).any():
            print("输入错误")
            i -= 1

    for i in range(n):
        tt = input("进程 P{} 的分配矩阵向量：".format(i)).split()
        allocation[i] = np.array(tt, dtype=int)
        if (max[i] < allocation[i]).any():
            print("输入错误")
            i -= 1

    need = max - allocation

    for i in allocation:
        available -= i  # 剩余资源

    printt(available, max, allocation, need)

    while (need != 0).any():
        pid, qq = input("输入请求: ").split(',')
        pid = int(pid[1:])
        qq = np.array(qq.split(), dtype=int)

        if (qq > max[pid]).any():
            print("输入错误")

        else:
            available -= qq
            allocation[pid] += qq
            need[pid] -= qq
            if anquan(available.copy(), need, allocation):
                printt(available, max, allocation, need)
                continue
            else:
                print("不安全 不可分配")
                available += qq
                allocation[pid] -= qq
                need[pid] += qq


if __name__ == '__main__':
    main()