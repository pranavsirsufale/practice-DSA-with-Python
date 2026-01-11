class Stack:
    def __init__(self):
        self.stack = [] # stack in list format

    def length(self):
        return len(self.stack)
    
    def peek(self):
        lastEl = (len(self.stack) - 1)
        print(self.stack[lastEl])
    
    def pop(self):
        return self.stack.pop()

    def push(self, value):
        return self.stack.append(value)
    
    def isEmpty(self) -> bool:
        if (len(self.stack) == 0):
            return True
        return False
    
    def printStack(self):
        for stackVal in reversed(self.stack):
            print(f"[ {stackVal} ]", end="\n \n")

obj = Stack()

print(obj.isEmpty())

for i in range(5):
    obj.push(i+1)

obj.printStack()
print(obj.isEmpty())

obj.pop()

obj.printStack()

obj.peek()
