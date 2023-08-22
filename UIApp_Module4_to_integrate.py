from tkinter import *
import tkinter.ttk as ttk
from tkinter.constants import *
import PIL.Image, PIL.ImageTk
from tkinter import filedialog
import sys
import os
from tkinter import scrolledtext


import Module4_opencv as cdr

#Global Variables
upload_imgs = []
result_imgs = []
dir_list = []
org_images = []
predicted_list = []
converted_org_images = []

logs = []
log_text = ""
index = -1
folder_index = -1
part_index = 0
rgb_converted_files = []
is_result_got = False

def tab4(main_canvas,Label4):
    for widget in main_canvas.winfo_children():
        widget.destroy()
    Label4.configure(text='''L4 Project - Pixels (Module 04)''')
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

    def upload_file():
        global org_images,upload_imgs,index,folder_index,result_imgs,is_result_got,logs,dir_list,converted_org_images
        global Label5,part_index,predicted_list
        
        for widget in Canvas1.winfo_children():
            widget.destroy()
        for widget in Canvas2.winfo_children():
            widget.destroy()
        #file_list.clear()
        logs.clear()
        upload_imgs.clear()
        result_imgs.clear()
        org_images.clear()
        predicted_list.clear()
        converted_org_images.clear()
        dir_list.clear()
        log_text = ""
        text.delete(1.0,END)
        part_index = 0
        is_result_got = False
        #f_types = [('PNG Files','*.png'),('Jpg Files', '*.jpg')] 
        filename = filedialog.askdirectory()
        dir_list,org_images = cdr.getRootDir(filename)
        col=1
        row=3
        print("file dir list",dir_list)
        print("file dir list",org_images)

        for rgb_converted_files in org_images:
            rgb_result = []
            for rgb_file in rgb_converted_files:
                im = PIL.Image.fromarray(rgb_file)
                sizex,sizey = im.size
                print("old size", im.size)
                im=im.resize((150,int(150*sizey/sizex)))
                img = PIL.ImageTk.PhotoImage(image=im)
                rgb_result.append(img)
            converted_org_images.append(rgb_result)
        
        index = -1
        folder_index = -1
        folder_swap_plus()
        Label3.configure(text="")
        Label3_2.configure(text="")
        #image_swap_plus()
        log = ">>> Image Files are Loaded into Application...\n"
        #data_log(log)
        #return filename

    def full_process_of_module2():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,clustered_files,with_contours_list,with_damaged_edges,thininng_result_list,logs
        global thinning_logs,part_index,boundaries_logs,damaged_edges_logs,logs
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        if not denoized_files:
            denoized_files = cdr.denoisingImage(file_list)
        if not clustered_files:
            clustered_files = cdr.clustering_image(denoized_files)
        if not with_contours_list:
            with_contours_list,boundaries_logs = cdr.extract_damage_boundaries(clustered_files)
            logs.append(boundaries_logs)
        if not with_damaged_edges:
            with_damaged_edges,damaged_edges_logs = cdr.find_damaged_edges(with_contours_list)
            logs.append(damaged_edges_logs)
        if not thininng_result_list:
            thininng_result_list,thinning_logs = cdr.thinning_result(with_damaged_edges)
            logs.append(thinning_logs)
        print(thininng_result_list)
        rgb_converted_files = cdr.display_out(thininng_result_list)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            sizex,sizey = im.size
            print("old size", im.size)
            im=im.resize((150,int(150*sizey/sizex)))
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 3
        Label3.configure(text="Final Results")
        image_swap_plus()
        log = ">>> Finished the full process of MODULE 02...\n"
        data_log(log)

    def start_prediction_process():
        global rgb_converted_files,result_imgs,is_result_got,index,dir_list,predicted_list
        global part_index,folder_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        #rgb_converted_files.clear()
        #denoized_files.clear()
        result_imgs.clear()
        #print(file_list)
        if not predicted_list:
            predicted_list = cdr.PredictionProcess(dir_list)

        is_result_got = True
        index = -1
        folder_index = -1
        folder_swap_plus()
        #part_index = 0
        Label3.configure(text="Predicted Character")
        #image_swap_plus()
        #log = ">>> Denoised all image segments...\n"
        #data_log(log)

    def start_clustering_process():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,clustered_files,logs
        global part_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #clustered_files.clear()
        if not clustered_files:
            clustered_files = cdr.clustering_image(denoized_files)
        print(clustered_files)
        rgb_converted_files = cdr.display_out(clustered_files)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            sizex,sizey = im.size
            print("old size", im.size)
            im=im.resize((150,int(150*sizey/sizex)))
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 0
        Label3.configure(text="Clustered Image")
        image_swap_plus()
        log = ">>> Clustered all image segments...\n"
        data_log(log)

    def start_damage_boundaries():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,clustered_files,with_contours_list,logs
        global boundaries_logs,part_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        with_contours_list.clear()
        if not with_contours_list:
            with_contours_list,boundaries_logs = cdr.extract_damage_boundaries(clustered_files)
            logs.append(boundaries_logs)
        print("log 1 ",boundaries_logs)
        print(with_contours_list)
        rgb_converted_files = cdr.display_out(with_contours_list)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            sizex,sizey = im.size
            print("old size", im.size)
            im=im.resize((150,int(150*sizey/sizex)))
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 1
        Label3.configure(text="Damage Boundaries")
        image_swap_plus()
        log = ">>> Found all dmaged boundaries of images...\n"
        data_log(log)

    def characters_with_damaged_edges():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,clustered_files,with_contours_list,with_damaged_edges,logs
        global damaged_edges_logs,part_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #with_damaged_edges.clear()
        if not with_damaged_edges:
            with_damaged_edges,damaged_edges_logs = cdr.find_damaged_edges(with_contours_list)
            logs.append(damaged_edges_logs)
        print(with_damaged_edges)
        rgb_converted_files = cdr.display_out(with_damaged_edges)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            sizex,sizey = im.size
            print("old size", im.size)
            im=im.resize((150,int(150*sizey/sizex)))
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 2
        Label3.configure(text="Characters with Damaged Edges")
        image_swap_plus()
        log = ">>> Identified the damaged edges...\n"
        data_log(log)

    def thinning_the_result():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,clustered_files,with_contours_list,with_damaged_edges,thininng_result_list,logs
        global thinning_logs,part_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #thininng_result_list.clear()
        if not thininng_result_list:
            thininng_result_list,thinning_logs = cdr.thinning_result(with_damaged_edges)
            logs.append(thinning_logs)
        print(thininng_result_list)
        rgb_converted_files = cdr.display_out(thininng_result_list)
        print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            sizex,sizey = im.size
            print("old size", im.size)
            im=im.resize((150,int(150*sizey/sizex)))
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        part_index = 3
        Label3.configure(text="After Thinning")
        image_swap_plus()
        log = ">>> Thinned the characters and identified real endtips...\n"
        data_log(log)

    def folder_swap_plus():
        global index,folder_index,converted_org_images
        if folder_index == len(converted_org_images)-1:
            folder_index = -1
        folder_index = folder_index + 1
        print("folder index",folder_index)
        print("files ",converted_org_images[folder_index])
        print("directory ",dir_list[folder_index])
        print("folderName ",os.path.basename(os.path.dirname(dir_list[folder_index])))
        Label2_2.configure(text=os.path.basename(os.path.dirname(dir_list[folder_index])))
        index = -1
        image_swap_plus()

    def folder_swap_minus():
        global index,folder_index,converted_org_images
        if folder_index <= 0:
            folder_index = len(converted_org_images)-1
        folder_index = folder_index - 1
        print("folder index",folder_index)
        print("files ",converted_org_images[folder_index])
        print("directory ",dir_list[folder_index])
        Label2_2.configure(text=os.path.basename(os.path.dirname(dir_list[folder_index])))
        index = -1
        image_swap_minus()

    def image_swap_plus():
        global index,upload_imgs,result_imgs,is_result_got,logs,part_index,folder_index,converted_org_images
        if index == len(converted_org_images[folder_index])-1:
            index = -1
        index = index+1
        print ("index = ",index, " part_index = ",part_index)
        for widget in Canvas1.winfo_children():
            widget.destroy()
        if converted_org_images[folder_index]:
            Label1= Label(Canvas1, image=converted_org_images[folder_index][index])
            Label1.place(x=150,y=150,anchor="center")

        if is_result_got:
            print("result got...")
            #if part_index==1 or part_index==2 or part_index==3:
            #    data_log(logs[part_index-1][index])
            for widget in Canvas2.winfo_children():
                widget.destroy()
            if predicted_list[folder_index]:
                right_label(predicted_list[folder_index][index])
                word = ""
                for char in predicted_list[folder_index]:
                    word = word + char
                Label3_2.configure(text="' "+word+" '")
            else:
                Label3_2.configure(text="")
            #Label2= Label(Canvas2, image=result_imgs[index])
            #Label2.place(x=150,y=150,anchor="center")
            
    def image_swap_minus():
        global index,result_imgs,upload_imgs,is_result_got,logs,part_index,converted_org_images
        if index <= 0:
            index = len(converted_org_images[folder_index])-1
        index = index-1
        for widget in Canvas1.winfo_children():
            widget.destroy()
        if converted_org_images[folder_index]: 
            Label1= Label(Canvas1, image=converted_org_images[folder_index][index])
            
            #Label1.image=upload_imgs[0]
            Label1.place(x=150,y=150,anchor="center")
        
        if is_result_got:
            #if part_index==1 or part_index==2 or part_index==3:
            #    data_log(logs[part_index-1][index])
            for widget in Canvas2.winfo_children():
                widget.destroy()
            if predicted_list[folder_index]:
                right_label(predicted_list[folder_index][index])
                word = ""
                for char in predicted_list[folder_index]:
                    word = word + char
                Label3_2.configure(text="' "+word+" '")
            else:
                Label3_2.configure(text="")
            
            
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

    Label2_2 = Label(Frame1, highlightthickness=2, highlightbackground="#ffffff")
    Label2_2.place(relx=0.095, rely=0.75, height=40, width=300)
    Label2_2.configure(anchor='center')
    Label2_2.configure(background="#2b2b2b")
    Label2_2.configure(compound='left')
    Label2_2.configure(disabledforeground="#a3a3a3")
    Label2_2.configure(font="-family {Segoe UI} -size 11")
    Label2_2.configure(foreground="#ffffff")
    #Label2_2.configure(text='Original Image')

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


    Label3_2 = Label(Frame1, highlightthickness=2, highlightbackground="#ffffff")
    Label3_2.place(relx=0.57, rely=0.75, height=40, width=300)
    Label3_2.configure(activebackground="#f9f9f9")
    Label3_2.configure(activeforeground="black")
    Label3_2.configure(anchor='center')
    Label3_2.configure(background="#2b2b2b")
    Label3_2.configure(compound='left')
    Label3_2.configure(disabledforeground="#a3a3a3")
    Label3_2.configure(font="-family {Segoe UI} -size 11")
    Label3_2.configure(foreground="#ffffff")
    Label3_2.configure(highlightbackground="#d9d9d9")
    Label3_2.configure(highlightcolor="black")
        

    def right_label(label_text):
        Label5 = Label(Canvas2)
        Label5.place(relx=0.25, rely=0.25, height=150, width=150)
        Label5.configure(anchor='center')
        Label5.configure(background="#000000")
        Label5.configure(compound='center')
        Label5.configure(disabledforeground="#a3a3a3")
        Label5.configure(font="-family {Segoe UI} -size 40")
        Label5.configure(foreground="#ffffff")
        Label5.configure(text=label_text)

    #right_label("A")

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

    Button3_2 = Button(Frame1)
    Button3_2.place(relx=0.33, rely=0.88, height=40, width=50)
    Button3_2.configure(activebackground="#1e1e1e")
    Button3_2.configure(activeforeground="white")
    Button3_2.configure(activeforeground="#ffffff")
    Button3_2.configure(background="#232323")
    Button3_2.configure(command=lambda:folder_swap_minus())
    Button3_2.configure(compound='left')
    Button3_2.configure(disabledforeground="#a3a3a3")
    Button3_2.configure(font="-family {Arial} -size 21 -weight bold")
    Button3_2.configure(foreground="#ffffff")
    Button3_2.configure(highlightbackground="#d9d9d9")
    Button3_2.configure(highlightcolor="black")
    Button3_2.configure(pady="0")
    Button3_2.configure(text='''<<''')
     
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

    Button4_2 = Button(Frame1)
    Button4_2.place(relx=0.615, rely=0.88, height=40, width=50)
    Button4_2.configure(activebackground="#1e1e1e")
    Button4_2.configure(activeforeground="white")
    Button4_2.configure(activeforeground="#ffffff")
    Button4_2.configure(background="#232323")
    Button4_2.configure(command=lambda:folder_swap_plus())
    Button4_2.configure(compound='left')
    Button4_2.configure(disabledforeground="#a3a3a3")
    Button4_2.configure(font="-family {Arial} -size 21 -weight bold")
    Button4_2.configure(foreground="#ffffff")
    Button4_2.configure(highlightbackground="#d9d9d9")
    Button4_2.configure(highlightcolor="black")
    Button4_2.configure(pady="0")
    Button4_2.configure(text='''>>''')

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
    Button1.configure(command=lambda:upload_file())
    Button1.configure(compound='left')
    Button1.configure(disabledforeground="#a3a3a3")
    Button1.configure(font="-family {Segoe UI} -size 11 -weight bold")
    Button1.configure(foreground="#ffffff")
    Button1.configure(highlightbackground="#d9d9d9")
    Button1.configure(highlightcolor="black")
    Button1.configure(pady="0")
    Button1.configure(text='''UPLOAD''')

    #Button2 = Button(Frame2)
    #Button2.place(relx=0.07, rely=0.12, height=34, width=155)
    #Button2.configure(activebackground="#4a1e00")
    #Button2.configure(activeforeground="white")
    #Button2.configure(activeforeground="#ffffff")
    #Button2.configure(background="#783000")
    #Button2.configure(command=lambda:full_process_of_module2())
    #Button2.configure(compound='left')
    #Button2.configure(disabledforeground="#a3a3a3")
    #Button2.configure(font="-family {Segoe UI} -size 10 -weight bold")
    #Button2.configure(foreground="#ffffff")
    #Button2.configure(highlightbackground="#d9d9d9")
    #Button2.configure(highlightcolor="black")
    #Button2.configure(pady="0")
    #Button2.configure(text="FULL PROCESS")

    Button5 = Button(Frame2)
    Button5.place(relx=0.12, rely=0.25, height=45, width=137)
    Button5.configure(activebackground="#1e1e1e")
    Button5.configure(activeforeground="white")
    Button5.configure(background="#232323")
    Button5.configure(command=lambda:start_prediction_process())
    Button5.configure(compound='left')
    Button5.configure(disabledforeground="#a3a3a3")
    Button5.configure(font="-family {Arial} -size 10 -weight bold")
    Button5.configure(foreground="#ffffff")
    Button5.configure(highlightbackground="#d9d9d9")
    Button5.configure(highlightcolor="black")
    Button5.configure(pady="0")
    Button5.configure(text='''PREDICITON''')

    #Button6 = Button(Frame2)
    #Button6.place(relx=0.12, rely=0.35, height=45, width=137)
    #Button6.configure(activebackground="#1e1e1e")
    #Button6.configure(activeforeground="white")
    #Button6.configure(activeforeground="#ffffff")
    #Button6.configure(background="#232323")
    #Button6.configure(command=lambda:start_clustering_process())
    #Button6.configure(compound='left')
    #Button6.configure(disabledforeground="#a3a3a3")
    #Button6.configure(font="-family {Arial} -size 10 -weight bold")
    #Button6.configure(foreground="#ffffff")
    #Button6.configure(highlightbackground="#d9d9d9")
    #Button6.configure(highlightcolor="black")
    #Button6.configure(pady="0")
    #Button6.configure(text='''CLUSTERING''')

    #Button7 = Button(Frame2)
    #Button7.place(relx=0.12, rely=0.45, height=45, width=137)
    #Button7.configure(activebackground="#1e1e1e")
    #Button7.configure(activeforeground="white")
    #Button7.configure(activeforeground="#ffffff")
    #Button7.configure(background="#232323")
    #Button7.configure(command=lambda:start_damage_boundaries())
    #Button7.configure(compound='left')
    #Button7.configure(disabledforeground="#a3a3a3")
    #Button7.configure(font="-family {Arial} -size 10 -weight bold ")
    #Button7.configure(wraplength=130)
    #Button7.configure(foreground="#ffffff")
    #Button7.configure(highlightbackground="#d9d9d9")
    #Button7.configure(highlightcolor="black")
    #Button7.configure(pady="0")
    #Button7.configure(text='''EXTRACT DAMAGE BOUNDARY''')

    #Button8 = Button(Frame2)
    #Button8.place(relx=0.12, rely=0.55, height=45, width=137)
    #Button8.configure(activebackground="#1e1e1e")
    #Button8.configure(activeforeground="white")
    #Button8.configure(activeforeground="#ffffff")
    #Button8.configure(background="#232323")
    #Button8.configure(command=lambda:characters_with_damaged_edges())
    #Button8.configure(compound='left')
    #Button8.configure(disabledforeground="#a3a3a3")
    #Button8.configure(font="-family {Arial} -size 10 -weight bold ")
    #Button8.configure(wraplength=130)
    #Button8.configure(foreground="#ffffff")
    #Button8.configure(highlightbackground="#d9d9d9")
    #Button8.configure(highlightcolor="black")
    #Button8.configure(pady="0")
    #Button8.configure(text='''FIND DAMAGED EDGES''')

    #Button9 = Button(Frame2)
    #Button9.place(relx=0.12, rely=0.65, height=45, width=137)
    #Button9.configure(activebackground="#1e1e1e")
    #Button9.configure(activeforeground="white")
    #Button9.configure(activeforeground="#ffffff")
    #Button9.configure(background="#232323")
    #Button9.configure(command=lambda:thinning_the_result())
    #Button9.configure(compound='left')
    #Button9.configure(disabledforeground="#a3a3a3")
    #Button9.configure(font="-family {Arial} -size 10 -weight bold ")
    #Button9.configure(wraplength=130)
    #Button9.configure(foreground="#ffffff")
    #Button9.configure(highlightbackground="#d9d9d9")
    #Button9.configure(highlightcolor="black")
    #Button9.configure(pady="0")
    #Button9.configure(text='''FIND DAMAGED END-TIPS''')

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


    #Label5 = Label(Frame3)
    #Label5.place(relx=0.009, rely=0.029, height=150, width=757)
    #Label5.configure(background="#000000")
    #Label5.configure(compound='left')
    #Label5.configure(anchor='nw')
    #Label5.configure(justify='left')
    #Label5.configure(disabledforeground="#a3a3a3")
    #Label5.configure(font="-family {Century Schoolbook} -size 10")
    #Label5.configure(foreground="#00de00")
    #Label5.configure(text='''>>> THIS WILL SHOW THE RESULTS OF\n>>> OUR PROJECT''')

    #Label4 = Label(window)
    #Label4.place(relx=0.0, rely=0.029, height=51, width=1004)
    #Label4.configure(background="#d9d9d9")
    #Label4.configure(compound='left')
    #Label4.configure(padx=10,pady=4)
    #Label4.configure(anchor='center')
    #Label4.configure(disabledforeground="#a3a3a3")
    #Label4.configure(font="-family {Segoe UI} -size 28 -weight bold")
    #Label4.configure(foreground="#000000")
    #Label4.configure(text='''L4 Project - Pixels (MODULE 04)''')

