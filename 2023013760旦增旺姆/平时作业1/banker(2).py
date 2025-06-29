class BankersAlgorithm:
    def __init__(self, max_resources, allocated_resources, max_needs):
        """
        初始化银行家算法所需的资源分配表、最大需求表和资源总数。
        :param max_resources: 系统中每种资源的最大数量（列表）。
        :param allocated_resources: 当前已经分配给每个进程的资源数量（二维列表）。
        :param max_needs: 每个进程的最大需求（二维列表）。
        """
        self.max_resources = max_resources  # 系统中每种资源的最大数量
        self.allocated_resources = allocated_resources  # 已分配给每个进程的资源
        self.max_needs = max_needs  # 每个进程的最大资源需求
        self.num_processes = len(allocated_resources)  # 进程数
        self.num_resources = len(max_resources)  # 资源种类数

        # 计算剩余需求 = 最大需求 - 已分配资源
        self.remaining_needs = [[self.max_needs[i][j] - self.allocated_resources[i][j]
                                 for j in range(self.num_resources)]
                                for i in range(self.num_processes)]

        # 系统当前可用资源 = 系统总资源 - 所有进程已分配的资源总和
        self.available_resources = [
            self.max_resources[j] - sum(self.allocated_resources[i][j] for i in range(self.num_processes))
            for j in range(self.num_resources)]

    def is_safe(self):
        """
        检查系统是否处于安全状态。
        :return: 如果处于安全状态，返回 True；否则返回 False。
        """
        work = self.available_resources[:]  # 当前可用资源
        finish = [False] * self.num_processes  # 进程是否完成标记
        safe_sequence = []  # 安全序列

        while len(safe_sequence) < self.num_processes:
            progress_made = False
            for i in range(self.num_processes):
                if not finish[i]:  # 如果进程 i 还没有完成
                    # 检查进程 i 是否能顺利完成（需求小于等于当前可用资源）
                    if all(self.remaining_needs[i][j] <= work[j] for j in range(self.num_resources)):
                        # 将进程 i 完成后的资源释放回系统
                        work = [work[j] + self.allocated_resources[i][j] for j in range(self.num_resources)]
                        finish[i] = True
                        safe_sequence.append(i)
                        progress_made = True
                        break
            if not progress_made:
                return False, []  # 没有进程可以继续执行，系统进入死锁状态
        return True, safe_sequence  # 返回安全序列

    def request_resources(self, process_index, request):
        """
        请求资源。
        :param process_index: 进程的索引（从0开始）。
        :param request: 该进程请求的资源量（列表）。
        :return: 如果请求成功，返回 True；如果请求导致死锁，返回 False。
        """
        # 检查请求是否合法
        if any(request[j] > self.max_needs[process_index][j] for j in range(self.num_resources)):
            print(f"Process {process_index} has requested more than its maximum need!")
            return False
        if any(request[j] > self.available_resources[j] for j in range(self.num_resources)):
            print(f"Not enough resources available for process {process_index}!")
            return False

        # 预分配资源
        for j in range(self.num_resources):
            self.available_resources[j] -= request[j]
            self.allocated_resources[process_index][j] += request[j]
            self.remaining_needs[process_index][j] -= request[j]

        # 检查是否进入安全状态
        safe, safe_sequence = self.is_safe()
        if safe:
            print(f"Resources allocated to process {process_index} successfully.")
            return True
        else:
            # 回滚资源分配
            for j in range(self.num_resources):
                self.available_resources[j] += request[j]
                self.allocated_resources[process_index][j] -= request[j]
                self.remaining_needs[process_index][j] += request[j]
            print(f"Request by process {process_index} leads to unsafe state, allocation rolled back.")
            return False


# 测试代码
def main():
    # 修正后的测试数据（满足 allocated <= max_resources 且 max_needs 合理）
    max_resources = [10, 5, 7]
    allocated_resources = [
        [1, 1, 2],  # 进程 0
        [2, 0, 1],  # 进程 1
        [0, 1, 0]   # 进程 2
    ]
    max_needs = [
        [5, 3, 3],  # 进程 0
        [3, 2, 2],  # 进程 1
        [4, 1, 2]   # 进程 2
    ]

    bankers = BankersAlgorithm(max_resources, allocated_resources, max_needs)

    # 检查初始状态
    safe, sequence = bankers.is_safe()
    print(f"Initial safe state: {safe}, Safe sequence: {sequence}")  # 应输出 True

    # 进程 1 请求资源 [1, 0, 1]
    request = [1, 0, 1]
    if bankers.request_resources(1, request):
        print("Request granted. New safe sequence:", bankers.is_safe()[1])
    else:
        print("Request denied.")

if __name__ == "__main__":
    main()



