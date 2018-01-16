import heapq

class PriorityQueue:
    def __init__(self, priorityFunction):
        self.heap = []
        self.count = 0
        self.priorityFunction = priorityFunction

    def push(self, item):
        priority = self.priorityFunction(item)
        heapq.heappush(self.heap, (priority, self.count, item))
        self.count += 1

    def pop(self):
        (priority, count, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

def get_class(module, object_name):
    if object_name not in dir(module):
        raise AttributeError("{} is not found in {}".format(object_name, module))
    return getattr(module, object_name)

def heaptest():
    def distanceFrom5(item):
        return abs(item-5)

    pqueue = PriorityQueue(distanceFrom5)
    lst = range(1, 10, 1)
    for num in lst:
        pqueue.push(num)

    while not pqueue.isEmpty():
        print(pqueue.pop())
