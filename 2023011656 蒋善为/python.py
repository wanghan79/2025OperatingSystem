class BankerAlgorithm:
    def __init__(self, available, max, allocation, need):
        self
.available = available[:]
        self
.max = [row[:] for row in max]
        self
.allocation = [row[:] for row in allocation]
        self
.need = [row[:] for row in need]

    def is_safe(self):
        work 
= self.available[:]
        finish 
= [False] * len(self.allocation)
        safe_sequence 
= []

        while True:
            for i in range(len(self.allocation)):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(work))):
                    for j in range(len(work)):
                        work
[j] += self.allocation[i][j]
                    finish
[i] = True
                    safe_sequence
.append(i)
                    break
            else:
                break

        return all(finish), safe_sequence if all(finish) else None

    def request_resources(self, process_number, request):
        if any(request[i] > self.need[process_number][i] for i in range(len(request))):
            return False

        if all(request[i] <= self.available[i] for i in range(len(request))):
            for i in range(len(request)):
                self
.available[i] -= request[i]
                self
.allocation[process_number][i] += request[i]
                self
.need[process_number][i] -= request[i]

            is_safe
, safe_sequence = self.is_safe()
            if is_safe:
                return True
            else:
                for i in range(len(request)):
                    self
.available[i] += request[i]
                    self
.allocation[process_number][i] -= request[i]
                    self
.need[process_number][i] += request[i]
                return False
        else:
            return False
