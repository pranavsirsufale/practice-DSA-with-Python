class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

class DoublyLL:

    def __init__(self, head=None):
        self.head = head
    
    def insertAtStart(self, value):
        newNode = Node(value)
        if (self.head == None):
            self.head = newNode
            return
        newNode.next = self.head
        self.head.prev = newNode
        self.head = newNode

    def insertAtMid(self, value, targetVal):
        newNode = Node(value)
        if (self.head == None):
            self.head = newNode
            return
        headObj = self.head
        while (headObj.data != targetVal):
            headObj = headObj.next
        headObj = headObj.prev
        newNode.next = headObj.next
        headObj.next.prev = newNode
        headObj.next = newNode
        newNode.prev = headObj

    def insertAtEnd(self, value):
        newNode = Node(value)

        if (self.head == None):
            self.head = newNode
            return
        
        if (self.head != None):
            t1 = self.head
            while(t1.next != None):
                t1 = t1.next
            t1.next = newNode
            newNode.prev = t1

    def printLL(self):
        t1 = self.head
        print("[", end="")
        while (t1 != None):
            print(t1.data, end="] <-> [")
            t1 = t1.next
        print("None", end="] \n")

obj = DoublyLL()

for i in range(5):
    obj.insertAtEnd(i + 1)

for i in range(5, 10):
    obj.insertAtStart(i + 1)

obj.insertAtMid(10, 4)

obj.printLL()
print(obj.head.data)
print(obj.head.next.data)
# print(obj.prev.data)
