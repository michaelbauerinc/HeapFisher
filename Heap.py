import random

class MaxHeap:
    def __init__(self):
        self.heap_list = [None]
        self.count = 0

    def parent_idx(self, idx):
        return idx // 2

    def left_child_idx(self, idx):
        return idx * 2

    def right_child_idx(self, idx):
        return idx * 2 + 1

    def child_present(self, idx):
        return self.left_child_idx(idx) <= self.count

    def retrieve_max(self):
        if self.count == 0:
            # print("No items in heap")
            return None

        # print(self.heap_list)

        max = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.count]
        self.count -= 1
        self.heap_list.pop()
        self.heapify_down()
        return max


    def prepDelete(self, idx):
        tmp = self.heap_list[idx].x
        self.heap_list[idx].x = self.heap_list[self.count].x
        self.heap_list[self.count].x = tmp
        tmp = self.heap_list[idx].y
        self.heap_list[idx].y = self.heap_list[self.count].y
        self.heap_list[self.count].y = tmp
        tmp = self.heap_list[idx]
        self.heap_list[idx] = self.heap_list[self.count]
        self.heap_list[self.count] = tmp
        tmp = self.heap_list[idx].idx
        self.heap_list[idx].idx = self.heap_list[self.count].idx
        self.heap_list[self.count].idx = tmp

        varToBeReturned = self.heap_list.pop(self.count)

        self.count -= 1
        self.heapify_down()


        return varToBeReturned



    def add(self, element):
        self.count += 1
        self.heap_list.append(element)
        self.heapify_up()

    def get_smaller_child_idx(self, idx):
        if self.right_child_idx(idx) > self.count:
            return self.left_child_idx(idx)
        else:
            left_child = self.heap_list[self.left_child_idx(idx)]
            right_child = self.heap_list[self.right_child_idx(idx)]
            if left_child.value < right_child.value:
                return self.left_child_idx(idx)
            else:
                return self.right_child_idx(idx)

    def heapify_up(self):
        idx = self.count
        swap_count = 0
        while self.parent_idx(idx) > 0:
            if self.heap_list[self.parent_idx(idx)].value < self.heap_list[idx].value:
                swap_count += 1
                tmp = self.heap_list[self.parent_idx(idx)].x
                self.heap_list[self.parent_idx(idx)].x = self.heap_list[idx].x
                self.heap_list[idx].x = tmp
                tmp = self.heap_list[self.parent_idx(idx)].y
                self.heap_list[self.parent_idx(idx)].y = self.heap_list[idx].y
                self.heap_list[idx].y = tmp
                tmp = self.heap_list[self.parent_idx(idx)]
                self.heap_list[self.parent_idx(idx)] = self.heap_list[idx]
                self.heap_list[idx] = tmp
                tmp = self.heap_list[self.parent_idx(idx)].idx
                self.heap_list[self.parent_idx(idx)].idx = self.heap_list[idx].idx
                self.heap_list[idx].idx = tmp
            idx -= 1

        element_count = len(self.heap_list)
        # if element_count > 10000:
            # print("Heap of {0} elements restored with {1} swaps"
                #   .format(element_count, swap_count))
            # print("")

    def heapify_down(self):
        idx = 1
        swap_count = 1
        while self.child_present(idx):
            smaller_child_idx = self.get_smaller_child_idx(idx)
            if self.heap_list[self.parent_idx(idx)] != None and self.heap_list[idx].value > self.heap_list[smaller_child_idx].value:
                swap_count += 1
                tmp = self.heap_list[self.parent_idx(idx)].idx
                self.heap_list[self.parent_idx(idx)].idx = self.heap_list[idx].idx
                self.heap_list[idx].idx = tmp
                tmp = self.heap_list[self.parent_idx(idx)].x
                self.heap_list[self.parent_idx(idx)].x = self.heap_list[idx].x
                self.heap_list[idx].x = tmp
                tmp = self.heap_list[self.parent_idx(idx)].y
                self.heap_list[self.parent_idx(idx)].y = self.heap_list[idx].y
                self.heap_list[idx].y = tmp
                tmp = self.heap_list[self.parent_idx(idx)]
                self.heap_list[self.parent_idx(idx)] = self.heap_list[idx]
                self.heap_list[idx] = tmp
            idx = smaller_child_idx

        element_count = len(self.heap_list)


    def print_heap(self):
        lst = []
        for i in self.heap_list:
            if i != None:
                lst.append(i.value)
        # print(lst)
        lst = []
        for i in self.heap_list:
            if i != None:
                lst.append(i.idx)
        # print(lst)