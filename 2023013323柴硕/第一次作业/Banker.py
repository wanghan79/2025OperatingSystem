import ProcSecurity

class BankersAlgorithm:
    def __init__(self, total_resources, processes):
        """
        初始化银行家算法系统
        :param total_resources: 总资源向量，如[10,5,7] 
        :param processes: 进程列表，格式为[{
            'pid': 0, 
            'max': [7,5,3], 
            'alloc': [0,1,0]
        }]
        """
        self.total = total_resources
        self.processes = processes
        self.n_res = len(total_resources)
        
        self.max = [p['max'] for p in processes]
        self.alloc = [p['alloc'] for p in processes]
        self.need = [
            [self.max[i][j] - self.alloc[i][j] 
             for j in range(self.n_res)]
            for i in range(len(processes))
        ]
        self._update_available()

    def request_resources(self, pid, request):
        """
        处理资源请求
        :return: (是否批准, 安全序列)
        """

        if not self._validate_request(pid, request):
            return False, []

        temp_alloc = [row.copy() for row in self.alloc]
        temp_need = [row.copy() for row in self.need]
        temp_available = self.available.copy()

        for i in range(self.n_res):
            temp_alloc[pid][i] += request[i]
            temp_need[pid][i] -= request[i]
            temp_available[i] -= request[i]

        checker = ProcSecurity.SafetyChecker(temp_available, temp_alloc, temp_need)
        is_safe, seq = checker.check()

        if is_safe:
            self.alloc = temp_alloc
            self.need = temp_need
            self._update_available()
            return True, seq
        else:
            return False, []

    def _validate_request(self, pid, request):
        if pid < 0 or pid >= len(self.processes):
            raise ValueError("无效进程ID")
        
        if any(request[i] > self.need[pid][i] for i in range(self.n_res)):
            print(f"错误:请求超过进程P{pid}最大需求")
            return False
        
        if any(request[i] > self.available[i] for i in range(self.n_res)):
            print(f"资源不足,进程P{pid}需等待")
            return False
        
        return True

    def _update_available(self):
        self.available = [
            self.total[i] - sum(p[i] for p in self.alloc)
            for i in range(self.n_res)
        ]
        self.print_status()

    def print_status(self):
        print("系统资源状态:")
        print(f"总资源: {self.total}")
        print(f"可用资源: {self.available}")
        print("进程 | 最大需求 | 已分配 | 剩余需求")
        for pid in range(len(self.processes)):
            print(f"P{pid}  | {self.max[pid]} | {self.alloc[pid]} | {self.need[pid]}")