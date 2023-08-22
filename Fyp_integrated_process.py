from tkinter import *
import tkinter.ttk as ttk
from tkinter.constants import *
import PIL.Image, PIL.ImageTk
from tkinter import filedialog
import sys
from tkinter import scrolledtext


import Module1_opencv as cdr

#Global Variables
file_list = []
upload_imgs = []
result_imgs = []
denoized_files = []
clahe_files = []
binarized_list = []
binarized_list_bgr = []
rotated_list = []
rotated_list_bgr = []
preprinted_remove = []
preprinted_remove_bgr = []
line_segmented_list = []
segmented_words = []
noised_removed_word_seg = []
segmented_chars = []
hfg = []
closed = None
logs = []
log_text = ""
index = -1
seg_index = -1
sub_module_index = 0
rgb_converted_files = []
is_result_got = False

def tab5(main_canvas,Label4):
    
    for widget in main_canvas.winfo_children():
            widget.destroy()
    Label4.configure(text='''L4 Project - Pixels (Module 01)''')
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

    def upload_file():
        global file_list,upload_imgs,index,result_imgs,is_result_got,logs,seg_index
        global Label5,sub_module_index
        
        for widget in Canvas1.winfo_children():
            widget.destroy()
        for widget in Canvas2.winfo_children():
            widget.destroy()
        file_list.clear()
        logs.clear()
        upload_imgs.clear()
        result_imgs.clear()
        denoized_files.clear()
        binarized_list_bgr.clear()
        binarized_list.clear()
        rotated_list.clear()
        rotated_list_bgr.clear()
        preprinted_remove.clear()
        preprinted_remove_bgr.clear()
        rgb_converted_files.clear()
        line_segmented_list.clear()
        segmented_words.clear()
        segmented_chars.clear()
        noised_removed_word_seg.clear()
        j = 0
        hfg.clear()
        closed = None
        #print("before ",clustered_files)
        clahe_files.clear()
        #print("After ",clustered_files)
        is_result_got = False
        f_types = [('PNG Files','*.png'),('Jpg Files', '*.jpg')] 
        filename = filedialog.askopenfilename(multiple=True,filetypes=f_types)
        col=1
        row=3
        for f in filename:
            file_list.append(f)
            img=PIL.Image.open(f)
            img = image_resize(img)
            img=PIL.ImageTk.PhotoImage(img)
            upload_imgs.append(img)

        index = -1
        seg_index = -1
        sub_module_index = 0
        image_swap_plus()
        log = ">>> Image Files are Loaded into Application...\n"
        data_log(log)
        #return filename

    def full_process_of_module2():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,clahe_files,binarized_list,binarized_list_bgr,rotated_list,rotated_list_bgr,preprinted_remove,preprinted_remove_bgr,logs
        global sub_module_index,line_segmented_list,j,hfg,closed,segmented_words,noised_removed_word_seg,segmented_chars
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        if not denoized_files:
            denoized_files = cdr.denoisingImage(file_list)
        if not clahe_files:
            clahe_files = cdr.contrastEqualized(denoized_files)
        if not binarized_list and not binarized_list_bgr:
            binarized_list,binarized_list_bgr = cdr.binarizedImage(clahe_files)
        if not rotated_list and not rotated_list_bgr:
            rotated_list,rotated_list_bgr = cdr.correct_skew(binarized_list)
        if not preprinted_remove and not preprinted_remove_bgr:
            preprinted_remove,preprinted_remove_bgr = cdr.removingPreprintedLines(binarized_list)
        if not line_segmented_list:
            line_segmented_list,j,hfg,closed = cdr.lineSegmentation(preprinted_remove[0],file_list[0])
        if not segmented_words:
            segmented_words,noised_removed_word_seg = cdr.wordSegmentation(file_list[0],closed,denoized_files[0],hfg,j)
        if not segmented_chars:
            segmented_chars = cdr.characterSegmentation()
        print(segmented_chars)
        rgb_converted_files = cdr.display_out(segmented_chars)
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
        sub_module_index = 1
        Label3.configure(text="Final Results")
        image_swap_plus()
        log = ">>> Finished the full process of MODULE 01...\n"
        data_log(log)

    def start_denoising_process():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,logs
        global sub_module_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        #denoized_files.clear()
        result_imgs.clear()
        print(file_list)
        if not denoized_files:
            denoized_files = cdr.denoisingImage(file_list)
        rgb_converted_files = cdr.display_out(denoized_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        sub_module_index = 0
        Label3.configure(text="Denoised Image")
        image_swap_plus()
        log = ">>> Denoised all image segments...\n"
        data_log(log)

    def start_contrast_equalized_process():
        global rgb_converted_files,result_imgs,is_result_got,index,denoized_files,clahe_files,logs
        global sub_module_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #clahe_files.clear()
        if not clahe_files:
            clahe_files = cdr.contrastEqualized(denoized_files)
        print(clahe_files)
        rgb_converted_files = cdr.display_out(clahe_files)
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
        sub_module_index = 0
        Label3.configure(text="Contrast Equalized Image")
        image_swap_plus()
        log = ">>> Clustered all image segments...\n"
        data_log(log)

    def start_binarizing():
        global rgb_converted_files,result_imgs,is_result_got,index,clahe_files,binarized_list,binarized_list_bgr,logs
        global sub_module_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        #binarized_list.clear()
        if not binarized_list and not binarized_list_bgr:
            binarized_list,binarized_list_bgr = cdr.binarizedImage(clahe_files)
        print(binarized_list)
        rgb_converted_files = cdr.display_out(binarized_list_bgr)
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
        sub_module_index = 0
        Label3.configure(text="Binarized Image")
        image_swap_plus()
        log = ">>> Found all dmaged boundaries of images...\n"
        data_log(log)

    def skew_correction():
        global rgb_converted_files,result_imgs,is_result_got,index,binarized_list,rotated_list,rotated_list_bgr,logs
        global sub_module_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        if not rotated_list and not rotated_list_bgr:
            rotated_list,rotated_list_bgr = cdr.correct_skew(binarized_list)
        print(rotated_list)
        print(rotated_list_bgr)
        rgb_converted_files = cdr.display_out(rotated_list_bgr)
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
        sub_module_index = 0
        Label3.configure(text="Skew Corrected Image")
        image_swap_plus()
        log = ">>> Identified the damaged edges...\n"
        data_log(log)

    def removing_preprinted_lines():
        global rgb_converted_files,result_imgs,index,binarized_list,preprinted_remove, preprinted_remove_bgr, logs,seg_index
        global sub_module_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        if not preprinted_remove and not preprinted_remove_bgr:
            preprinted_remove,preprinted_remove_bgr = cdr.removingPreprintedLines(binarized_list)
        print(preprinted_remove)
        rgb_converted_files = cdr.display_out(preprinted_remove_bgr)
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
        sub_module_index = 0
        Label3.configure(text="Preprinted Removed Image")
        image_swap_plus()
        log = ">>> Thinned the characters and identified real endtips...\n"
        data_log(log)

    def line_segmentation():
        global rgb_converted_files,result_imgs,index,file_list,line_segmented_list, preprinted_remove, logs
        global j,hfg,closed,sub_module_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        if not line_segmented_list:
            line_segmented_list,j,hfg,closed = cdr.lineSegmentation(preprinted_remove[0],file_list[0])
        #print("line segmented list ",line_segmented_list)
        rgb_converted_files = cdr.display_out(line_segmented_list)
        #print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        seg_index = -1
        sub_module_index = 1
        Label3.configure(text="Line Segmented Images")
        image_swap_plus()
        log = ">>> Thinned the characters and identified real endtips...\n"
        data_log(log)

    def word_segmentation():
        global rgb_converted_files,result_imgs,index,binarized_list,file_list,line_segmented_list, preprinted_remove, logs
        global j,hfg,closed,sub_module_index,segmented_words,denoized_files,noised_removed_word_seg,seg_index
        
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        if not segmented_words:
            segmented_words,noised_removed_word_seg = cdr.wordSegmentation(file_list[0],closed,denoized_files[0],hfg,j)
        print("word segmented list ",len(segmented_words))
        print("word n r segmented list ",len(noised_removed_word_seg))
        rgb_converted_files = cdr.display_out(segmented_words)
        #print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        seg_index = -1
        sub_module_index = 1
        Label3.configure(text="Word Segmented Images")
        image_swap_plus()
        log = ">>> Thinned the characters and identified real endtips...\n"
        data_log(log)

    def character_segmentation():
        global rgb_converted_files,result_imgs,index,binarized_list,file_list,line_segmented_list, preprinted_remove, logs
        global j,hfg,closed,sub_module_index,segmented_words,denoized_files,noised_removed_word_seg,segmented_chars
        global seg_index
        for widget in Canvas2.winfo_children():
            widget.destroy()
        rgb_converted_files.clear()
        result_imgs.clear()
        if not segmented_chars:
            segmented_chars = cdr.characterSegmentation()
        print("Chars segmented list ",segmented_chars)
        rgb_converted_files = cdr.display_out(segmented_chars)
        #print("rgb converted ",rgb_converted_files)
        col=1 
        row=1 
        for rgb_file in rgb_converted_files:
            im = PIL.Image.fromarray(rgb_file)
            im = image_resize(im)
            img = PIL.ImageTk.PhotoImage(image=im)
            result_imgs.append(img)
        is_result_got = True
        index = -1
        seg_index = -1
        sub_module_index = 1
        Label3.configure(text="Segmented Characters")
        image_swap_plus()
        log = ">>> Thinned the characters and identified real endtips...\n"
        data_log(log)

    def image_swap_plus():
        global index,upload_imgs,result_imgs,is_result_got,logs,seg_index,sub_module_index
        if sub_module_index == 1:
            if seg_index == len(result_imgs)-1:
                seg_index = -1
            seg_index = seg_index + 1
            for widget in Canvas1.winfo_children():
                widget.destroy()
            Label1= Label(Canvas1, image=upload_imgs[0])
            Label1.place(x=200,y=200,anchor="center")

            if is_result_got:
                for widget in Canvas2.winfo_children():
                    widget.destroy()
                Label2= Label(Canvas2, image=result_imgs[seg_index])
                #data_log(logs[index])
                Label2.place(x=200,y=200,anchor="center")
        else:        
            if index == len(upload_imgs)-1:
                index = -1
            index = index+1
            for widget in Canvas1.winfo_children():
                widget.destroy()
            Label1= Label(Canvas1, image=upload_imgs[index])
            Label1.place(x=200,y=200,anchor="center")

            if is_result_got:
            
                for widget in Canvas2.winfo_children():
                    widget.destroy()
                Label2= Label(Canvas2, image=result_imgs[index])
                #data_log(logs[index])
                Label2.place(x=200,y=200,anchor="center")
            
    def image_swap_minus():
        global index,result_imgs,upload_imgs,is_result_got,logs,seg_index,sub_module_index
        if sub_module_index == 1:
            if seg_index <= 0:
                seg_index = len(result_imgs)-1
            seg_index = seg_index-1
            for widget in Canvas1.winfo_children():
                widget.destroy()
            Label1= Label(Canvas1, image=upload_imgs[0])
            Label1.place(x=200,y=200,anchor="center")

            if is_result_got:
                for widget in Canvas2.winfo_children():
                    widget.destroy()
                Label2= Label(Canvas2, image=result_imgs[seg_index])
                #data_log(logs[index])
                Label2.place(x=200,y=200,anchor="center")
        else:    
            if index <= 0:
                index = len(upload_imgs)-1
            index = index-1
            for widget in Canvas1.winfo_children():
                widget.destroy()
        
            Label1= Label(Canvas1, image=upload_imgs[index])
        
            #Label1.image=upload_imgs[0]
            Label1.place(x=150,y=150,anchor="center")
        
            if is_result_got:
            
                for widget in Canvas2.winfo_children():
                    widget.destroy()
                Label2= Label(Canvas2, image=result_imgs[index])
                #data_log(logs[index])
                Label2.place(x=150,y=150,anchor="center")


            
            
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
    Button1.configure(command=lambda:upload_file())
    Button1.configure(compound='left')
    Button1.configure(disabledforeground="#a3a3a3")
    Button1.configure(font="-family {Segoe UI} -size 11 -weight bold")
    Button1.configure(foreground="#ffffff")
    Button1.configure(highlightbackground="#d9d9d9")
    Button1.configure(highlightcolor="black")
    Button1.configure(pady="0")
    Button1.configure(text='''UPLOAD''')

    Button2 = Button(Frame2)
    Button2.place(relx=0.07, rely=0.12, height=34, width=155)
    Button2.configure(activebackground="#4a1e00")
    Button2.configure(activeforeground="white")
    Button2.configure(activeforeground="#ffffff")
    Button2.configure(background="#783000")
    Button2.configure(command=lambda:full_process_of_module2())
    Button2.configure(compound='left')
    Button2.configure(disabledforeground="#a3a3a3")
    Button2.configure(font="-family {Segoe UI} -size 10 -weight bold")
    Button2.configure(foreground="#ffffff")
    Button2.configure(highlightbackground="#d9d9d9")
    Button2.configure(highlightcolor="black")
    Button2.configure(pady="0")
    Button2.configure(text="FULL PROCESS")


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
    #Label5.grid(row=0,column=1)
    #Label5.configure(background="#000000")
    #Label5.configure(compound='left')
    #Label5.configure(anchor='nw')
    #Label5.configure(justify='left')
    #Label5.configure(disabledforeground="#a3a3a3")
    #Label5.configure(font="-family {Century Schoolbook} -size 10")
    #Label5.configure(foreground="#00de00")
    #Label5.configure(text='''>>> THIS WILL SHOW THE RESULTS OF\n>>> OUR PROJECT''')


    #Label4 = Label(window)
    #Label4.place(relx=0.0, rely=0.029, height=51, relwidth=1)
    #Label4.configure(background="#d9d9d9")
    #Label4.configure(compound='left')
    #Label4.configure(padx=10,pady=4)
    #Label4.configure(anchor='center')
    #Label4.configure(disabledforeground="#a3a3a3")
    #Label4.configure(font="-family {Segoe UI} -size 28 -weight bold")
    #Label4.configure(foreground="#000000")
    #Label4.configure(text='''L4 Project - Pixels (Module 01)''')


