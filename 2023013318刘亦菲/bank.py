class BankersAlgorithm:
    """
    实现银行家算法的类。

    属性：
    - allocation：当前资源分配情况
    - max_need：每个进程的最大资源需求
    - available：系统中可用的资源
    - need：每个进程还需要的资源
    - safe_sequence：安全序列
    """

    def __init__(self, allocation, max_need, available):
        """
        构造函数。

        参数：
        - allocation：当前资源分配情况
        - max_need：每个进程的最大资源需求
        - available：系统中可用的资源

        异常：
        - ValueError：如果 allocation 和 max_need 的维度不匹配，则抛出异常
        """
        if len(allocation) != len(max_need) or len(allocation[0]) != len(max_need[0]):
            raise ValueError("allocation 和 max_need 的维度不匹配")

        self.allocation = allocation
        self.max_need = max_need
        self.available = available
        self.need = [[max_need[i][j] - allocation[i][j] for j in range(len(allocation[0]))] for i in range(len(allocation))]
        self.safe_sequence = []

    def is_safe_state(self):
        """
        判断当前状态是否安全。

        返回值：
        - bool：如果当前状态安全，则返回 True，否则返回 False
        """
        work = self.available.copy()
        finish = [False] * len(self.allocation)

        while True:
            found = False
            for i in range(len(self.allocation)):
                if not finish[i] and all(need <= work for need, work in zip(self.need[i], work)):
                    found = True
                    break

            if not found:
                break

            self.safe_sequence.append(i)
            finish[i] = True
            work = [work[j] + self.allocation[i][j] for j in range(len(self.allocation[0]))]

        return all(finish)

    def execute_bankers_algorithm(self):
        """
        执行银行家算法。

        异常：
        - ValueError：如果当前状态不安全，则抛出异常
        """
        if self.is_safe_state():
            print("安全序列：", self.safe_sequence)
        else:
            raise ValueError("当前状态不安全")


# 示例用法
allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
max_need = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
available = [3, 3, 2]

bankers_algorithm = BankersAlgorithm(allocation, max_need, available)
bankers_algorithm.execute_bankers_algorithm()