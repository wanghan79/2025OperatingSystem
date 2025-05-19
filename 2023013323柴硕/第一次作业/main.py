# main.py
from Banker import BankersAlgorithm

def initialize_system():
    processes = [
        {'pid':0, 'max':[7,5,3], 'alloc':[0,1,0]},
        {'pid':1, 'max':[3,2,2], 'alloc':[2,0,0]},
        {'pid':2, 'max':[9,0,2], 'alloc':[3,0,2]},
        {'pid':3, 'max':[2,2,2], 'alloc':[2,1,1]},
        {'pid':4, 'max':[4,3,3], 'alloc':[0,0,2]}
    ]
    total_resources = [10, 5, 7]
    return BankersAlgorithm(total_resources, processes)

def run_test_case(banker):
    print("\n" + "="*40)
    banker.print_status()
    
    print("\n>>> 测试P1请求资源[1,0,2]")
    granted, seq = banker.request_resources(1, [1,0,2])
    print(f"批准状态: {granted}, 安全序列: {seq}")

    
    print("\n>>> 测试P4请求资源[3,3,0]")
    granted, seq = banker.request_resources(4, [3,3,0])
    print(f"批准状态: {granted}, 安全序列: {seq}")
    

def interactive_mode(banker):
    while True:
        try:
            print("\n" + "="*40)
            req = input("输入请求(格式: 进程ID,R1,R2,R3 / q退出): ")
            if req.lower() == 'q': break
            
            pid, *resources = map(int, req.split(','))
            result, seq = banker.request_resources(pid, resources)
            
            print(f"审批结果: {'通过' if result else '拒绝'}")
            banker.print_status()
            if result: print(f"安全序列: {' → '.join(seq)}")
            
        except Exception as e:
            print(f"输入错误: {str(e)}")

if __name__ == "__main__":
    system = initialize_system()
    run_test_case(system)
    interactive_mode(system)