import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import os
import subprocess as sp
import math

class variables:
    check_arr = []
    df_arr = []
    answer_arr = []
    base = []
    bg = '#e6e6e6'
    fg = '#4d4d4d'
    vbg='#ffffff'

def base_chooser():  
    try:
        base_but["state"] = "disabled"    
        added_arr = []
        def add():
            value = column_box.get(column_box.curselection())
            column_box_dknow.insert(tk.END, value)
            column_box.delete(column_box.get(0, "end").index(value))
            added_arr.append(value)
            
        def sub():
            values = column_box_dknow.get(column_box_dknow.curselection())
            column_box.insert(tk.END, values)
            column_box_dknow.delete(column_box_dknow.get(0, "end").index(values))
            added_arr.remove(values)
            
        def submit():            
            for items in df['{}'.format(added_arr[0])]:
                try:
                    math.floor(int(items))
                except:
                    pass
                variables.base.append(items)
            for elements in added_arr[1:]:
                for no, things in enumerate(df['{}'.format(elements)]):
                    try:
                        things = math.floor(int(things))
                    except:
                        pass
                    try:
                        things = things.replace('nan', '')
                    except:
                        pass
                    variables.base[no] = str(variables.base[no])+ ' ' +str(things)
            
            root.destroy()

        path = os.getlogin()
        pt = 'C:/Users/' + path + '/Documents'
        window.filename = filedialog.askopenfilename(initialdir=pt, title="Select base file",
                                                     filetypes=(("excel file", "*.xlsx"), ("all files", "*.*")))

        df = pd.read_excel(window.filename)
        
        root = tk.Tk()
        Consolas = Font(root, family='Consolas', size=12)
        
        
        root.title('Choose columns')
        root.iconbitmap('files/Cookie.ico')
        root.geometry('470x300')
        root.resizable(0,0)
        root.configure(bg=variables.bg)

        column_box = tk.Listbox(root, bg=variables.vbg, fg=variables.fg, font=Consolas, height=15, bd=0)
        column_box.grid(row=0, column=0)

        column_box_dknow = tk.Listbox(root, bg=variables.vbg, fg=variables.fg, font=Consolas, height=15, bd=0)
        column_box_dknow.grid(row=0, column=4)

        spacex = tk.Label(root, text='          ', bg=variables.bg)
        spacex.grid(row=0, column=1)
        space2 = tk.Label(root, text='         ', bg=variables.bg)
        space2.grid(row=0, column=3)

        frame = tk.Frame(root)
        frame.grid(row=0, column=2)
        
        append = tk.Button(frame, bg=variables.bg, fg=variables.fg, font=Consolas, relief='flat', text='>>>', command=add)
        append.grid(row=0, column=0)
        depend = tk.Button(frame, bg=variables.bg, fg=variables.fg, font=Consolas, relief='flat', text='<<<', command=sub)
        depend.grid(row=1, column=0)
        ok_but = tk.Button(frame, bg=variables.bg, fg=variables.fg, font=Consolas, relief='flat', text='Ok', command=submit)
        ok_but.grid(row=3, column=0)
        
        for elements in df.columns:
            column_box.insert(tk.END, elements)

        root.mainloop()
        
    except:
        pass

def check_but():
    try:
        path = os.getlogin()
        pt = 'C:/Users/' + path + '/Downloads'
        window.filename = filedialog.askopenfilename(initialdir=pt, title="Select check file",
                                                     filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        for things in open(window.filename).readlines():
            things = things.replace(' ', '').lower()
            things = things.replace('locked', '')
            things = things.replace('\n', '')
            if len(things) <= 2:
                pass
            else:
                variables.check_arr.append(things)
        check_but["state"] = "disabled"
    except:
        pass

    
def check():
    
    for aw in variables.base:
        aw = aw.replace(' ', '')
        variables.df_arr.append(aw.lower())
    

    for no, elements in enumerate(variables.df_arr):
        if elements in variables.check_arr:
            pass
        else:
            variables.answer_arr.append(variables.base[no])
    wi = open('answer.txt', 'a')
    for elemen in variables.answer_arr:
        wi.write(elemen)
        wi.write('\n')
    wi.write('\n')
    wi.write('\n')
    wi.write('Number of students on roll: {}'.format(len(variables.base)))
    wi.write('\n')
    wi.write('Number of students present: {}'.format(len(variables.base)-len(variables.answer_arr)))        
    wi.write('\n')
    wi.write('Number of students absent: {}'.format(len(variables.answer_arr)))
    wi.close()
    programName = "notepad.exe"
    fileName = "answer.txt"
    sp.Popen([programName, fileName])
    try:
        os.remove('files/temp.csv')
    except:
        pass



try:
   os.remove('answer.txt')
except:
   pass

window = tk.Tk()
Consolas = Font(family='Consolas', size=12)
bse_img = ImageTk.PhotoImage(Image.open("files/base_select.PNG"))
chk_img = ImageTk.PhotoImage(Image.open('files/check_select.PNG'))
cmp_img = ImageTk.PhotoImage(Image.open('files/Compare.PNG'))

window.title('Biscuit')
window.geometry('300x400')
window.configure(bg=variables.bg)
window.resizable(0, 0)
window.iconbitmap('files/Cookie.ico')


base_chose_label = tk.Label(window, bg=variables.bg, fg=variables.fg, font=Consolas, text=
'''   How to use:
1.Hit the select base file
to choose your base excel file
  2.Hit the select check file
  to choose your file downloaded
  from bigbluebutton
3.Hit the Compare button

''')
base_chose_label.grid(row=0, column=0)

base_but = tk.Button(window, bg=variables.fg, fg=variables.fg, relief='flat', font=Consolas, image=bse_img,
                     command=base_chooser)
base_but.grid(row=1, column=0)

space = tk.Label(window, bg=variables.bg, text='''
''')
space.grid(row=2, column=4)

check_but = tk.Button(window, bg=variables.fg, fg=variables.fg, relief='flat', font=Consolas, image=chk_img,
                      command=check_but)
check_but.grid(row=3, column=0)

space = tk.Label(window, bg=variables.bg, text='''
''')
space.grid(row=4, column=4)

comp_but = tk.Button(window, bg=variables.fg, fg=variables.fg, relief='flat', font=Consolas, image=cmp_img,
                     command=check)
comp_but.grid(row=5, column=0)

window.mainloop()


def results():
    print('check_arr = ', variables.check_arr)
    print('\n')
    print('df_arr = ', variables.df_arr)
    print('\n')
    print('answer_arr = ', variables.answer_arr)
results()
