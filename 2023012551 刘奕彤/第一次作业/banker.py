import copy


class BankersAlgorithm:
    def __init__(self, available, max_demand, allocation, resource_names, process_names):
        """
        初始化银行家算法系统

        参数:
            available: 可用资源向量
            max_demand: 最大需求矩阵
            allocation: 已分配矩阵
            resource_names: 资源名称列表
            process_names: 进程名称列表
        """
        self.available = copy.deepcopy(available)
        self.max_demand = copy.deepcopy(max_demand)
        self.allocation = copy.deepcopy(allocation)
        self.resource_names = resource_names
        self.process_names = process_names
        self.need = self.calculate_need()

    def calculate_need(self):
        """计算需求矩阵(Need = Max - Allocation)"""
        return [
            [self.max_demand[i][j] - self.allocation[i][j]
             for j in range(len(self.available))]
            for i in range(len(self.allocation))
        ]

    def safety_check(self):
        """执行安全检测算法，检查系统是否处于安全状态"""
        work = self.available.copy()
        finish = [False] * len(self.allocation)
        safe_sequence = []

        while True:
            found = False
            for i in range(len(self.allocation)):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(work))):
                    # 模拟进程执行完成并释放资源
                    for j in range(len(work)):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

            if not found:
                break

        is_safe = all(finish)
        return is_safe, safe_sequence

    def request_resources(self, process_id, request):
        """处理进程的资源请求"""
        # 1. 检查请求是否超过需求
        if any(request[j] > self.need[process_id][j] for j in range(len(request))):
            return False, f"错误：进程{self.process_names[process_id]}的请求超过其需求"

        # 2. 检查请求是否超过可用资源
        if any(request[j] > self.available[j] for j in range(len(request))):
            return False, f"错误：进程{self.process_names[process_id]}的请求超过可用资源"

        # 3. 尝试分配资源
        old_available = copy.deepcopy(self.available)
        old_allocation = copy.deepcopy(self.allocation)
        old_need = copy.deepcopy(self.need)

        # 更新系统状态
        for j in range(len(request)):
            self.available[j] -= request[j]
            self.allocation[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]

        # 4. 检查安全性
        is_safe, safe_sequence = self.safety_check()
        if is_safe:
            return True, f"分配成功! 安全序列: {' → '.join([self.process_names[i] for i in safe_sequence])}"
        else:
            # 回滚操作
            self.available = old_available
            self.allocation = old_allocation
            self.need = old_need
            return False, "错误：分配会导致系统进入不安全状态"

    def print_state(self):
        """打印系统当前状态"""
        print("\n" + "=" * 60)
        print("银行家算法系统状态")
        print("=" * 60)

        # 打印可用资源
        print("\n可用资源:")
        print('   '.join(f"{res}: {self.available[i]}" for i, res in enumerate(self.resource_names)))

        # 打印表头
        print("\n" + "-" * 90)
        header = f"{'进程':<6}"
        for res in self.resource_names:
            header += f"{'Max_' + res:<6}"
        for res in self.resource_names:
            header += f"{'Alloc_' + res:<6}"
        for res in self.resource_names:
            header += f"{'Need_' + res:<6}"
        print(header)
        print("-" * 90)

        # 打印进程资源信息
        for i, name in enumerate(self.process_names):
            row = f"{name:<6}"
            # 最大需求
            for j in range(len(self.resource_names)):
                row += f"{self.max_demand[i][j]:<6}"
            # 已分配
            for j in range(len(self.resource_names)):
                row += f"{self.allocation[i][j]:<6}"
            # 需求
            for j in range(len(self.resource_names)):
                row += f"{self.need[i][j]:<6}"
            print(row)
        print("-" * 90)


def main():
    # =========================================
    # 新测试用例：使用不同的系统状态
    # =========================================
    resource_names = ['CPU', 'Memory', 'Disk']
    process_names = ['WebServer', 'Database', 'Cache', 'App', 'Backup']

    # 初始系统状态
    available = [5, 4, 3]  # 可用资源: [CPU, Memory, Disk]

    max_demand = [
        [3, 3, 2],  # WebServer
        [4, 2, 3],  # Database
        [2, 1, 2],  # Cache
        [3, 3, 2],  # App
        [2, 2, 2]  # Backup
    ]

    allocation = [
        [1, 1, 0],  # WebServer
        [2, 0, 1],  # Database
        [0, 0, 1],  # Cache
        [1, 1, 0],  # App
        [0, 0, 1]  # Backup
    ]

    # 创建银行家算法实例
    bank = BankersAlgorithm(available, max_demand, allocation, resource_names, process_names)

    # 打印初始状态
    bank.print_state()

    # =========================================
    # 执行安全检查
    # =========================================
    print("\n执行安全检查...")
    is_safe, safe_sequence = bank.safety_check()
    if is_safe:
        safe_seq_names = ' → '.join([bank.process_names[i] for i in safe_sequence])
        print(f"✓ 系统安全! 安全序列: {safe_seq_names}")
    else:
        print("✗ 系统不安全!")

    # =========================================
    # 模拟资源请求（新测试用例）
    # =========================================

    # 请求1: Database请求资源 [1, 0, 1]
    print("\n请求1: Database请求资源 [1, 0, 1]")
    success, message = bank.request_resources(1, [1, 0, 1])
    print(message)
    if success:
        bank.print_state()

    # 请求2: App请求资源 [0, 2, 0]
    print("\n请求2: App请求资源 [0, 2, 0]")
    success, message = bank.request_resources(3, [0, 2, 0])
    print(message)
    if success:
        bank.print_state()

    # 请求3: Backup请求资源 [2, 2, 1] (超过可用资源)
    print("\n请求3: Backup请求资源 [2, 2, 1]")
    success, message = bank.request_resources(4, [2, 2, 1])
    print(message)

    # 请求4: WebServer请求资源 [1, 0, 1] (可能导致不安全状态)
    print("\n请求4: WebServer请求资源 [1, 0, 1]")
    success, message = bank.request_resources(0, [1, 0, 1])
    print(message)
    if success:
        bank.print_state()


if __name__ == "__main__":
    main()