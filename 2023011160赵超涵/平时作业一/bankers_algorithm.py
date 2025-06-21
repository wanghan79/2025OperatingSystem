import copy
from typing import List, Tuple, Union, NamedTuple


class BankerMatrices(NamedTuple):
    Max: List[List[int]]
    Need: List[List[int]]
    Available: List[int]
    Allocated: List[List[int]]
    Request: Tuple[int, List[int]]


def safety_algorithm(args) -> Tuple[bool, Union[List[int], None]]:

    work = copy.deepcopy(args.Available)
    finish = [False] * len(args.Allocated)
    safe_sequence = []

    need_copy = copy.deepcopy(args.Need)
    allocated_copy = copy.deepcopy(args.Allocated)

    count = 0
    while count < len(args.Allocated):
        found = False
        for i in range(len(args.Allocated)):
            if not finish[i]:
                if all(need_copy[i][j] <= work[j] for j in range(len(work))):
                    for j in range(len(work)):
                        work[j] += allocated_copy[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    count += 1
                    found = True
        if not found:
            break

    return all(finish), safe_sequence if all(finish) else None


def bankers_algorithm(args) -> Tuple[bool, Union[List[int], None], BankerMatrices, str]:
    process_id, request = args.Request
    original_matrices = copy.deepcopy(args)
    if any(request[j] > args.Need[process_id][j] for j in range(len(request))):
        return False, None, original_matrices, "错误：请求超过进程需求"
    if any(request[j] > args.Available[j] for j in range(len(request))):
        return False, None, original_matrices, "错误：请求超过系统可用资源"
    new_available = copy.deepcopy(args.Available)
    new_allocated = copy.deepcopy(args.Allocated)
    new_need = copy.deepcopy(args.Need)

    for j in range(len(request)):
        new_available[j] -= request[j]
        new_allocated[process_id][j] += request[j]
        new_need[process_id][j] -= request[j]

    new_matrices = BankerMatrices(
        Max=args.Max,
        Need=new_need,
        Available=new_available,
        Allocated=new_allocated,
        Request=args.Request
    )

    is_safe, safe_sequence = safety_algorithm(new_matrices)

    if is_safe:
        return True, safe_sequence, new_matrices, "分配成功，系统处于安全状态"
    else:
        return False, None, original_matrices, "分配失败：会导致系统进入不安全状态"


if __name__ == "__main__":
    matrices = BankerMatrices(
        Max=[
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ],
        Need=[
            [7, 4, 3],
            [1, 2, 2],
            [6, 0, 0],
            [0, 1, 1],
            [4, 3, 1]
        ],
        Available=[3, 3, 2],
        Allocated=[
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ],
        Request=(1, [1, 0, 2])
    )


    success, sequence, new_matrices, message = bankers_algorithm(matrices)

    print("=== 银行家算法结果 ===")
    print(f"分配结果: {message}")
    print(f"安全序列: {sequence if success else '无'}")

