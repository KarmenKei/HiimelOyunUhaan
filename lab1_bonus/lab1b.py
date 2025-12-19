from collections import deque

# Dasgal 1: Stack

class Stack:
    def __init__(self):
        self._list = []

    def push(self, element):
        self._list.append(element)

    def pop(self):
        return self._list.pop()

    def top(self):
        return self._list[-1]

    def __len__(self):
        return len(self._list)

    def is_empty(self):
        return len(self) == 0

    def __str__(self):
        return "Stack: " + str(self._list)


print("--- Dasgal 1: Stack")
stack = Stack()
stack.push('T1')
stack.push('T2')
stack.push('T3')

print('stack:', stack)
print('stack.is_empty():', stack.is_empty())
print('stack.length():', len(stack))
print('stack.top():', stack.top())
print('stack.pop():', stack.pop())
print('stack:', stack)


# Dasgal 2: deque Queue

print("--- Dasgal 2: deque Queue")
data = [5, 1, 3, 8, 2]
data.sort()

queue = deque(data)
print(queue)


# Dasgal 3: List Index Filtering

print("---Dasgal 3: List Index Filtering")

listOne = [3, 6, 9, 12, 15, 18, 21]
listTwo = [4, 8, 12, 16, 20, 24, 28]

listThree = []

for i in range(len(listOne)):
    if i % 2 == 1:
        listThree.append(listOne[i])

for i in range(len(listTwo)):
    if i % 2 == 0:
        listThree.append(listTwo[i])

print(listThree)
