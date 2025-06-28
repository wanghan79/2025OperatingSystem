def resource_request_handler(max_claim, remaining, available, allocated, req):
    """
    Banker's Algorithm implementation for resource request handling.
    Returns allocation status and updated system state.
    """
    process_id, resource_req = req
    process_count = len(max_claim)
    resource_types = len(available)
    
    # Preserve original state for rollback
    orig_remaining = [r[:] for r in remaining]
    orig_available = available[:]
    orig_allocated = [a[:] for a in allocated]
    
    # Validate request
    for j in range(resource_types):
        if resource_req[j] > remaining[process_id][j]:
            return "分配失败：请求超过需求", max_claim, orig_remaining, orig_available, orig_allocated
        if resource_req[j] > available[j]:
            return "分配失败：请求超过可用资源", max_claim, orig_remaining, orig_available, orig_allocated
    
    # Tentative allocation
    new_available = [available[j] - resource_req[j] for j in range(resource_types)]
    new_allocated = [a[:] for a in allocated]
    new_remaining = [r[:] for r in remaining]
    
    for j in range(resource_types):
        new_allocated[process_id][j] += resource_req[j]
        new_remaining[process_id][j] -= resource_req[j]
    
    # Security verification
    work_vector = new_available[:]
    completed = [False] * process_count
    execution_order = []
    progress_made = True
    
    while progress_made and not all(completed):
        progress_made = False
        for i in range(process_count):
            if not completed[i] and all(new_remaining[i][j] <= work_vector[j] for j in range(resource_types)):
                for j in range(resource_types):
                    work_vector[j] += new_allocated[i][j]
                completed[i] = True
                execution_order.append(i)
                progress_made = True
    
    # Check system security
    if all(completed):
        return (f"分配成功！安全序列: {execution_order}",
                max_claim, new_remaining, new_available, new_allocated)
    else:
        return "分配失败：系统将进入不安全状态", max_claim, orig_remaining, orig_available, orig_allocated


def display_system_state(max_table, alloc_table, need_table, avail_vector):
    """Formatted display of system resource allocation state"""
    print("\n系统资源分配状态：\n")
    
    # Prepare column headers
    headers = ["进程", "Max Allocation", "Current Allocation", "Remaining Need", "Available"]
    print(f"{headers[0]:<5} | {headers[1]:<15} | {headers[2]:<15} | {headers[3]:<15} | {headers[4]}")
    print("-"*70)
    
    # Display each process
    for i in range(len(max_table)):
        max_str = " ".join(str(x) for x in max_table[i])
        alloc_str = " ".join(str(x) for x in alloc_table[i])
        need_str = " ".join(str(x) for x in need_table[i])
        avail_str = " ".join(str(x) for x in avail_vector) if i == 0 else ""
        
        print(f"P{i:<4} | {max_str:<15} | {alloc_str:<15} | {need_str:<15} | {avail_str}")


if __name__ == "__main__":
    # System state configuration
    max_claim = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    current_alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    remaining_need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
    available_res = [3, 3, 2]
    
    # Process resource request
    resource_req = (1, [1, 0, 2])
    
    # Process request
    result, max_out, need_out, avail_out, alloc_out = resource_request_handler(
        max_claim, remaining_need, available_res, current_alloc, resource_req
    )
    
    # Display results
    print(result)
    display_system_state(max_out, alloc_out, need_out, avail_out)