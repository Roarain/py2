#coding=utf-8

from Tkinter import *
'''
#RadioButtonTest
root = Tk()
# label = Label(root,text='Hello,Tknter')
# label.pack()
label = Label(root,text='RadioButtonTest')
label.pack()
#Vn means default choic from all riadiobutton
V1 = IntVar()
V1.set(1)

V2=IntVar()
V2.set(2)

V3=IntVar()
V3.set(3)

V4=IntVar()
V4.set(4)



Radiobutton(root,text='roarain',value=1).pack(anchor=N)
# Radiobutton(root,text='roarain',variable=V1,value=1).pack(anchor=N)
Radiobutton(root,text='dog',variable=V2,value=2).pack(anchor=S)
Radiobutton(root,text='cat',variable=V3,value=3).pack(anchor=W)
Radiobutton(root,text='pig',variable=V4,value=4).pack(anchor=E)
root.mainloop()
'''

'''
#CheckButtonTest

root = Tk()
var = IntVar()
c = Checkbutton(root,text='this is roarain',variable = var)
c1 = Checkbutton(root,text='this is dog',variable = var)
c.pack()
c1.pack()
root.mainloop()
'''
'''
#EntryTest

root = Tk()
e = Entry(root)
e.pack(padx=20,pady=20)
e.delete(0,END)
e.insert(0,'This is Roarain,My name is Wangxiaoyu,I`m learning Python...')
root.mainloop()
'''
'''
#listbox test

root = Tk()
listbox = Listbox(root)
listbox.pack(fill=BOTH,expand=False)
for i in ['dog','cat','pig','roarain']:
    listbox.insert(0,i)
root.mainloop()
'''
'''
#Pack test
root = Tk()
# Label(root,text='red',bg='red',fg='white').pack(fill=BOTH)
# Label(root,text='green',bg='green',fg='black').pack(fill=Y)
# Label(root,text='yellow',bg='yellow',fg='black').pack(fill=Y)

Label(root,text='red',bg='red',fg='white').pack(side=LEFT)
Label(root,text='green',bg='green',fg='black').pack(side=RIGHT)
Label(root,text='blue',bg='blue',fg='white').pack(side=BOTTOM)
Label(root,text='yellow',bg='yellow',fg='black').pack(side=TOP)
root.mainloop()
'''

#grid test

root = Tk()
Label(root,text='First Line').grid(row=0)
Label(root,text='Third Line').grid(row=2)
Entry(root).grid(column=0,row=1)
Entry(root).grid(column=1,row=1)



root.mainloop()
