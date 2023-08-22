from tkinter import *
import tkinter.ttk as ttk
from tkinter.constants import *
import PIL.Image, PIL.ImageTk
from tkinter import filedialog
import sys
from tkinter import scrolledtext

import UIApp_Module1_to_integrate as module1
import UIApp_Module2_to_integrate as module2
import UIApp_Module3_to_integrate as module3
import UIApp_Module4_to_integrate as module4
import Fyp_integrated_process as fyp_inte

window = Tk()
window.title("Final Year Project")
window.geometry("1150x100")
window.minsize(1150,910)
window.maxsize(1150,910)
window.configure(background="#000000")

main_canvas = Canvas(window,highlightthickness=0)
main_canvas.place(relx=0, rely=0.11, height=800, width=1150)
main_canvas.configure(background="#505459")


Label4 = Label(window)
Label4.place(relx=0, rely=0, height=53, width=1150)
Label4.configure(background="#783000")
Label4.configure(compound='left')
Label4.configure(padx=10,pady=4)
Label4.configure(anchor='center')
Label4.configure(disabledforeground="#a3a3a3")
Label4.configure(font="-family {Segoe UI} -size 25 -weight bold")
Label4.configure(foreground="#FFFFFF")
Label4.configure(text='''L4 Project - Pixels (Module 01)''')

Label4_2 = Label(window)
Label4_2.place(relx=0, rely=0.989, height=10, width=1150)
Label4_2.configure(background="#783000")
Label4_2.configure(compound='left')
Label4_2.configure(anchor='center')


module1.tab1(main_canvas,Label4)

Button_01 = Button(window, borderwidth=0)
Button_01.place(relx=0, rely=0.06, height=45, width=137)
Button_01.configure(activebackground="#505459")
Button_01.configure(activeforeground="white")
Button_01.configure(background="#505459")
Button_01.configure(command=lambda:press_module_button(1))
Button_01.configure(compound='left')
Button_01.configure(disabledforeground="#a3a3a3")
Button_01.configure(font="-family {Arial} -size 10 -weight bold")
Button_01.configure(foreground="#ffffff")
Button_01.configure(highlightbackground="#d9d9d9")
Button_01.configure(highlightcolor="black")
Button_01.configure(pady="0")
Button_01.configure(text='''MODULE 01''')

Button_02 = Button(window,borderwidth=0)
Button_02.place(relx=0.119, rely=0.06, height=45, width=137)
Button_02.configure(activebackground="#505459")
Button_02.configure(activeforeground="white")
Button_02.configure(background="#000000")
Button_02.configure(command=lambda:press_module_button(2))
Button_02.configure(compound='left')
Button_02.configure(disabledforeground="#a3a3a3")
Button_02.configure(font="-family {Arial} -size 10 -weight bold")
Button_02.configure(foreground="#ffffff")
Button_02.configure(highlightbackground="#d9d9d9")
Button_02.configure(highlightcolor="black")
Button_02.configure(pady="0")
Button_02.configure(text='''MODULE 02''')

Button_03 = Button(window,borderwidth=0)
Button_03.place(relx=0.238, rely=0.06, height=45, width=137)
Button_03.configure(activebackground="#505459")
Button_03.configure(activeforeground="white")
Button_03.configure(background="#000000")
Button_03.configure(command=lambda:press_module_button(3))
Button_03.configure(compound='left')
Button_03.configure(disabledforeground="#a3a3a3")
Button_03.configure(font="-family {Arial} -size 10 -weight bold")
Button_03.configure(foreground="#ffffff")
Button_03.configure(highlightbackground="#d9d9d9")
Button_03.configure(highlightcolor="black")
Button_03.configure(pady="0")
Button_03.configure(text='''MODULE 03''')

Button_04 = Button(window,borderwidth=0)
Button_04.place(relx=0.357, rely=0.06, height=45, width=137)
Button_04.configure(activebackground="#505459")
Button_04.configure(activeforeground="white")
Button_04.configure(background="#000000")
Button_04.configure(command=lambda:press_module_button(4))
Button_04.configure(compound='left')
Button_04.configure(disabledforeground="#a3a3a3")
Button_04.configure(font="-family {Arial} -size 10 -weight bold")
Button_04.configure(foreground="#ffffff")
Button_04.configure(highlightbackground="#d9d9d9")
Button_04.configure(highlightcolor="black")
Button_04.configure(pady="0")
Button_04.configure(text='''MODULE 04''')

Button_05 = Button(window,borderwidth=0)
Button_05.place(relx=0.476, rely=0.06, height=45, width=137)
Button_05.configure(activebackground="#505459")
Button_05.configure(activeforeground="white")
Button_05.configure(background="#000000")
Button_05.configure(command=lambda:press_module_button(5))
Button_05.configure(compound='left')
Button_05.configure(disabledforeground="#a3a3a3")
Button_05.configure(font="-family {Arial} -size 10 -weight bold")
Button_05.configure(foreground="#ffffff")
Button_05.configure(highlightbackground="#d9d9d9")
Button_05.configure(highlightcolor="black")
Button_05.configure(pady="0")
Button_05.configure(text='''INTEGRATED''')

def press_module_button(index):
    if index==1:
        Button_01.configure(background="#505459")
        Button_02.configure(background="#000000")
        Button_03.configure(background="#000000")
        Button_04.configure(background="#000000")
        Button_05.configure(background="#000000")
        module1.tab1(main_canvas,Label4)
    elif index==2: 
        Button_01.configure(background="#000000")
        Button_02.configure(background="#505459")
        Button_03.configure(background="#000000")
        Button_04.configure(background="#000000")
        Button_05.configure(background="#000000")
        module2.tab2(main_canvas,Label4)
    elif index==3: 
        Button_01.configure(background="#000000")
        Button_02.configure(background="#000000")
        Button_03.configure(background="#505459")
        Button_04.configure(background="#000000")
        Button_05.configure(background="#000000")
        module3.tab3(main_canvas,Label4)
    elif index==4: 
        Button_01.configure(background="#000000")
        Button_02.configure(background="#000000")
        Button_03.configure(background="#000000")
        Button_04.configure(background="#505459")
        Button_05.configure(background="#000000")
        module4.tab4(main_canvas,Label4)
    elif index==5: 
        Button_01.configure(background="#000000")
        Button_02.configure(background="#000000")
        Button_03.configure(background="#000000")
        Button_04.configure(background="#000000")
        Button_05.configure(background="#505459")
        fyp_inte.tab5(main_canvas,Label4)
    

window.mainloop()
