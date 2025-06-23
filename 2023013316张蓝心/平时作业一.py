class BankersAlgorithm:
    def __init__(self, max_claim, allocation, available):
        """
        初始化银行家算法

        参数:
        max_claim -- 最大需求矩阵 (n_processes × n_resources)
        allocation -- 已分配矩阵 (n_processes × n_resources)
        available -- 可用资源向量 (n_resources,)
        """
        self.max_claim = max_claim
        self.allocation = allocation
        self.available = available
        self.n_processes = len(max_claim)
        self.n_resources = len(available)

        # 计算需求矩阵
        self.need = [
            [max_claim[i][j] - allocation[i][j]
             for j in range(self.n_resources)]
            for i in range(self.n_processes)
        ]

    def is_safe(self):
        """检查系统是否处于安全状态"""
        work = self.available.copy()
        finish = [False] * self.n_processes
        safe_seq = []
        count = 0

        while count < self.n_processes:
            found = False
            for i in range(self.n_processes):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.n_resources)):
                    # 释放资源
                    for j in range(self.n_resources):
                        work[j] += self.allocation[i][j]

                    finish[i] = True
                    safe_seq.append(i)
                    count += 1
                    found = True

            if not found:
                break

        return safe_seq if count == self.n_processes else None

    def request_resources(self, process_id, request):
        """
        处理资源请求

        参数:
        process_id -- 请求资源的进程ID
        request -- 请求的资源向量 (n_resources,)

        返回:
        (success, new_max, new_alloc, new_need, new_avail, safe_seq)
        success: 是否分配成功
        四个矩阵的新状态和安全序列(如果成功)
        """
        # 验证输入
        if process_id < 0 or process_id >= self.n_processes:
            return False, None, None, None, None, None

        if len(request) != self.n_resources:
            return False, None, None, None, None, None

        # 检查请求是否超过需求
        if any(request[j] > self.need[process_id][j] for j in range(self.n_resources)):
            return False, None, None, None, None, None

        # 检查系统是否有足够资源
        if any(request[j] > self.available[j] for j in range(self.n_resources)):
            return False, None, None, None, None, None

        # 尝试分配资源
        new_available = self.available.copy()
        new_allocation = [row.copy() for row in self.allocation]
        new_need = [row.copy() for row in self.need]

        for j in range(self.n_resources):
            new_available[j] -= request[j]
            new_allocation[process_id][j] += request[j]
            new_need[process_id][j] -= request[j]

        # 临时创建对象检查安全性
        temp_banker = BankersAlgorithm(self.max_claim, new_allocation, new_available)
        safe_seq = temp_banker.is_safe()

        if safe_seq is not None:
            # 分配成功，更新状态
            self.available = new_available
            self.allocation = new_allocation
            self.need = new_need

            return True, self.max_claim, self.allocation, self.need, self.available, safe_seq
        else:
            # 分配会导致不安全状态，不更新实际状态
            return False, None, None, None, None, None

    def get_current_state(self):
        """获取当前系统状态"""
        return {
            'max_claim': [row.copy() for row in self.max_claim],
            'allocation': [row.copy() for row in self.allocation],
            'need': [row.copy() for row in self.need],
            'available': self.available.copy()
        }



if __name__ == "__main__":
    # 举例
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

    available = [3, 3, 2]

    # 创建银行家算法实例
    banker = BankersAlgorithm(max_claim, allocation, available)

    # 示例请求1: P1请求(1,0,2) - 应该成功
    print("示例1: P1请求(1,0,2)")
    success, new_max, new_alloc, new_need, new_avail, safe_seq = banker.request_resources(1, [1, 0, 2])

    if success:
        print("分配成功!")
        print("安全序列:", ' -> '.join(f'P{i}' for i in safe_seq))
        print("分配后的状态:")
        print("Max:", new_max)
        print("Allocation:", new_alloc)
        print("Need:", new_need)
        print("Available:", new_avail)
    else:
        print("分配失败!")

    print("\n示例2: P0请求(0,2,0) - 应该失败(会导致不安全)")
    success, new_max, new_alloc, new_need, new_avail, safe_seq = banker.request_resources(0, [0, 2, 0])

    if success:
        print("分配成功!")
        print("安全序列:", ' -> '.join(f'P{i}' for i in safe_seq))
    else:
        print("分配失败!")

    print("\n当前系统状态:")
    state = banker.get_current_state()
    print("Max:", state['max_claim'])
    print("Allocation:", state['allocation'])
    print("Need:", state['need'])
    print("Available:", state['available'])