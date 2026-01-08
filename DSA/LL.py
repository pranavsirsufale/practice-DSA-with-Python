class Node:
    def __init__(self, info, next=None):
        self.info, self.next = info, next

class SingleLinkedList:
    def __init__(self, head=None):
        self.head = head
    
    def insertAtBeg(self, value):
        temp = Node(value)
        temp.next = self.head
        self.head = temp

    def insertAtEnd(self, value):
        temp = Node(value)
        if (self.head != None):
            t1 = self.head
            while (t1.next != None):
                t1 = t1.next
            t1.next = temp
        else:
            self.head = temp
    
    def deleteLL(self, value):
        prev = self.head
        while(prev != None and prev.info != value):
            if (prev.next.info == value):
                break
            prev = prev.next
        if (prev != None):
            prev.next = prev.next.next

    def insertAtMid(self, value, posVal):
        temp = Node(value)
        t1 = self.head
        while (t1 != None and t1.info != posVal):
            t1 = t1.next
            next = t1.next
            if (next.info == posVal):
                break
        if (t1 != None):
            temp.next = t1.next
            t1.next = temp
        else:
            print("Position value not found")

    def printLL(self):
        t1 = self.head
        print("[", end="")
        while (t1.next != None):
            print(t1.info, end="] -> [")
            t1 = t1.next
        print(t1.info, end="] \n")

obj = SingleLinkedList()
for i in range(5):
    obj.insertAtEnd(i+1)

for i in range(5, 10):
    obj.insertAtBeg(i+1)

obj.insertAtMid(100, 2)
obj.deleteLL(3)
obj.deleteLL(4)

obj.printLL()

