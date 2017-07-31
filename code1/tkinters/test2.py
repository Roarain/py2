#coding:utf-8
"""界面编程"""
from Tkinter import *
#清空
def clear():
    display.set('')
#删除
def delete():
    display.set(str(display.get()[:-1]))
#输入
def call(m):
    content = display.get() + m
    display.set(content)
#计算
def he():
    try:
        con = display.get()
        res = eval(con)
        display.set(con + '=' + str(res))
    except:
        display.set('计算错误！！！！')

def main():
    root = Tk()  # 实例化类
    root.title('PYTHON计算器')
    root.geometry()
    global display
    display=StringVar()
    label = Label(root,relief = 'sunken',borderwidth=3,anchor=SE)
    label.config(bg='grey',width=25,height=3)
    label['textvariable'] = display
    label.grid(row=0,column=0,columnspan=4)
    Button(root,text='C',fg='#EF7321',width=3,command=lambda :clear()).grid(row=1,column=0)
    Button(root,text='DEL',width=3,command=lambda :delete()).grid(row=1,column=1)
    Button(root, text='/', width=3, command=lambda: call('/')).grid(row=1, column=2)
    Button(root, text='+', width=3, command=lambda: call('+')).grid(row=1, column=3)
    Button(root, text='-', width=3, command=lambda: call('-')).grid(row=2, column=0)
    Button(root, text='*', width=3, command=lambda: call('*')).grid(row=2, column=1)
    Button(root, text='0', width=3, command=lambda: call('0')).grid(row=2, column=2)
    Button(root, text='1', width=3, command=lambda: call('1')).grid(row=2, column=3)
    Button(root, text='2', width=3, command=lambda: call('2')).grid(row=3, column=0)
    Button(root, text='3', width=3, command=lambda: call('3')).grid(row=3, column=1)
    Button(root, text='4', width=3, command=lambda: call('4')).grid(row=3, column=2)
    Button(root, text='5', width=3, command=lambda: call('5')).grid(row=3, column=3)
    Button(root, text='6', width=3, command=lambda: call('6')).grid(row=4, column=0)
    Button(root, text='7', width=3, command=lambda: call('7')).grid(row=4, column=1)
    Button(root, text='8', width=3, command=lambda: call('8')).grid(row=4, column=2)
    Button(root, text='9', width=3, command=lambda: call('9')).grid(row=4, column=3)
    Button(root, text='=', width=22, command=lambda: he()).grid(row=5, column=0,columnspan=4)
    root.mainloop()  # 显示界面
if __name__ == '__main__':
    main()