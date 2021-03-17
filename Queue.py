class Node:
    def __init__(self, number, next_node=None):
        self.number = number
        self.value = number.value
        self.next_node = next_node

    def set_next_node(self, next_node):
        self.next_node = next_node

    def get_next_node(self):
        return self.next_node

    def get_value(self):
        return self.value


class Queue:
    def __init__(self, max_size=None):
        self.queue_list = []
        self.head = None
        self.tail = None
        self.max_size = max_size
        self.size = 0

    def enqueue(self, value):
        if self.has_space():
            item_to_add = Node(value)
            if self.is_empty():
                self.head = item_to_add
                self.tail = item_to_add
            else:
                self.tail.set_next_node(item_to_add)
                self.tail = item_to_add
            self.size += 1
            self.queue_list.append(value)
            # print(self.head.number.value)
            # print(self.tail.number.value)
        # else:
            # print("No room!")

    def dequeue(self):
        if self.get_size() > 0:
            item_to_remove = self.head
            if self.get_size() == 1:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.get_next_node()
            self.size -= 1
            return item_to_remove
        # else:
            # print("Queue is empty!")

    def peek(self):
        if self.size > 0:
            return self.head

    def get_size(self):
        return self.size

    def has_space(self):
        if self.max_size == None:
            return True
        else:
            return self.max_size > self.get_size()

    def is_empty(self):
        return self.size == 0


    def drawNumbers(self):
        printNum = self.size
        counter = 4
        current = self.head
        for i in range(printNum):
            if current != None:
                val = current.number.value
                space = (", ")
                current.number.value = current.number.value
                current.number.text_to_screen()
                if counter > 1:
                    current.number.value = ("    , ")
                    current.number.text_to_screen()
                current.number.value = val
                current = current.next_node
                counter -= 1

    def print(self):
        printNum = self.size
        current = self.head
        lst = []
        for i in range(printNum):
            lst.append(current.value)
            current = current.next_node
        # print(lst)