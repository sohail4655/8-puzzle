import math
import time
import tkinter as tk
import random
from tkinter import *
class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def top(self):
        return self.list[-1]

    def is_empty(self):
        return len(self.list) == 0

    def contain(self,value):
        return value in self.list

nodes_expanded=0
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
        possible.append(''.join(swap2(7, 6, grid_temp)))
        possible.append(''.join(swap2(7, 8, grid_temp)))
        possible.append(''.join(swap2(7, 4, grid_temp)))
    elif (grid_state.index("0") == 8):
        possible.append(''.join(swap2(8, 5, grid_temp)))
        possible.append(''.join(swap2(8, 7, grid_temp)))
    return possible

def depth_first_search():
    global nodes_expanded
    global grid_state
    global steps
    explored=list()
    frontier=Stack()
    frontier.push(grid_state)
    while(not frontier.is_empty()):
        state=frontier.pop()
        steps.append(state)
        explored.append(state)
        if(check_goal(state)):
            print("wiiiin")
            return True
        possible_grids=get_possible_moves(state)
        print(possible_grids)
        possible_grids.reverse()
        nodes_expanded=nodes_expanded+1
        for path in possible_grids:
            if(not explored.__contains__(path) and not frontier.contain(path)):
                frontier.push(path)
    return False


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
def flip(grid,button,text):
   global grid_state
   global Buttons
   row = grid["row"]
   column = grid["column"]
   blank = grid_state.index("0")
   blank_row = math.floor(blank / 3)
   blank_column = blank % 3
   if((row == blank_row+1 and column == blank_column) or (row == blank_row-1 and column == blank_column) or (column == blank_column+1 and row ==blank_row) or (column == blank_column-1 and row ==blank_row)):
        temp1=blank_row
        temp2=blank_column
        blank_row=row
        blank_column=column
        row=temp1
        column=temp2
        Buttons[blank].grid_forget()
        button.grid_forget()
        Buttons[blank].grid(row=blank_row, column=blank_column,padx=5,pady=10)
        button.grid(row=row,column=column,padx=5,pady=10)
        grid_state=swap(grid_state.index("0"),grid_state.index(text),grid_state)
def flip2(row,column,text):
    global Buttons
    global grid_state
    blank=grid_state.index("0")
    blank_row = math.floor(blank / 3)
    blank_column = blank % 3
    temp1 = blank_row
    temp2 = blank_column
    blank_row = row
    blank_column = column
    row = temp1
    column = temp2
    Buttons[blank].grid_forget()
    Buttons[grid_state.index(text)].grid_forget()
    Buttons[blank].grid(row=blank_row, column=blank_column, padx=5, pady=10)
    Buttons[grid_state.index(text)].grid(row=row, column=column, padx=5, pady=10)
    Buttons[blank], Buttons[grid_state.index(text)] = Buttons[grid_state.index(text)], Buttons[blank]
    grid_state = swap(blank, grid_state.index(text), grid_state)


def next_step():
    global i
    global steps
    if(i < len(steps)-1):
        blank_place=-1
        str1=steps[i]
        str2=steps[i+1]
        for j in range(len(str1)):
            if(str1[j]!=str2[j] and str2[j] == "0"):
                blank_place=j
        row= math.floor(blank_place/3)
        column = blank_place%3
        flip2(row,column,str1[blank_place])
        i=i+1




#try 125340678
grid_state = input("Enter grid order: ")
#grid_state = ''.join(map(str, random.sample(range(9), 9)))
print(grid_state)
steps=[]
start_time = time.time()
print(depth_first_search())
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


