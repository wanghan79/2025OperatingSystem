import random
import xml.etree.ElementTree as ET
from functools import wraps
from typing import List, Dict, Any, Tuple, Generator
import statistics
import io

def bankers_algorithm(max_matrix: List[List[int]],
                      need_matrix: List[List[int]],
                      available: List[int],
                      allocated_matrix: List[List[int]],
                      request: Tuple[int, List[int]]) -> Dict:
    """
    银行家算法实现

    参数:
        max_matrix: 最大需求矩阵
        need_matrix: 需求矩阵
        available: 可用资源向量
        allocated_matrix: 已分配矩阵
        request: 资源申请 (进程号, 申请资源列表)

    返回:
        字典包含: {
            'can_allocate': bool,
            'safe_sequence': list,
            'new_matrices': dict
        }
    """

    def is_safe(avail, alloc, need):
        """安全性算法"""
        n_processes = len(alloc)
        n_resources = len(avail)

        # 工作向量和完成标志
        work = avail[:]
        finish = [False] * n_processes
        safe_seq = []

        while len(safe_seq) < n_processes:
            found = False
            for i in range(n_processes):
                if not finish[i]:
                    # 检查是否可以满足进程i的需求
                    if all(need[i][j] <= work[j] for j in range(n_resources)):
                        # 模拟完成进程i，释放资源
                        for j in range(n_resources):
                            work[j] += alloc[i][j]
                        finish[i] = True
                        safe_seq.append(i)
                        found = True
                        break

            if not found:
                return False, []

        return True, safe_seq

    # 复制矩阵以避免修改原始数据
    max_copy = [row[:] for row in max_matrix]
    need_copy = [row[:] for row in need_matrix]
    available_copy = available[:]
    allocated_copy = [row[:] for row in allocated_matrix]

    process_id, request_vector = request

    # 检查申请是否合法
    # 1. 申请不能超过需求
    for i in range(len(request_vector)):
        if request_vector[i] > need_copy[process_id][i]:
            return {
                'can_allocate': False,
                'reason': f'申请资源{i}超过需求',
                'safe_sequence': [],
                'new_matrices': {}
            }

    # 2. 申请不能超过可用资源
    for i in range(len(request_vector)):
        if request_vector[i] > available_copy[i]:
            return {
                'can_allocate': False,
                'reason': f'申请资源{i}超过可用数量',
                'safe_sequence': [],
                'new_matrices': {}
            }

    # 试探性分配
    for i in range(len(request_vector)):
        available_copy[i] -= request_vector[i]
        allocated_copy[process_id][i] += request_vector[i]
        need_copy[process_id][i] -= request_vector[i]

    # 检查是否处于安全状态
    safe, safe_sequence = is_safe(available_copy, allocated_copy, need_copy)

    if safe:
        return {
            'can_allocate': True,
            'safe_sequence': safe_sequence,
            'new_matrices': {
                'Max': max_copy,
                'Need': need_copy,
                'Available': available_copy,
                'Allocated': allocated_copy
            }
        }
    else:
        return {
            'can_allocate': False,
            'reason': '分配后系统将处于不安全状态',
            'safe_sequence': [],
            'new_matrices': {}
        }


def print_banker_result(result: Dict):
    """打印银行家算法结果"""
    print(f"是否可以分配: {'是' if result['can_allocate'] else '否'}")

    if not result['can_allocate']:
        print(f"原因: {result.get('reason', '未知')}")
    else:
        print(f"安全序列: {result['safe_sequence']}")
        print("\n分配后的矩阵:")
        matrices = result['new_matrices']

        print("Max矩阵:")
        for i, row in enumerate(matrices['Max']):
            print(f"P{i}: {row}")

        print("\nNeed矩阵:")
        for i, row in enumerate(matrices['Need']):
            print(f"P{i}: {row}")

        print(f"\nAvailable: {matrices['Available']}")

        print("\nAllocated矩阵:")
        for i, row in enumerate(matrices['Allocated']):
            print(f"P{i}: {row}")
def test_all_assignments():
    """测试作业"""

    print("=" * 60)
    print("作业一：银行家算法测试")
    print("=" * 60)

    # 银行家算法测试数据
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    allocated_matrix = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    # 计算Need矩阵
    need_matrix = [[max_matrix[i][j] - allocated_matrix[i][j]
                    for j in range(len(max_matrix[i]))]
                   for i in range(len(max_matrix))]

    available = [3, 3, 2]

    # 测试资源申请
    request = (1, [1, 0, 2])  # 进程P1申请资源[1,0,2]

    result = bankers_algorithm(max_matrix, need_matrix, available, allocated_matrix, request)
    print_banker_result(result)
    print("\n" + "=" * 60)
test_all_assignments()
