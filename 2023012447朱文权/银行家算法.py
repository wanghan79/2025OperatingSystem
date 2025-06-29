class BankerAlgorithm:
    def __init__(self, available, max_claim, allocation):
        """
        初始化银行家算法
        :param available: 可用资源向量，例如 [3, 3, 2]
        :param max_claim:  最大需求矩阵，例如 [[7, 5, 3], [3, 2, 2], ...]
        :param allocation: 已分配矩阵，例如 [[0, 1, 0], [2, 0, 0], ...]
        """
        self.available = available.copy()
        self.max_claim = [row.copy() for row in max_claim]
        self.allocation = [row.copy() for row in allocation]
        self.n = len(allocation)  # 进程数
        self.m = len(available)  # 资源种类数
        self.need = [
            [max_claim[i][j] - allocation[i][j] for j in range(self.m)]
            for i in range(self.n)
        ]

    def is_safe(self):
        """ 检查系统当前状态是否安全 """
        work = self.available.copy()
        finish = [False] * self.n
        safe_sequence = []
        found = True

        while found:
            found = False
            for i in range(self.n):
                if not finish[i]:
                    # 检查需求是否小于等于可用资源
                    can_allocate = True
                    for j in range(self.m):
                        if self.need[i][j] > work[j]:
                            can_allocate = False
                            break

                    if can_allocate:
                        # 模拟进程执行完成并释放资源
                        for j in range(self.m):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(i)
                        found = True

        # 检查所有进程是否完成
        return all(finish), safe_sequence

    def request_resources(self, pid, request):
        """
        处理进程的资源请求
        :param pid: 进程ID
        :param request: 请求向量，例如 [1, 0, 2]
        :return: 是否成功分配
        """
        # 步骤1：检查请求是否超过需求
        for j in range(self.m):
            if request[j] > self.need[pid][j]:
                return False, f"错误：请求的资源超过进程最大需求"

        # 步骤2：检查请求是否超过可用资源
        for j in range(self.m):
            if request[j] > self.available[j]:
                return False, f"错误：请求的资源超过系统可用资源"

        # 步骤3：尝试分配
        old_available = self.available.copy()
        old_allocation = self.allocation[pid].copy()
        old_need = self.need[pid].copy()

        # 模拟分配
        for j in range(self.m):
            self.available[j] -= request[j]
            self.allocation[pid][j] += request[j]
            self.need[pid][j] -= request[j]

        # 步骤4：检查安全性
        safe, sequence = self.is_safe()
        if not safe:
            # 不安全，回滚分配
            self.available = old_available
            self.allocation[pid] = old_allocation
            self.need[pid] = old_need
            return False, "拒绝分配：会导致系统不安全状态"

        return True, f"分配成功！安全序列: {sequence}"


# 测试代码
if __name__ == "__main__":
    # 初始状态设置 (5个进程，3种资源)
    available = [3, 3, 2]
    max_claim = [
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

    banker = BankerAlgorithm(available, max_claim, allocation)

    # 示例请求1：安全
    pid = 1
    request = [1, 0, 2]
    success, msg = banker.request_resources(pid, request)
    print(f"进程 {pid} 请求 {request}:")
    print(f"  -> {msg}\n")

    # 示例请求2：不安全
    pid = 4
    request = [3, 3, 0]
    success, msg = banker.request_resources(pid, request)
    print(f"进程 {pid} 请求 {request}:")
    print(f"  -> {msg}\n")

    # 示例请求3：超过需求
    pid = 0
    request = [0, 4, 0]
    success, msg = banker.request_resources(pid, request)
    print(f"进程 {pid} 请求 {request}:")
    print(f"  -> {msg}")