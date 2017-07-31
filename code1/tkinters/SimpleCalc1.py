#coding=utf-8
from Tkinter import *

'''
clear() clear all boxes
dele() delete the last character
call() call +++
calcee() calculate the label's value
negate() Calculate negative values
'''
def clear():
    display.set('')
    display2.set('')
def dele():
    display.set(str(display.get()[:-1]))
def call(m):
    contents = display.get() + m
    display.set(contents)
def calcee():
    try:
        con = display.get()
        res = eval(con)
        display2.set(str(res))
    except:
        display.set('Error')
def negate():
    con = display.get()
    res = '-'+con
    display.set(res)

def main():
    root = Tk()
    root.title('RoarainCalc')
    root.geometry()

    global display
    global display2
    display = StringVar()
    display2 = StringVar()
    #First Label
    label = Label(root,relief='sunken',borderwidth=6,anchor=SE)
    label.config(bg='grey',width=25 ,height=3)
    #defalut wording
    label['textvariable'] = display
    label.grid(row=0,column=0,columnspan=4)
    #Second Label
    label2 = Label(root,relief='sunken',borderwidth=6,anchor=SE)
    label2.config(bg='grey',width=25 ,height=3)
    label2['textvariable'] = display2
    label2.grid(row=1,column=0,columnspan=4)

    #First Row
    Button(root,text='C',fg='#EF7321',width=3,command=lambda : clear()).grid(row=2,column=0)
    Button(root, text='DEL',width=3, command=lambda: dele()).grid(row=2, column=2)
    Button(root, text='/', width=3, command=lambda: call('/')).grid(row=2, column=3)
    #Second Row
    Button(root, text='7', width=3, command=lambda: call('7')).grid(row=3, column=0)
    Button(root, text='8', width=3, command=lambda: call('8')).grid(row=3, column=1)
    Button(root, text='9', width=3, command=lambda: call('9')).grid(row=3, column=2)
    Button(root, text='*', width=3, command=lambda: call('*')).grid(row=3, column=3)
    #Third Row
    Button(root, text='4', width=3, command=lambda: call('4')).grid(row=4, column=0)
    Button(root, text='5', width=3, command=lambda: call('5')).grid(row=4, column=1)
    Button(root, text='6', width=3, command=lambda: call('6')).grid(row=4, column=2)
    Button(root, text='-', width=3, command=lambda: call('-')).grid(row=4, column=3)
    #Fourth Row
    Button(root, text='1', width=3, command=lambda: call('1')).grid(row=5, column=0)
    Button(root, text='2', width=3, command=lambda: call('2')).grid(row=5, column=1)
    Button(root, text='3', width=3, command=lambda: call('3')).grid(row=5, column=2)
    Button(root, text='+', width=3, command=lambda: call('+')).grid(row=5, column=3)
    #Fifth Row ±
    Button(root, text='±', width=3, command=lambda: negate()).grid(row=6, column=0)
    Button(root, text='0', width=3, command=lambda: call('0')).grid(row=6, column=1)
    Button(root, text='.', width=3, command=lambda: call('.')).grid(row=6, column=2)
    Button(root, text='=', width=3, command=lambda: calcee()).grid(row=6, column=3)

    root.mainloop()

if __name__ == '__main__':
    main()