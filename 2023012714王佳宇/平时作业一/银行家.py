class BankersAlgorithm:
    """
    银行家算法实现类，包含安全检测算法
    通过资源请求模拟和安全性检查避免死锁
    """
    
    def __init__(self, available, max_need, allocation):
        """
        初始化银行家算法所需数据结构
        :param available: 可用资源向量 (列表)
        :param max_need: 最大需求矩阵 (二维列表)
        :param allocation: 已分配矩阵 (二维列表)
        """
        self.available = available.copy()
        self.max_need = [row.copy() for row in max_need]
        self.allocation = [row.copy() for row in allocation]
        self.need = [
            [max_need[i][j] - allocation[i][j] 
             for j in range(len(available))]
            for i in range(len(max_need))
        ]
        self.process_num = len(max_need)
        self.resource_type = len(available)

    def is_safe(self):
        """
        安全检测算法实现
        :return: (是否安全, 安全序列)
        """
        work = self.available.copy()
        finish = [False] * self.process_num
        safe_sequence = []
        count = 0  # 防止无限循环

        while count < self.process_num * 2:  # 最多循环2n次防止死循环
            found = False
            for i in range(self.process_num):
                # 查找未完成且需求可满足的进程
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.resource_type)):
                    # 模拟资源分配并回收
                    for j in range(self.resource_type):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
            if not found:
                break
            count += 1

        return all(finish), safe_sequence

    def request_resources(self, process_id, request):
        """
        处理资源请求的完整流程
        :param process_id: 请求资源的进程ID
        :param request: 请求资源向量
        :return: (是否批准, 响应信息)
        """
        # 输入有效性验证
        if process_id < 0 or process_id >= self.process_num:
            return False, f"无效进程ID: {process_id}"

        # 步骤1: 检查请求是否超过声明的最大需求
        if any(request[j] > self.need[process_id][j] for j in range(self.resource_type)):
            return False, "错误：请求超过进程最大需求"

        # 步骤2: 检查请求是否超过可用资源
        if any(request[j] > self.available[j] for j in range(self.resource_type)):
            return False, "错误：请求超过当前可用资源"

        # 步骤3: 尝试分配资源
        temp_available = [self.available[j] - request[j] for j in range(self.resource_type)]
        temp_allocation = [row.copy() for row in self.allocation]
        temp_allocation[process_id] = [
            temp_allocation[process_id][j] + request[j] 
            for j in range(self.resource_type)
        ]
        temp_need = [row.copy() for row in self.need]
        temp_need[process_id] = [
            temp_need[process_id][j] - request[j] 
            for j in range(self.resource_type)
        ]

        # 创建临时银行家实例进行安全检查
        temp_banker = BankersAlgorithm(
            temp_available,
            self.max_need,
            temp_allocation
        )

        # 步骤4: 执行安全检测
        is_safe, _ = temp_banker.is_safe()
        
        if is_safe:
            # 正式分配资源
            self.available = temp_available
            self.allocation = temp_allocation
            self.need = temp_need
            return True, "请求批准：系统保持安全状态"
        else:
            return False, "请求拒绝：分配后系统将进入不安全状态"


if __name__ == "__main__":
    # ================== 示例用法 ==================
    # 系统初始状态
    available = [3, 3, 2]  # 可用资源向量
    max_need = [           # 最大需求矩阵
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3],  # P4
    ]
    allocation = [          # 已分配矩阵
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2],  # P4
    ]

    # 初始化银行家算法实例
    banker = BankersAlgorithm(available, max_need, allocation)

    # 显示初始安全状态
    is_safe_init, seq_init = banker.is_safe()
    print("[初始状态]")
    print(f"安全状态: {is_safe_init}")
    print(f"安全序列: {seq_init}\n")

    # 测试请求1: 合法安全请求 (P1请求[1, 0, 2])
    process_id = 1
    request = [1, 0, 2]
    success, msg = banker.request_resources(process_id, request)
    print(f"[请求处理] 进程P{process_id} 请求资源: {request}")
    print(f"结果: {msg}")
    print(f"当前可用资源: {banker.available}")

    # 显示请求后安全状态
    is_safe_after, seq_after = banker.is_safe()
    print(f"\n[请求后状态]")
    print(f"安全状态: {is_safe_after}")
    print(f"安全序列: {seq_after}\n")

    # 测试请求2: 不安全请求 (P0请求[0, 2, 0])
    process_id = 0
    request = [0, 2, 0]
    success, msg = banker.request_resources(process_id, request)
    print(f"[请求处理] 进程P{process_id} 请求资源: {request}")
    print(f"结果: {msg}")
