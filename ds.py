
## example Linked List:
## Last -> 3rd -> 2nd -> 1st
## Ending signified if 1st is the same as the NEW last
##

class Node:
    def __init__(self, PCNumber):
        self.PC = PCNumber
        self.count = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.current = None

    def insertBeginning(self, node):
        if not self.head:
            node.count = 1
            self.head = node
            return

        node.count = self.head.count + 1
        node.next = self.head
        self.head = node
        self.current = self.head

    def pop(self):
        temp = self.head
        self.head = self.head.next
        return temp

    #def __repr__(self):
       #pass

    def __str__(self):
        current = self.head
        while current is not None:
            print(f"#{current.count} : {current.PC}")
            current=current.next
        return ""


#LLtest = LinkedList()
#LLtest.insertBeginning(Node("344754"))
#LLtest.insertBeginning(Node("15124124"))
#print(LLtest)
