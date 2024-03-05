import math
import time
import tkinter as tk
import random
from tkinter import *


class Queue:
    def __init__(self):
        self.queue_set = set()

    def enqueue(self, item):
        self.queue_set.add(item)

    def dequeue(self):
        if not self.is_empty():
            item = next(iter(self.queue_set))
            self.queue_set.remove(item)
            return item
        else:
            raise IndexError("dequeue from empty queue")

    def top(self):
        if not self.is_empty():
            return next(iter(self.queue_set))
        else:
            raise IndexError("top of empty queue")

    def is_empty(self):
        return len(self.queue_set) == 0

    def contain(self, value):
        return value in self.queue_set


nodes_expanded = 0
parents = []

class Stack:
    def __init__(self):
        self.set = set()  # Initialize the set

    def push(self, item):
        self.set.add(item)  # Add item to the set

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        item = self.top()  # Get the top item
        self.set.remove(item)  # Remove the top item from the set
        return item

    def top(self):
        if self.is_empty():
            raise IndexError("top from an empty stack")
        # Since sets are unordered, returning an arbitrary element
        return next(iter(self.set))

    def is_empty(self):
        return len(self.set) == 0

    def contain(self, value):
        return value in self.set

def check_goal(grid_state):
    if(grid_state =="012345678"):
        return True
    else:
        return False

def swap2(i,j,grid):
    temp= list(grid)
    copied=temp[:]
    temp2=copied[i]
    copied[i]=copied[j]
    copied[j]=temp2
    return copied

def swap(i, j ,grid_state):
    grid_state[i], grid_state[j] = grid_state[j], grid_state[i]
    return grid_state

def get_possible_moves(grid_state):
    grid_temp=list(grid_state)
    possible=[]
    if(grid_state.index("0")==0):
        possible.append(''.join(swap2(0,1,grid_temp)))
        possible.append(''.join(swap2(0,3, grid_temp)))
    elif(grid_state.index("0")==1):
        possible.append(''.join(swap2(1, 0, grid_temp)))
        possible.append(''.join(swap2(1, 2, grid_temp)))
        possible.append(''.join(swap2(1, 4, grid_temp)))
    elif (grid_state.index("0") == 2):
        possible.append(''.join(swap2(2, 1, grid_temp)))
        possible.append(''.join(swap2(2, 5, grid_temp)))
    elif (grid_state.index("0") == 3):
        possible.append(''.join(swap2(3, 0, grid_temp)))
        possible.append(''.join(swap2(3, 4, grid_temp)))
        possible.append(''.join(swap2(3, 6, grid_temp)))
    elif (grid_state.index("0") == 4):
        possible.append(''.join(swap2(4, 1, grid_temp)))
        possible.append(''.join(swap2(4, 3, grid_temp)))
        possible.append(''.join(swap2(4, 5, grid_temp)))
        possible.append(''.join(swap2(4, 7, grid_temp)))
    elif (grid_state.index("0") == 5):
        possible.append(''.join(swap2(5, 2, grid_temp)))
        possible.append(''.join(swap2(5, 4, grid_temp)))
        possible.append(''.join(swap2(5, 8, grid_temp)))
    elif (grid_state.index("0") == 6):
        possible.append(''.join(swap2(6, 3, grid_temp)))
        possible.append(''.join(swap2(6, 7, grid_temp)))
    elif (grid_state.index("0") == 7):
        possible.append(''.join(swap2(7, 4, grid_temp)))
        possible.append(''.join(swap2(7, 6, grid_temp)))
        possible.append(''.join(swap2(7, 8, grid_temp)))
    elif (grid_state.index("0") == 8):
        possible.append(''.join(swap2(8, 5, grid_temp)))
        possible.append(''.join(swap2(8, 7, grid_temp)))
    return possible

def reconstruction():
    global parents
    global steps
    target="012345678"
    c=0
    parent=""
    child=""
    while(parent != "None"):
        for i in range(len(parents)):
            family=str(parents[i]).split(',')
            parent=family[0]
            child=family[1]
            if(child==target):
                steps.append(child)
                target=parent
                break

def Breadth_Frist_Search():
    global nodes_expanded
    global grid_state
    global steps
    frontier = Queue()
    explored = set()
    frontier.enqueue(grid_state)

    while (not frontier.is_empty()):
        state = frontier.dequeue()
        explored.add(state)
        steps.append(state)

        if (check_goal(state)):
            print("congratulation for your sucess")
            return True
        possible_grids = get_possible_moves(state)
        print(possible_grids)
        possible_grids.reverse()
        nodes_expanded = nodes_expanded + 1
        for neighbor in get_possible_moves(state):
            if not frontier.contain(neighbor) and not neighbor in explored:
                frontier.enqueue(neighbor)

    return False

def depth_first_search():
    global nodes_expanded
    global grid_state
    global steps
    global parents
    explored = set()  # Change explored to a set
    frontier = Stack()
    frontier.push(grid_state)
    parents.append("None,"+grid_state)
    while not frontier.is_empty():
        state = frontier.pop()
        explored.add(state)  # Add state to the set
        if state == "012345678":
            print("wiiiin")
            print(parents)
            reconstruction()
            steps.reverse()
            return True
        possible_grids = get_possible_moves(state)
        possible_grids.reverse()
        print(possible_grids)
        nodes_expanded += 1
        for path in possible_grids:
            parents.append(state+","+path)
            if path not in explored and not frontier.contain(path):
                frontier.push(path)
    return False

def next_step():
    global i
    global steps
    global Buttons
    if(i < len(steps)-1):
        i += 1
        for k in range(9):
            Buttons[k].config(text=steps[i][k])

#try 125340678
grid_state = input("Enter grid order: ")
#grid_state = ''.join(map(str, random.sample(range(9), 9)))
print(grid_state)
steps=[]
start_time = time.time()
print(depth_first_search())
#print(Breadth_Frist_Search())
end_time = time.time()
execution_time = end_time - start_time
print(nodes_expanded)
print("Cost : ",nodes_expanded)
print("Path : ",steps)
print("Search depth : ",len(steps))
print("Execution time:", execution_time, "seconds")
grid_state=list(grid_state)
Buttons=list()
r = tk.Tk()
i=0
r.geometry("670x600")
e0 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[0],font=25)
e1 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[1],font=25)
e2 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[2],font=25)
e3 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[3],font=25)
e4 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[4],font=25)
e5 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[5],font=25)
e6 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[6],font=25)
e7 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[7],font=25)
e8 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text=grid_state[8],font=25)
next = Button(r,width=25,height=5, bg='#aa22ff', fg='white',text="Next",font=25,command=lambda: next_step())
Buttons.append(e0)
Buttons.append(e1)
Buttons.append(e2)
Buttons.append(e3)
Buttons.append(e4)
Buttons.append(e5)
Buttons.append(e6)
Buttons.append(e7)
Buttons.append(e8)
r.title('8 puzzle')
e0.grid(row=0, column=0,padx=5,pady=10)
e1.grid(row=0, column=1,padx=5,pady=10)
e2.grid(row=0, column=2,padx=5,pady=10)
e3.grid(row=1, column=0,padx=5,pady=10)
e4.grid(row=1, column=1,padx=5,pady=10)
e5.grid(row=1, column=2,padx=5,pady=10)
e6.grid(row=2, column=0,padx=5,pady=10)
e7.grid(row=2, column=1,padx=5,pady=10)
e8.grid(row=2, column=2,padx=5,pady=10)
next.grid(row=3,column=1,padx=5,pady=10)
r.mainloop()

