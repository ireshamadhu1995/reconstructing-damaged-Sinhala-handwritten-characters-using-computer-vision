from tkinter import *
import tkinter.ttk as ttk
from tkinter.constants import *
import PIL.Image, PIL.ImageTk
from tkinter import filedialog
from tkinter import scrolledtext

import module3_opencv as cdr

#Global Variables
thinned_file_list = []
upload_imgs = []
result_imgs = []
thicked_file_list = []
#Module 3
endtip_coupled_files = []
linked_images = []
thicked_list = []
bnw_list = []
binded_images = []
couples_list = []
log_text = ""
logs = []
linking_logs= []


index = -1
part_index = 0
rgb_converted_files = []
is_result_got = False

def tab3(main_canvas,Label4):
    for widget in main_canvas.winfo_children():
        widget.destroy()
    Label4.configure(text='''L4 Project - Pixels (Module 03)''')
    Frame1 = Frame(main_canvas)
    Frame1.place(relx=0.19, rely=0.02, height=600, width=900)
    Frame1.configure(relief='groove')
    Frame1.configure(borderwidth="8")
    Frame1.configure(relief="groove")
    Frame1.configure(background="#3b3b3b")

    def canvas_left():
        global Canvas1
        Canvas1 = Canvas(Frame1)
        Canvas1.place(relx=0.04, rely=0.1, height=400, width=400)
        Canvas1.configure(background="#000000")
        Canvas1.configure(borderwidth="2")
        Canvas1.configure(insertbackground="black")
        Canvas1.configure(relief="ridge")
        Canvas1.configure(selectbackground="blue")
        Canvas1.configure(selectforeground="white")

    def canvas_right():
        global Canvas2
        Canvas2 = Canvas(Frame1)
        Canvas2.place(relx=0.51, rely=0.1, height=400, width=400)
        Canvas2.configure(background="#000000")
        Canvas2.configure(borderwidth="2")
        Canvas2.configure(insertbackground="black")
        Canvas2.configure(relief="ridge")
        Canvas2.configure(selectbackground="blue")
        Canvas2.configure(selectforeground="white")

    def image_resize(img):
        sizex,sizey = img.size
        if sizex>=sizey:
            print("old size", img.size)
            img=img.resize((370,int(370*sizey/sizex)))
            print("new size", img.size)
        else:
            print("old size", img.size)
            img=img.resize((int(370*sizex/sizey), 370))
            print("new size", img.size)
        return img
    
    def upload_thinned_file():
        global thinned_file_list,upload_imgs,index,result_imgs,is_result_got,log_text,logs
        global Label5
        
        for widget in Canvas1.winfo_children():
            widget.destroy()
        for widget in Canvas2.winfo_children():
            widget.destroy()
        thinned_file_list.clear()
        upload_imgs.clear()
        result_imgs.clear()
        rgb_converted_files.clear()
        linked_images.clear()
        thicked_list.clear()
        bnw_list.clear()
        #thicked_file_list.clear()
        binded_images.clear()
        text.delete(1.0,END)
        log_text = ""
        couples_list.clear()
        linking_logs.clear()
        logs.clear()
        part_index = 0
        is_result_got = False
        f_types = [('PNG Files','*.png'),('Jpg Files', '*.jpg')] 
        filename = filedialog.askopenfilename(multiple=True,filetypes=f_types)
        col=1
        row=3
        for f in filename:
            thinned_file_list.append(f)
            img=PIL.Image.open(f)
            img = image_resize(img)
            img=PIL.ImageTk.PhotoImage(img)
            upload_imgs.append(img)

        index = -1
        image_swap_plus()
        print(filename)
        log = ">> Uploaded Thinned Files..\n"
        data_log(log)

    def upload_thicked_file():
        global thicked_file_list,upload_imgs,index,result_imgs,is_result_got,log_text,logs
        global Label5
        
        for widget in Canvas1.winfo_children():
            widget.destroy()
        for widget in Canvas2.winfo_children():
            widget.destroy()
        thicked_file_list.clear()
        binded_images.clear()
        bnw_list.clear()
        #thinned_file_list.clear()
        upload_imgs.clear()
        result_imgs.clear()
        rgb_converted_files.clear()
        linked_images.clear()
        thicked_list.clear()
        text.delete(1.0,END)
        log_text = ""
        couples_list.clear()
        linking_logs.clear()
        logs.clear()
        part_index = 0
        is_result_got = False
        f_types = [('PNG Files','*.png'),('Jpg Files', '*.jpg')] 
        filename = filedialog.askopenfilename(multiple=True,filetypes=f_types)
        col=1
        row=3
        for f in filename:
            thicked_file_list.append(f)
            img=PIL.Image.open(f)
            img = image_resize(img)
            img=PIL.ImageTk.PhotoImage(img)
            upload_imgs.append(img)

        index = -1
        image_swap_plus()
        print(filename)
        log = ">> Uploaded Thicked Files..\n"
        data_log(log)

    def full_process_of_module3():
        global rgb_converted_files,result_imgs,is_result_got,index,linked_images, thicked_list,bnw_list,thicked_file_list,binded_images
        global part_index,couples_list,linking_logs,endtip_coupled_files
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #linked_images.clear()
        #thicked_list.clear()
        #binded_images.clear()
        #bnw_list.clear()
        if not endtip_coupled_files:
            endtip_coupled_files,couples_list = cdr.final_suitable_mapping(thinned_file_list)
            logs.append(couples_list)
        if not linked_images:
            linked_images,linking_logs = cdr.final_linking(thinned_file_list,10)
            logs.append(linking_logs)
        if not thicked_list:
            thicked_list = cdr.increase_thickness(linked_images)
        if not binded_images:
            binded_images = cdr.pasteSuitableArea(thicked_list,thicked_file_list)
        if not bnw_list:
            bnw_list = cdr.bwConvertitng(binded_images)
        print(bnw_list)
        rgb_converted_files = cdr.display_out(bnw_list)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 0
        Label3.configure(text="Final Results")
        image_swap_plus()

    def findSuitableEndTipCouples():
        global rgb_converted_files,result_imgs,is_result_got,index,endtip_coupled_files,couples_list,logs,part_index
        
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        endtip_coupled_files.clear()
        result_imgs.clear()
        print(thinned_file_list)
        if not endtip_coupled_files:
            endtip_coupled_files,couples_list = cdr.final_suitable_mapping(thinned_file_list)
            logs.append(couples_list)
        print("couples list",couples_list)
        rgb_converted_files = cdr.display_out(endtip_coupled_files)
        print("length ",len(rgb_converted_files))
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 1
        Label3.configure(text="End-Tip Coupled Images")
        image_swap_plus()
        log = ">> Identified all the End-Tip Couples..\n"
        data_log(log)

    def linkSuitableShapeToImages():
        global rgb_converted_files,result_imgs,is_result_got,linked_images,index,linking_logs,part_index
        
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #linked_images.clear()
        print("length file list ",len(thinned_file_list))
        print("file list ",thinned_file_list)
        if not linked_images:
            linked_images,linking_logs = cdr.final_linking(thinned_file_list)
            logs.append(linking_logs)
        print(linked_images)
        rgb_converted_files = cdr.display_out(linked_images)
        print("length ",len(rgb_converted_files))
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 2
        Label3.configure(text="Linked Image")
        image_swap_plus()
        log = ">> Linked Damages Completely..\n"
        data_log(log)

    def increase_thickness_Images():
        global rgb_converted_files,result_imgs,is_result_got,index,linked_images, thicked_list,part_index
        
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #thicked_list.clear()
        if not thicked_list:
            thicked_list = cdr.increase_thickness(linked_images)
        print("thicked list ",thicked_list)
        rgb_converted_files = cdr.display_out(thicked_list)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 0
        Label3.configure(text="Thicked Images")
        image_swap_plus()
        log = ">> Increased Thickness in Images..\n"
        data_log(log)

    def binding_damage_part():
        global rgb_converted_files,result_imgs,is_result_got,index,linked_images, thicked_list, thicked_file_list, binded_images
        global part_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #binded_images.clear()
        print("thick files ",thicked_file_list)
        if not binded_images:
            binded_images = cdr.pasteSuitableArea(thicked_list,thicked_file_list)
        print("thicked list ",binded_images)
        rgb_converted_files = cdr.display_out(binded_images)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 0
        Label3.configure(text="Thicked Images")
        image_swap_plus()
        log = ">> Binded linked parts to original Image..\n"
        data_log(log)

    def bw_convertitng_images():
        global rgb_converted_files,result_imgs,is_result_got,index,linked_images, thicked_list,bnw_list,binded_images
        global part_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #bnw_list.clear()
        print("thicked list after",binded_images)
        if not bnw_list:
            bnw_list = cdr.bwConvertitng(binded_images)
        print(bnw_list)
        rgb_converted_files = cdr.display_out(bnw_list)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 0
        Label3.configure(text="Black & White images")
        image_swap_plus()
        log = ">> Convert images to Black & White..\n"
        data_log(log)

    def image_swap_plus():
        global index,upload_imgs,result_imgs,is_result_got,part_index,logs
        if index == len(upload_imgs)-1:
            index = -1
        index = index+1
        for widget in Canvas1.winfo_children():
            widget.destroy()
        Label1= Label(Canvas1, image=upload_imgs[index])
        Label1.place(x=200,y=200,anchor="center")

        if is_result_got:
            print("part index = ",part_index)
            if part_index == 1 or part_index==2:
                data_log(logs[part_index-1][index])
            for widget in Canvas2.winfo_children():
                widget.destroy()
            Label2= Label(Canvas2, image=result_imgs[index])
            Label2.place(x=200,y=200,anchor="center")
            
    def image_swap_minus():
        global index,result_imgs,upload_imgs,is_result_got,part_index,logs
        if index <= 0:
            index = len(upload_imgs)-1
        index = index-1
        for widget in Canvas1.winfo_children():
            widget.destroy()
        Label1= Label(Canvas1, image=upload_imgs[index])
        Label1.image=upload_imgs[0]
        Label1.place(x=200,y=200,anchor="center")
        
        if is_result_got:
            print("part index = ",part_index)
            if part_index == 1 or part_index==2:
                data_log(logs[part_index-1][index])
            for widget in Canvas2.winfo_children():
                widget.destroy()
            Label2= Label(Canvas2, image=result_imgs[index])
            Label2.place(x=200,y=200,anchor="center")

    def data_log(log):
        text.delete(1.0,END)
        global log_text
        log_text = log_text + log
        text.insert(END,log_text)
        text.see(END)

    canvas_left()
    canvas_right()
    Label2 = Label(Frame1)
    Label2.place(relx=0.088, rely=0.04, height=21, width=284)
    Label2.configure(anchor='w') 
    Label2.configure(background="#3b3b3b")
    Label2.configure(compound='left')
    Label2.configure(disabledforeground="#a3a3a3")
    Label2.configure(font="-family {Segoe UI} -size 11")
    Label2.configure(foreground="#ffffff")
    Label2.configure(text='Original Image')

    Label3 = Label(Frame1)
    Label3.place(relx=0.563, rely=0.04, height=21, width=284)
    Label3.configure(activebackground="#f9f9f9")
    Label3.configure(activeforeground="black")
    Label3.configure(anchor='w')
    Label3.configure(background="#3b3b3b")
    Label3.configure(compound='left')
    Label3.configure(disabledforeground="#a3a3a3")
    Label3.configure(font="-family {Segoe UI} -size 11")
    Label3.configure(foreground="#ffffff")
    Label3.configure(highlightbackground="#d9d9d9")
    Label3.configure(highlightcolor="black")
    Label3.configure(text="")



    Button3 = Button(Frame1)
    Button3.place(relx=0.41, rely=0.88, height=40, width=40)
    Button3.configure(activebackground="#1e1e1e")
    Button3.configure(activeforeground="white")
    Button3.configure(activeforeground="#ffffff")
    Button3.configure(background="#232323")
    Button3.configure(command=lambda:image_swap_minus())
    Button3.configure(compound='left')
    Button3.configure(disabledforeground="#a3a3a3")
    Button3.configure(font="-family {Arial} -size 21 -weight bold")
    Button3.configure(foreground="#ffffff")
    Button3.configure(highlightbackground="#d9d9d9")
    Button3.configure(highlightcolor="black")
    Button3.configure(pady="0")
    Button3.configure(text='''<''')
     
    Button4 = Button(Frame1)
    Button4.place(relx=0.55, rely=0.88, height=40, width=40)
    Button4.configure(activebackground="#1e1e1e")
    Button4.configure(activeforeground="white")
    Button4.configure(activeforeground="#ffffff")
    Button4.configure(background="#232323")
    Button4.configure(command=lambda:image_swap_plus())
    Button4.configure(compound='left')
    Button4.configure(disabledforeground="#a3a3a3")
    Button4.configure(font="-family {Arial} -size 21 -weight bold")
    Button4.configure(foreground="#ffffff")
    Button4.configure(highlightbackground="#d9d9d9")
    Button4.configure(highlightcolor="black")
    Button4.configure(pady="0")
    Button4.configure(text='''>''')

    Frame2 = Frame(main_canvas)
    Frame2.place(relx=0.02, rely=0.02, height=770, width=180)
    Frame2.configure(relief='groove')
    Frame2.configure(borderwidth="2")
    Frame2.configure(relief="groove")
    Frame2.configure(background="#1b1b1b")

    Button1 = Button(Frame2)
    Button1.place(relx=0.07, rely=0.04, height=34, width=155)
    Button1.configure(activebackground="#380900")
    Button1.configure(activeforeground="white")
    Button1.configure(activeforeground="#ffffff")
    Button1.configure(background="#8a1700")
    Button1.configure(command=lambda:upload_thinned_file())
    Button1.configure(compound='left')
    Button1.configure(disabledforeground="#a3a3a3")
    Button1.configure(font="-family {Segoe UI} -size 11 -weight bold")
    Button1.configure(foreground="#ffffff")
    Button1.configure(highlightbackground="#d9d9d9")
    Button1.configure(highlightcolor="black")
    Button1.configure(pady="0")
    Button1.configure(text='''UPLOAD THINNED''')

    Button1_2 = Button(Frame2)
    Button1_2.place(relx=0.07, rely=0.12, height=34, width=155)
    Button1_2.configure(activebackground="#380900")
    Button1_2.configure(activeforeground="white")
    Button1_2.configure(activeforeground="#ffffff")
    Button1_2.configure(background="#8a1700")
    Button1_2.configure(command=lambda:upload_thicked_file())
    Button1_2.configure(compound='left')
    Button1_2.configure(disabledforeground="#a3a3a3")
    Button1_2.configure(font="-family {Segoe UI} -size 9 -weight bold")
    Button1_2.configure(foreground="#ffffff")
    Button1_2.configure(highlightbackground="#d9d9d9")
    Button1_2.configure(highlightcolor="black")
    Button1_2.configure(pady="0")
    Button1_2.configure(text='''UPLOAD BEFORE THIN''')

    Button2 = Button(Frame2)
    Button2.place(relx=0.07, rely=0.20, height=34, width=155)
    Button2.configure(activebackground="#4a1e00")
    Button2.configure(activeforeground="white")
    Button2.configure(activeforeground="#ffffff")
    Button2.configure(background="#783000")
    Button2.configure(command=lambda:full_process_of_module3())
    Button2.configure(compound='left')
    Button2.configure(disabledforeground="#a3a3a3")
    Button2.configure(font="-family {Segoe UI} -size 10 -weight bold")
    Button2.configure(foreground="#ffffff")
    Button2.configure(highlightbackground="#d9d9d9")
    Button2.configure(highlightcolor="black")
    Button2.configure(pady="0")
    Button2.configure(text="FULL PROCESS")

    Button5 = Button(Frame2)
    Button5.place(relx=0.12, rely=0.33, height=45, width=137)
    Button5.configure(activebackground="#1e1e1e")
    Button5.configure(activeforeground="white")
    Button5.configure(background="#232323")
    Button5.configure(command=lambda:findSuitableEndTipCouples())
    Button5.configure(compound='left')
    Button5.configure(disabledforeground="#a3a3a3")
    Button5.configure(font="-family {Arial} -size 10 -weight bold")
    Button5.configure(foreground="#ffffff")
    Button5.configure(highlightbackground="#d9d9d9")
    Button5.configure(highlightcolor="black")
    Button5.configure(pady="0")
    Button5.configure(text='''FIND END-TIPS''')

    Button6 = Button(Frame2)
    Button6.place(relx=0.12, rely=0.41, height=45, width=137)
    Button6.configure(activebackground="#1e1e1e")
    Button6.configure(activeforeground="white")
    Button6.configure(activeforeground="#ffffff")
    Button6.configure(background="#232323")
    Button6.configure(command=lambda:linkSuitableShapeToImages())
    Button6.configure(compound='left')
    Button6.configure(disabledforeground="#a3a3a3")
    Button6.configure(font="-family {Arial} -size 10 -weight bold")
    Button6.configure(foreground="#ffffff")
    Button6.configure(highlightbackground="#d9d9d9")
    Button6.configure(highlightcolor="black")
    Button6.configure(pady="0")
    Button6.configure(text='''EDGE LINKING''')

    Button7 = Button(Frame2)
    Button7.place(relx=0.12, rely=0.49, height=45, width=137)
    Button7.configure(activebackground="#1e1e1e")
    Button7.configure(activeforeground="white")
    Button7.configure(activeforeground="#ffffff")
    Button7.configure(background="#232323")
    Button7.configure(command=lambda:increase_thickness_Images())
    Button7.configure(compound='left')
    Button7.configure(disabledforeground="#a3a3a3")
    Button7.configure(font="-family {Arial} -size 10 -weight bold ")
    Button7.configure(wraplength=130)
    Button7.configure(foreground="#ffffff")
    Button7.configure(highlightbackground="#d9d9d9")
    Button7.configure(highlightcolor="black")
    Button7.configure(pady="0")
    Button7.configure(text='''INCREASE THICKNESS''')

    Button9 = Button(Frame2)
    Button9.place(relx=0.12, rely=0.57, height=45, width=137)
    Button9.configure(activebackground="#1e1e1e")
    Button9.configure(activeforeground="white")
    Button9.configure(activeforeground="#ffffff")
    Button9.configure(background="#232323")
    Button9.configure(command=lambda:binding_damage_part())
    Button9.configure(compound='left')
    Button9.configure(disabledforeground="#a3a3a3")
    Button9.configure(font="-family {Arial} -size 10 -weight bold ")
    Button9.configure(wraplength=130)
    Button9.configure(foreground="#ffffff")
    Button9.configure(highlightbackground="#d9d9d9")
    Button9.configure(highlightcolor="black")
    Button9.configure(pady="0")
    Button9.configure(text='''BINDING DAMAGE PART''')

    Button8 = Button(Frame2)
    Button8.place(relx=0.12, rely=0.65, height=45, width=137)
    Button8.configure(activebackground="#1e1e1e")
    Button8.configure(activeforeground="white")
    Button8.configure(activeforeground="#ffffff")
    Button8.configure(background="#232323")
    Button8.configure(command=lambda:bw_convertitng_images())
    Button8.configure(compound='left')
    Button8.configure(disabledforeground="#a3a3a3")
    Button8.configure(font="-family {Arial} -size 10 -weight bold ")
    Button8.configure(wraplength=130)
    Button8.configure(foreground="#ffffff")
    Button8.configure(highlightbackground="#d9d9d9")
    Button8.configure(highlightcolor="black")
    Button8.configure(pady="0")
    Button8.configure(text='''BLACK & WHITE CONVERT''')

    Frame3 = Frame(main_canvas)
    Frame3.place(relx=0.19, rely=0.78, height=165, width=900)
    Frame3.configure(relief='groove')
    Frame3.configure(borderwidth="2")
    Frame3.configure(relief="groove")
    Frame3.configure(background="#1c211c")

    text = scrolledtext.ScrolledText(Frame3,wrap =WORD, font = ("Times New Roman",15))
    text.configure(background = "#000000")
    text.configure(foreground = "green")
    text.vbar.configure(troughcolor ="#000000")
    text.place(relx=0.009, rely=0.029, height=150, width=880)



    #Label4 = Label(window)
    #Label4.place(relx=0.0, rely=0.029, height=51, width=1004)
    #Label4.configure(background="#d9d9d9")
    #Label4.configure(compound='left')
    #Label4.configure(padx=10,pady=4)
    #Label4.configure(anchor='center')
    #Label4.configure(disabledforeground="#a3a3a3")
    #Label4.configure(font="-family {Segoe UI} -size 28 -weight bold")
    #Label4.configure(foreground="#000000")
    #Label4.configure(text='''L4 Project - Pixels (MODULE 3)''')

