import tkinter as tk
import os
from tkinter import BooleanVar, PhotoImage, StringVar, messagebox, filedialog

root = tk.Tk()
root.geometry('200x400')
root.minsize(400,400)
root.maxsize(400,800)
root.title('File rename')

global file_list
global dir

file_list = []
dir = './'

# lists all files in the selected directory
def check_dir():
    eligible_files = 0
    global file_list
    file_list = os.listdir(dir)

    for file in file_list:
        if str_to_replace.get() in file:
            eligible_files += 1

    print(f'list of files in directory: {file_list}\n')
    lbl2.config(text = f'{eligible_files} file(s) eligible for renaming')

def export_list_as_txt():
    txt_name = './files_list.txt'
    count = 0

    if not file_list:
        print('No files')
        messagebox.showinfo('No files', 'No files in directory')
        return
    
    while True:
        if os.path.exists(txt_name):
            print(f'{txt_name} already exists, changing name')
            txt_name = f'./files_list_{count}.txt'
            count += 1
        else:
            break

    f = open(txt_name, 'a', encoding='utf-8')

    for item in file_list:
        f.write(item + '\n')

def rename_files():
    label_msg = ""
    rename_count = 0

    for file_name in file_list:
        if str_to_replace.get() in file_name:
            new_name = os.path.join(dir, file_name.replace(str_to_replace.get(), ''))
            old_name = os.path.join(dir, file_name)

            if not os.path.exists(new_name):
                os.rename(old_name, new_name)
            elif os.path.exists(new_name) and delete_dups.get():
                os.remove(new_name)
                os.rename(old_name, new_name)
            else:
                print(f"File '{new_name}' already exists. Skipping file.")
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
    new_dir = filedialog.askdirectory(initialdir= './',
                                      title='Select directory')

    if new_dir:
        dir = new_dir
        lbl1.config(text=f'Current directory: {dir}')

def update_replace_lbl(var, index, mode):
    print(str_to_replace.get())
    replaceInfoLbl.config(text=f'Replacing files that contain: \'{str_to_replace.get()}\'')
    
###
### Widgets
###
gen_width = 300

window_width = root.winfo_width()
print('window width ' + str(window_width))

lbl1 = tk.Label(root,
                text=f'Current directory: {dir}',
                pady=10,
                wraplength=gen_width,
                justify='left')

str_to_replace = StringVar()
str_to_replace.set('y2mate.com - ')
entry1 = tk.Entry(root,
                  textvariable=str_to_replace,
                  width=gen_width,
                  justify='center')

dirSelectBtn = tk.Button(root,
                         text = 'Change directory',
                         command = change_directory)

checkBtn = tk.Button(root,
                     text = 'Check directory',
                     command = check_dir)

downloadBtn = tk.Button(root,
                        text='Download txt of files in directory',
                        command=export_list_as_txt)

btn1 = tk.Button(root,
                 text = 'Rename file(s)',
                 activeforeground = "yellow",
                 command = rename_files)

lbl2 = tk.Label(root,
                text = '',
                wraplength=gen_width)

replaceInfoLbl = tk.Label(root,
                          text=f'Replacing files that contain: \'{str_to_replace.get()}\'')

# optional settings
ignore_cap = BooleanVar()
delete_dups = BooleanVar()
ignore_img = PhotoImage(file='./caps-lock.png')

ignoreCapsCheck = tk.Checkbutton(root,
                                text='Ignore capitalization',
                                command='',
                                variable=ignore_cap,
                                onvalue=True,
                                offvalue=False)

deleteDupsCheck = tk.Checkbutton(root,
                                 text='Delete duplicates when renamed',
                                 variable=delete_dups,
                                 onvalue=True,
                                 offvalue=False)

# packing order
lbl1.pack(padx=5)
entry1.pack(padx=5)
replaceInfoLbl.pack(padx=5)
ignoreCapsCheck.pack(padx=5)
deleteDupsCheck.pack(padx=5)
dirSelectBtn.pack(pady=5)
checkBtn.pack(pady=5)
downloadBtn.pack(pady=5)
btn1.pack(pady=5)
lbl2.pack(padx=5)

str_to_replace.trace_add("write", update_replace_lbl)


root.mainloop()