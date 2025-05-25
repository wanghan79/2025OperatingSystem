class BankersAlgorithm:
    def __init__(self):
        self.n_processes = 0  # 进程数量
        self.n_resources = 0  # 资源种类数
        self.max_claim = []  # 最大需求矩阵
        self.allocation = []  # 已分配矩阵
        self.need = []  # 需求矩阵
        self.available = []  # 可用资源向量

    def initialize(self):
        """初始化系统状态"""
        self.n_processes = int(input("请输入进程数: "))
        self.n_resources = int(input("请输入资源种类数: "))

        # 输入最大需求矩阵
        print("\n输入各进程的最大需求矩阵(max_claim):")
        for i in range(self.n_processes):
            self.max_claim.append(list(map(int, input(f"进程P{i}: ").split())))

        # 输入已分配矩阵
        print("\n输入已分配矩阵(allocation):")
        for i in range(self.n_processes):
            self.allocation.append(list(map(int, input(f"进程P{i}: ").split())))

        # 计算需求矩阵
        self.need = [
            [self.max_claim[i][j] - self.allocation[i][j]
             for j in range(self.n_resources)]
            for i in range(self.n_processes)
        ]

        # 输入可用资源向量
        self.available = list(map(int, input("\n输入可用资源向量(available): ").split()))

    def is_safe(self):
        """安全性检查算法"""
        work = self.available.copy()
        finish = [False] * self.n_processes
        safe_sequence = []
        count = 0

        while count < self.n_processes:
            found = False
            for i in range(self.n_processes):
                if not finish[i] and all(need <= work[j] for j, need in enumerate(self.need[i])):
                    # 找到可执行的进程
                    print(f"  → 发现可执行进程P{i}: need={self.need[i]} <= work={work}")
                    work = [work[j] + self.allocation[i][j] for j in range(self.n_resources)]
                    finish[i] = True
                    safe_sequence.append(f"P{i}")
                    count += 1
                    found = True
                    break

            if not found:  # 没有找到安全序列
                return False, []

        return True, safe_sequence

    def request_resources(self, process_id, request):
        """处理资源请求"""
        print(f"\n处理进程P{process_id}的请求: {request}")

        # 步骤1: 检查请求是否超过需求
        if any(request[j] > self.need[process_id][j] for j in range(self.n_resources)):
            print("错误：请求超过进程最大需求")
            return False

        # 步骤2: 检查请求是否超过可用资源
        if any(request[j] > self.available[j] for j in range(self.n_resources)):
            print("错误：请求超过当前可用资源")
            return False

        # 尝试分配资源
        print("执行试分配...")
        old_available = self.available.copy()
        old_allocation = [row.copy() for row in self.allocation]
        old_need = [row.copy() for row in self.need]

        # 修改状态
        self.available = [self.available[j] - request[j] for j in range(self.n_resources)]
        self.allocation[process_id] = [self.allocation[process_id][j] + request[j] for j in range(self.n_resources)]
        self.need[process_id] = [self.need[process_id][j] - request[j] for j in range(self.n_resources)]

        # 检查安全性
        is_safe, sequence = self.is_safe()
        if is_safe:
            print("√ 请求安全，分配成功")
            print(f"安全序列: {' → '.join(sequence)}")
            return True
        else:
            print("× 请求不安全，恢复原状态")
            self.available = old_available
            self.allocation = old_allocation
            self.need = old_need
            return False

    def print_state(self):
        """打印当前系统状态"""
        print("\n当前系统状态:")
        print("进程\t最大需求\t已分配\t需求")
        for i in range(self.n_processes):
            print(f"P{i}\t{self.max_claim[i]}\t{self.allocation[i]}\t{self.need[i]}")
        print(f"可用资源: {self.available}\n")


# 测试案例
def test_case():
    banker = BankersAlgorithm()

    # 设置测试数据
    banker.n_processes = 5
    banker.n_resources = 3
    banker.max_claim = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    banker.allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    banker.available = [3, 3, 2]

    # 计算需求矩阵
    banker.need = [
        [banker.max_claim[i][j] - banker.allocation[i][j]
         for j in range(banker.n_resources)]
        for i in range(banker.n_processes)
    ]

    # 显示初始状态
    banker.print_state()

    # 执行安全性检查
    print("执行安全性检查...")
    is_safe, seq = banker.is_safe()
    if is_safe:
        print("√ 系统处于安全状态")
        print(f"安全序列: {' → '.join(seq)}\n")
    else:
        print("× 系统处于不安全状态\n")

    # 测试请求：P1请求[1, 0, 2]
    banker.request_resources(1, [1, 0, 2])


if __name__ == "__main__":
    # 选择运行模式
    choice = input("运行测试案例吗？(y/n): ")
    if choice.lower() == 'y':
        test_case()
    else:
        banker = BankersAlgorithm()
        banker.initialize()
        banker.print_state()

        # 执行安全性检查
        is_safe, seq = banker.is_safe()
        if is_safe:
            print("√ 系统处于安全状态")
            print(f"安全序列: {' → '.join(seq)}\n")
        else:
            print("× 系统处于不安全状态\n")

        # 处理请求
        while True:
            choice = input("是否处理请求？(y/n): ")
            if choice.lower() != 'y':
                break
            try:
                pid = int(input("输入进程ID: "))
                req = list(map(int, input("输入请求资源(用空格分隔): ").split()))
                if pid < 0 or pid >= banker.n_processes:
                    raise ValueError
                banker.request_resources(pid, req)
                banker.print_state()
            except:
                print("输入错误，请重新输入！")

