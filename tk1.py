import tkinter as tk
import os
from tkinter import messagebox, filedialog

root = tk.Tk()
root.geometry('200x400')
root.minsize(400,400)
root.maxsize(400,800)
root.title('File rename')

global substring
global file_list
global rename_count
global dir

substring = 'y2mate.com - '
file_list = []
rename_count = 0
dir = './'

# lists all files in the selected directory
def check_dir():
    eligible_files = 0
    global file_list
    file_list = os.listdir(dir)

    for file in file_list:
        if substring in file:
            eligible_files += 1

    export_list_as_txt()

    print(f'list of files in directory: {file_list}\n')
    lbl2.config(text = f'{eligible_files} file(s) eligible for renaming')

def export_list_as_txt():
    txt_name = './files_list.txt'
    count = 0

    while True:
        if os.path.exists(txt_name):
            print(f'{txt_name} already exists, changing name')
            txt_name = f'./files_list_{count}.txt'
            count += 1
        else:
            break

    f = open(txt_name, 'a', encoding='utf-8')

    if not file_list:
        print('No files')
        return
    
    for item in file_list:
        f.write(item + '\n')

# renames files in directory
def rename_files():
    label_msg = ""
    rename_count = 0

    for file_name in file_list:
        if substring in file_name:
            new_name = os.path.join(dir, file_name[13:])
            old_name = os.path.join(dir, file_name)

            if not os.path.exists(new_name):
                os.rename(old_name, new_name)
            else:
                print(f"File '{new_name}' already exists. Skipping renaming.")
                continue

            print(f'Renamed {old_name} to {new_name}')
            label_msg += f'Renamed {old_name} to {new_name} \n'
            rename_count += 1

    print(f'Renamed {rename_count} file(s)')
    messagebox.showinfo("Done", f"Renamed {rename_count} files")
    lbl2.config(text = label_msg)

# changes directory where renaming happens
def change_directory():
    global dir
    new_dir = filedialog.askdirectory(initialdir= '/',
                                      title='Select directory')
    
    if new_dir:
        dir = new_dir
        lbl1.config(text=f'Current directory: {dir}')


###
### Widgets 
###
lbl1 = tk.Label(root, 
                text=f'Current directory: {dir}')
lbl1.pack()

dirSelectBtn = tk.Button(root,
                         text = 'Change directory',
                         command = change_directory)
dirSelectBtn.pack()

checkBtn = tk.Button(root, 
                     text = 'Check directory', 
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