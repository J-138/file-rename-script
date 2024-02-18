import tkinter as tk
import os
from tkinter import messagebox, filedialog

root = tk.Tk()
root.geometry('200x400')
root.minsize(400,400)
root.maxsize(400,800)
root.title('Y2Mate rename')

# lists all files in the selected directory
def check_dir():
    global file_list
    global dir
    file_list = os.listdir(dir)
    print(f'list of files in directory: {file_list}\n')
    lbl2.config(text = str(file_list))

def rename_files():
    label_msg = ""
    global file_list
    global substring
    global rename_count
    global dir

    for file_name in file_list:
        if substring in file_name:
            new_name = os.path.join(dir, file_name[13:])
            old_name = os.path.join(dir, file_name)
            os.rename(old_name, new_name)
            print(f'Renamed {old_name} to {new_name}')
            label_msg += f'Renamed {old_name} to {new_name} \n'
            rename_count += 1

    print(f'Renamed {rename_count} file(s)')
    messagebox.showinfo("Done", f"Renamed {rename_count} files")
    lbl2.config(text = label_msg)

def change_directory():
    global dir
    new_dir = filedialog.askdirectory(initialdir= '/',
                                      title='Select directory')
    
    if new_dir:
        dir = new_dir
        lbl1.config(text=f'Current directory: {dir}')


## Variables ##
file_list = []
substring = 'y2mate.com - '
rename_count = 0
dir = './'


## Widgets ##
lbl1 = tk.Label(root, 
                text=f'Current directory: {dir}')
lbl1.pack()

dirSelectBtn = tk.Button(root,
                         text = 'Change directory',
                         command = change_directory)
dirSelectBtn.pack()

checkBtn = tk.Button(root, 
                     text = 'Check folder', 
                     command = check_dir)
checkBtn.pack()

btn1 = tk.Button(root, 
                 text = 'Rename file(s)', 
                 activeforeground = "yellow",
                 command = rename_files)
btn1.pack()

lbl2 = tk.Label(root,
                text = '',
                wraplength=400)
lbl2.pack()


root.mainloop()