import math
from math import sqrt
import time
import tkinter as tk
import random
from tkinter import *
from queue import PriorityQueue

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

class aStarNode:
    def __init__(self, value, weight,parent):
        self.value = value
        self.weight = weight
        self.parent = parent

    def __lt__(self, other):
        return self.weight < other.weight
    
    
def check_goal(grid_state):
    if(grid_state =="012345678"):
        return True
    else:
        return False

def swap(i,j,grid):
    temp= list(grid)
    copied=temp[:]
    temp2=copied[i]
    copied[i]=copied[j]
    copied[j]=temp2
    return copied

def get_manhattan_distance(state):
    distance = 0
    for i in range(9):
        current_row = i/3
        current_col = i%3
        goal_row = state[i] /3
        goal_col = state[i]%3
        diff = abs(current_col-goal_col) + abs (current_row - goal_row)
        distance += diff
    return distance

def get_euclidean_distance(state):
    distance = 0
    for i in range(9):
        current_row = i/3
        current_col = i%3
        goal_row = state[i] /3
        goal_col = state[i]%3
        x = (current_col-goal_col)
        y = (current_row - goal_row)
        diff = sqrt(x*x + y*y)
        distance += diff
    return distance

def update_priority(pq, node_value, new_weight):
    temp_pq = PriorityQueue()
    updated = False
    while not pq.empty():
        node = pq.get()
        if node.value == node_value:
            if node.weight > new_weight:
                node.weight = new_weight
                updated = True
            temp_pq.put(node)
        else:
            temp_pq.put(node)
    if updated:
        pq.queue = temp_pq.queue

def get_possible_moves(grid_state):
    grid_temp=list(grid_state)
    possible=[]
    if(grid_state.index("0")==0):
        possible.append(''.join(swap(0,1,grid_temp)))
        possible.append(''.join(swap(0,3, grid_temp)))
    elif(grid_state.index("0")==1):
        possible.append(''.join(swap(1, 0, grid_temp)))
        possible.append(''.join(swap(1, 2, grid_temp)))
        possible.append(''.join(swap(1, 4, grid_temp)))
    elif (grid_state.index("0") == 2):
        possible.append(''.join(swap(2, 1, grid_temp)))
        possible.append(''.join(swap(2, 5, grid_temp)))
    elif (grid_state.index("0") == 3):
        possible.append(''.join(swap(3, 0, grid_temp)))
        possible.append(''.join(swap(3, 4, grid_temp)))
        possible.append(''.join(swap(3, 6, grid_temp)))
    elif (grid_state.index("0") == 4):
        possible.append(''.join(swap(4, 1, grid_temp)))
        possible.append(''.join(swap(4, 3, grid_temp)))
        possible.append(''.join(swap(4, 5, grid_temp)))
        possible.append(''.join(swap(4, 7, grid_temp)))
    elif (grid_state.index("0") == 5):
        possible.append(''.join(swap(5, 2, grid_temp)))
        possible.append(''.join(swap(5, 4, grid_temp)))
        possible.append(''.join(swap(5, 8, grid_temp)))
    elif (grid_state.index("0") == 6):
        possible.append(''.join(swap(6, 3, grid_temp)))
        possible.append(''.join(swap(6, 7, grid_temp)))
    elif (grid_state.index("0") == 7):
        possible.append(''.join(swap(7, 4, grid_temp)))
        possible.append(''.join(swap(7, 6, grid_temp)))
        possible.append(''.join(swap(7, 8, grid_temp)))
    elif (grid_state.index("0") == 8):
        possible.append(''.join(swap(8, 5, grid_temp)))
        possible.append(''.join(swap(8, 7, grid_temp)))
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
    start_time = time.time()
    global nodes_expanded
    global grid_state
    global steps
    global parents
    global grid_var
    grid_state = grid_var.get()
    adjust_buttons()
    frontier = Queue()
    explored = set()
    frontier.enqueue(grid_state)

    while (not frontier.is_empty()):
        state = frontier.dequeue()
        explored.add(state)
        steps.append(state)

        if (check_goal(state)):
            end_time = time.time()
            execution_time = end_time - start_time
            reconstruction()
            steps.reverse()
            set_results()
            print("Execution time:", execution_time, "seconds")
            return True
        possible_grids = get_possible_moves(state)
        print(possible_grids)
        possible_grids.reverse()
        nodes_expanded = nodes_expanded + 1
        for neighbor in get_possible_moves(state):
            parents.append(state + "," + neighbor)
            if not frontier.contain(neighbor) and not neighbor in explored:
                frontier.enqueue(neighbor)

    return False


def aStar():
    start_time = time.time()
    global nodes_expanded
    global grid_state
    global steps
    global parents
    global grid_var
    grid_state = grid_var.get()
    adjust_buttons()
    explored = set()  # Change explored to a set
    frontier = PriorityQueue()
    frontier.put((0,grid_state))
    parents.append("None,"+grid_state)
    while not frontier.is_empty():
        state = frontier.get()
        explored.add(state)  # Add state to the set
        if state == "012345678":
            end_time = time.time()
            execution_time = end_time - start_time
            reconstruction()
            steps.reverse()
            set_results()
            print("Execution time:", execution_time, "seconds")
            return True
        possible_grids = get_possible_moves(state)
        possible_grids.reverse()
        print(possible_grids)
        nodes_expanded += 1
        for path in possible_grids:
            parents.append(state+","+path)
            if path not in explored and not frontier.contain(path):
                frontier.put((path))
    return False



def depth_first_search():
    start_time = time.time()
    global nodes_expanded
    global grid_state
    global steps
    global parents
    global grid_var
    grid_state=grid_var.get()
    adjust_buttons()
    explored = set()  # Change explored to a set
    frontier = Stack()
    frontier.push(grid_state)
    parents.append("None,"+grid_state)
    while not frontier.is_empty():
        state = frontier.pop()
        explored.add(state)  # Add state to the set
        if state == "012345678":
            end_time = time.time()
            execution_time = end_time - start_time
            reconstruction()
            steps.reverse()
            set_results()
            print("Execution time:", execution_time, "seconds")
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
def transition_step(type):
    global i
    global steps
    global Buttons
    if(type == "next"):
        i=i+1
        if (i > len(steps)-1):
            i = i - 1
            return
    else:
        i=i-1
        if(i<0):
            i=i+1
            return
    for k in range(9):
        Buttons[k].config(text=steps[i][k])
def adjust_buttons():
    global Buttons
    global grid_state
    for k in range(9):
        Buttons[k].config(text=grid_state[k])
def set_results():
    global cost_blank
    global node_blank
    global search_blank
    global goal_blank
    global steps
    global nodes_expanded
    cost_blank.config(text=nodes_expanded)
    node_blank.config(text=nodes_expanded)
    search_blank.config(text=len(steps))
    goal_blank.config(text=len(steps))

grid_state=""
steps=[]
Buttons=list()
r = tk.Tk()
grid_var=tk.StringVar()
i=0
r.geometry("1300x800")
name_label = tk.Label(r, text='Enter the Grid', font=('calibre', 18, 'bold'))
grid_entry = tk.Entry(r, textvariable=grid_var, font=('calibre', 18, 'normal'))
cost = tk.Label(r, text='Cost :', font=('calibre', 18, 'bold'))
cost_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
nodes_expand = tk.Label(r, text='Nodes Expanded :', font=('calibre', 18, 'bold'))
node_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
search_depth = tk.Label(r, text='Search depth :', font=('calibre', 18, 'bold'))
search_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
goal_depth = tk.Label(r, text='Goal depth :', font=('calibre', 18, 'bold'))
goal_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
grid_list=list(grid_state)
e0 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="0",font=25)
e1 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="1",font=25)
e2 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="2",font=25)
e3 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="3",font=25)
e4 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="4",font=25)
e5 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="5",font=25)
e6 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="6",font=25)
e7 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="7",font=25)
e8 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="8",font=25)
next_button = Button(r,width=25,height=5, bg='#aa22ff', fg='white',text="Next",font=25,command=lambda: transition_step("next"))
previous = Button(r,width=25,height=5, bg='#aa22ff', fg='white',text="Previous",font=25,command=lambda: transition_step("previous"))
start_dfs = Button(r,width=15,height=5, bg='#0c0201', fg='white',text="DFS",font=25,command=lambda: depth_first_search())
start_bfs = Button(r,width=15,height=5, bg='#0c0201', fg='white',text="BFS",font=25,command=lambda: Breadth_Frist_Search())
start_Astar = Button(r,width=15,height=5, bg='#0c0201', fg='white',text="A *",font=25,command=lambda: aStar())
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
name_label.grid(row=0, column=3,padx=5,pady=10)
grid_entry.grid(row=0, column=4,padx=5,pady=10)
cost.grid(row=1, column=3,padx=5,pady=10)
cost_blank.grid(row=1, column=4,padx=5,pady=10)
nodes_expand.grid(row=2, column=3,padx=5,pady=10)
node_blank.grid(row=2, column=4,padx=5,pady=10)
search_depth.grid(row=3, column=3,padx=5,pady=10)
search_blank.grid(row=3, column=4,padx=5,pady=10)
goal_depth.grid(row=4, column=3,padx=5,pady=10)
goal_blank.grid(row=4, column=4,padx=5,pady=10)
e0.grid(row=0, column=0,padx=5,pady=10)
e1.grid(row=0, column=1,padx=5,pady=10)
e2.grid(row=0, column=2,padx=5,pady=10)
e3.grid(row=1, column=0,padx=5,pady=10)
e4.grid(row=1, column=1,padx=5,pady=10)
e5.grid(row=1, column=2,padx=5,pady=10)
e6.grid(row=2, column=0,padx=5,pady=10)
e7.grid(row=2, column=1,padx=5,pady=10)
e8.grid(row=2, column=2,padx=5,pady=10)
next_button.grid(row=3,column=0,padx=5,pady=10)
previous.grid(row=3,column=2,padx=5,pady=10)
start_dfs.grid(row=4,column=0,padx=5,pady=10)
start_bfs.grid(row=4,column=1,padx=5,pady=10)
start_Astar.grid(row=4,column=2,padx=5,pady=10)
r.mainloop()

