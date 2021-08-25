
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
        self.end = None

    def insertBeginning(self, node):
        if not self.head: #pointer at the end to signify last pc
            node.count = 1
            self.head = node
            self.end = node
            return

        node.count = self.head.count + 1
        node.next = self.head
        self.head = node

    #def __repr__(self):
       #pass

    def __str__(self):
        current = self.head
        while current is not None:
            print(f"{current.count} : {current.PC}")
            current=current.next
        return ""


#LLtest = LinkedList()
#LLtest.insertBeginning(Node("344754"))
#LLtest.insertBeginning(Node("15124124"))
#print(LLtest)
