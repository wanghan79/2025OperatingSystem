import numpy as np


class ResourceAllocationManager:
    def __init__(self, max_res, allocated_res, available_res):
        self.max_res = max_res
        self.allocated_res = allocated_res
        self.available_res = available_res
        self.num_processes = max_res.shape[0]
        self.num_resources = max_res.shape[1]

    def calculate_need_matrix(self):
        return self.max_res - self.allocated_res

    def is_request_valid(self, request, process_id):
        # 检查请求是否小于等于需求
        if np.any(request > self.calculate_need_matrix()[process_id]):
            print(f"进程 {process_id} 的请求超过了其声明的最大需求")
            return False

        # 检查请求是否小于等于可用资源
        if np.any(request > self.available_res):
            print(f"系统当前可用资源不足，无法满足进程 {process_id} 的请求")
            return False

        return True

    def allocate_resources(self, request, process_id):
        if not self.is_request_valid(request, process_id):
            return False, None, None, None, None

        # 尝试分配资源
        temp_available = self.available_res - request
        temp_allocated = self.allocated_res.copy()
        temp_allocated[process_id] += request
        temp_need = self.calculate_need_matrix()
        temp_need[process_id] -= request

        # 测试安全性
        finish = np.zeros(self.num_processes, dtype=bool)
        work_vector = temp_available.copy()
        safe_sequence = []

        # 寻找安全序列
        while True:
            process_found = False
            for i in range(self.num_processes):
                if not finish[i] and np.all(temp_need[i] <= work_vector):
                    work_vector += temp_allocated[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    process_found = True
                    break

            if not process_found:
                break

        # 判断资源分配是否安全
        if all(finish):
            print(f"资源分配成功，安全序列为: {safe_sequence}")
            return True, self.max_res, temp_need, temp_available, temp_allocated
        else:
            print("资源分配会导致系统处于不安全状态，分配失败")
            return False, None, None, None, None


if __name__ == "__main__":
    # 定义资源请求参数
    num_processes = 5
    num_resources = 3

    # 初始化资源矩阵
    max_matrix = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])

    allocated_matrix = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])

    available_vector = np.array([3, 3, 2])

    # 创建资源分配管理器实例
    ram = ResourceAllocationManager(max_matrix, allocated_matrix, available_vector)

    # 进程请求资源
    process_request = np.array([1, 0, 2])
    target_process = 1

    # 尝试分配资源
    allocation_success, updated_max, updated_need, updated_available, updated_allocation = ram.allocate_resources(
        process_request, target_process)

    if allocation_success:
        print("\n资源分配后当前系统状态:")
        print("最大需求矩阵:\n", updated_max)
        print("需求矩阵:\n", updated_need)
        print("可用资源向量:\n", updated_available)
        print("资源分配矩阵:\n", updated_allocation)
    else:
        print("资源分配失败。")