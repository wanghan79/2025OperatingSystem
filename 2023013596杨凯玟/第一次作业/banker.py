class BankerAlgorithm:
    def __init__(self, max_resources, allocated_resources, available_resources):
        """
        初始化银行家算法
        :param max_resources: 最大需求矩阵 (n_processes x n_resources)
        :param allocated_resources: 已分配矩阵 (n_processes x n_resources)
        :param available_resources: 可用资源向量 (n_resources)
        """
        self.max = max_resources
        self.allocated = allocated_resources
        self.available = available_resources.copy()
        self.n_processes = len(max_resources)
        self.n_resources = len(available_resources)

        # 计算需求矩阵
        self.need = [
            [max_resources[i][j] - allocated_resources[i][j]
             for j in range(self.n_resources)
             for i in range(self.n_processes)
             ]]

    def is_safe_state(self):
        work = self.available.copy()
        finish = [False] * self.n_processes
        safe_sequence = []

        while True:
            found = False
            for i in range(self.n_processes):
                if not finish[i] and all(
                        self.need[i][j] <= work[j]
                        for j in range(self.n_resources)
                ):

                    for j in range(self.n_resources):
                        work[j] += self.allocated[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

            if not found:
                break

        if all(finish):
            print(f"安全状态! 安全序列: {safe_sequence}")
            return True, safe_sequence
        else:
            print("系统处于不安全状态!")
            return False, []

    def request_resources(self, process_id, request):
        """
        处理资源请求
        :param process_id: 请求资源的进程ID
        :param request: 请求资源向量
        :return: 是否允许分配
        """

        if any(request[j] > self.need[process_id][j] for j in range(self.n_resources)):
            print(f"错误：进程 {process_id} 请求超过其需求")
            return False


        if any(request[j] > self.available[j] for j in range(self.n_resources)):
            print(f"错误：进程 {process_id} 请求超过可用资源")
            return False


        old_available = self.available.copy()
        old_allocated = [row[:] for row in self.allocated]
        old_need = [row[:] for row in self.need]

        # 临时修改状态
        for j in range(self.n_resources):
            self.available[j] -= request[j]
            self.allocated[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]


        is_safe, _ = self.is_safe_state()
        if is_safe:
            print(f"允许分配资源给进程 {process_id}")
            return True
        else:
            # 回滚状态
            print("分配会导致系统不安全，已回滚")
            self.available = old_available
            self.allocated = old_allocated
            self.need = old_need
            return False

    def print_state(self):
        print("\n当前系统状态:")
        print(f"{'进程':<8}{'Max':<20}{'Allocated':<20}{'Need':<20}")
        for i in range(self.n_processes):
            print(f"P{i}:".ljust(8),
                  str(self.max[i]).ljust(20),
                  str(self.allocated[i]).ljust(20),
                  str(self.need[i]).ljust(20))
        print(f"\n可用资源: {self.available}")



if __name__ == "__main__":
    max_res = [
        [0, 0, 4, 4],
        [2, 7, 5, 0],
        [3, 6, 10, 10],
        [0, 9, 8, 4],
        [0, 6, 6, 10]
    ]
    allocated = [
        [0, 0, 3, 2],
        [2, 0, 0, 0],
        [1, 3, 5, 4],
        [0, 3, 3, 2],
        [0, 0, 1, 4]
    ]
    available = [1, 2, 1, 6]

    banker = BankerAlgorithm(max_res, allocated, available)
    banker.print_state()

    # 检查初始状态是否安全
    banker.is_safe_state()

    request = [1, 2, 2, 2]
    print(f"\n进程P2请求资源: {request}")
    if banker.request_resources(2, request):
        banker.print_state()
    else:
        print("请求被拒绝")