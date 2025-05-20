"""
@Author: Zhang Gaosheng
@Version: 1.0
@Description: 使用 python 语言模拟实现银行家算法，要求封装成一个函数，能够接收 Max、Need、
              Available、Allocated 矩阵，以及资源申请 Request, 使用银行家算法计算后输出是
              否能够分配，以及分配后的四个矩阵。
"""

###################################################################################
##
##  Import
##
###################################################################################

from banker import banker_algorithm, print_matrix, safety_check

###################################################################################
##
##  Main
##
###################################################################################

def main():
    # 1. 打印初始系统状态
    print("="*100)
    print("初始系统状态：")
    print(f"\n可利用资源向量: {available}")
    print_matrix(**{'title' : "最大需求矩阵", 'matrix': max_matrix, 
                    'resource_names': resource_names, 'process_names': process_names})
    print_matrix(**{'title' : "分配矩阵", 'matrix': allocation_matrix, 
                    'resource_names': resource_names, 'process_names': process_names})
    print_matrix(**{'title' : "需求矩阵", 'matrix': need_matrix, 
                    'resource_names': resource_names, 'process_names': process_names})


    # 2. 执行安全检测
    is_safe, safe_seq = safety_check(**{'available': available, 
                                        'allocation': allocation_matrix, 'need': need_matrix})
    print("\n" + "="*100)
    if is_safe:
        print(f"安全检测结果：系统安全，安全序列为：{" → ".join([f'P{i}' for i in safe_seq])}")
    else:
        print("安全检测结果：系统不安全")
    print("\n" + "="*100)


    # 3. 银行家算法（P1 请求资源 [1, 0, 2]）
    copy_available = available.copy()
    to_banker_data = {'process_id': 1, 'request': [1, 0, 2], 'available': copy_available, 
                      'allocation': [row.copy() for row in allocation_matrix], 'need': [row.copy() for row in need_matrix]}
    result, msg, new_avail, new_alloc, new_need, safe_seq = banker_algorithm(**to_banker_data)

    # 4. 输出结果
    print(f"处理请求: 进程 P{to_banker_data['process_id']} 请求资源 {to_banker_data['request']}")
    print(f"结果：{msg}")
    if result:
        print(f"\n新的可利用资源向量: {new_avail}")
        print_matrix(**{'title' : "新的最大需求矩阵", 'matrix': max_matrix, 
                        'resource_names': resource_names, 'process_names': process_names})
        print_matrix(**{'title' : "新的分配矩阵", 'matrix': new_alloc, 
                        'resource_names': resource_names, 'process_names': process_names})
        print_matrix(**{'title' : "新的需求矩阵", 'matrix': new_need, 
                        'resource_names': resource_names, 'process_names': process_names})
        print(f"新的安全序列：{" → ".join([f'P{i}' for i in safe_seq])}")


if __name__ == "__main__":
    # 初始数据
    available = [3, 3, 2]
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    allocation_matrix = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    # need_matrix = max_matrix - allocation_matrix
    need_matrix = [
        [7-0, 5-1, 3-0],
        [3-2, 2-0, 2-0],
        [9-3, 0-0, 2-2],
        [2-2, 2-1, 2-1],
        [4-0, 3-0, 3-2]
    ]
    resource_names = ['A', 'B', 'C']
    process_names = [f'P{i}' for i in range(5)]

    # 运行
    main()