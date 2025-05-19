class SafetyChecker:
    def __init__(self, available, allocation, need):
        """
        初始化安全检测器
        :param available: 可用资源向量
        :param allocation: 已分配资源矩阵
        :param need: 需求资源矩阵
        """
        self.available = available.copy()
        self.allocation = [row.copy() for row in allocation]
        self.need = [row.copy() for row in need]
        self.n_process = len(allocation)
        self.n_res = len(available)

    def check(self):
        """
        执行安全检测算法
        返回：(是否安全状态, 安全序列)
        """
        work = self.available.copy()
        finish = [False] * self.n_process
        sequence = []

        for _ in range(self.n_process):
            found = False
            for pid in range(self.n_process):
                if not finish[pid] and self.canExec(pid, work):
                    for i in range(self.n_res):
                        work[i] += self.allocation[pid][i]
                    finish[pid] = True
                    sequence.append(f"P{pid}")
                    found = True
                    break
            if not found:
                break

        return all(finish), sequence

    def canExec(self, pid, work):
        return all(self.need[pid][i] <= work[i] for i in range(self.n_res))