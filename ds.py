
## example Linked List:
## Last -> 3rd -> 2nd -> 1st
## Ending signified if 1st is the same as the NEW last

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

        node.count = self.head.count + 1
        node.next = self.head
        self.head = node
