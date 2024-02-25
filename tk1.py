import tkinter as tk
import os
from tkinter import INSERT, BooleanVar, PhotoImage, StringVar, messagebox, filedialog

root = tk.Tk()
root.geometry('200x400')
root.minsize(400,400)
root.maxsize(400,1080)
root.title('File rename')

try:
    app_icon = tk.PhotoImage(file='./app_icon.png')
    root.iconphoto(True, app_icon)
except tk.TclError:
    print("Image file not found or invalid")

global file_list
global dir
file_list = []
dir = './'

# lists all files in the selected directory
def check_dir():
    eligible_files = 0
    global file_list
    file_list = os.listdir(dir)

    if ignore_cap.get():
        for file in file_list:
            if str_to_replace.get().upper() in file.upper():
                eligible_files += 1

    else:
        for file in file_list:
            if str_to_replace.get() in file:
                eligible_files += 1

    btn1.config(state='normal')

    print(f'list of files in directory: {file_list}')
    bottomText.delete(1.0, tk.END)
    bottomText.insert(1.0, f'{eligible_files} file(s) eligible for renaming')

def export_list_as_txt():
    file_list = os.listdir(dir)
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

    open_txt_name = os.path.join(os.getcwd(), txt_name)
    os.startfile(open_txt_name)

# renames file in dir, if the name exists, either delete it or skip renaming
def rename(new_name, old_name, d_new_name, d_old_name):
    renamed = True
    msg= ''

    if not os.path.exists(new_name):
        os.rename(old_name, new_name)

    elif os.path.exists(new_name) and delete_dups.get():
        os.remove(new_name)
        os.rename(old_name, new_name)

    else:
        dup_msg = f"File '{new_name}' already exists. Skipping file."
        print(dup_msg)
        msg = dup_msg
        renamed = False

    if renamed:
        msg = f'Renamed: {d_old_name} -> {d_new_name}\n'

    print(msg)
    return msg, renamed

def rename_files():
    label_msg = ''
    rename_count = 0

    # renames based on user options, could be made more elegant i think
    for file_name in file_list:
        if ignore_cap.get():
            r_str_upper = str_to_replace.get().upper()
            file_name_upper = file_name.upper()

            if r_str_upper in file_name_upper:
                index_l = file_name_upper.index(r_str_upper)
                index_r = index_l + len(r_str_upper)
                new_file_name = file_name[0:index_l] + replacement_str.get() + file_name[index_r:]
                new_name = os.path.join(dir, new_file_name)
                old_name = os.path.join(dir, file_name)
                msg, renamed = rename(
                    new_name=new_name, 
                    old_name=old_name,
                    d_new_name=new_file_name,
                    d_old_name=file_name
                )
                label_msg += msg
                if renamed: rename_count += 1

        elif str_to_replace.get() in file_name and not ignore_cap.get():
            new_name = os.path.join(dir, file_name.replace(str_to_replace.get(), replacement_str.get()))
            old_name = os.path.join(dir, file_name)
            new_file_name = file_name.replace(str_to_replace.get(), '')
            msg, renamed = rename(
                new_name=new_name, 
                old_name=old_name,
                d_new_name=new_file_name,
                d_old_name=file_name
            )
            label_msg += msg
            if renamed: rename_count += 1
    
        else:
            print('error in rename_files')

    # disables renaming button after renaming is done
    btn1.config(state='disabled')

    print(msg)
    msg = f'Renamed {rename_count} file(s)'
    bottomText.delete(1.0, tk.END)
    bottomText.insert(1.0, label_msg)
    messagebox.showinfo('Done', msg)

def change_directory():
    global dir
    new_dir = filedialog.askdirectory(initialdir= './',
                                      title='Select directory')

    if new_dir:
        dir = new_dir
        lbl1.config(text=f'Current directory: {dir}')

def update_replace_lbl(var, index, mode):
    print(str_to_replace.get())
    replaceInfoLbl.config(text=f'Replacing files that contain: \'{str_to_replace.get()}\' with \'{replacement_str.get()}\'')
    
#/ / / / / / / / / /
#      WIDGETS
#/ / / / / / / / / /
gen_width = 300

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

replacement_str = StringVar()
replacement_str.set('')
replacementStrEntry = tk.Entry(root,
                               textvariable=replacement_str,
                               width=gen_width,
                               justify='center')

replaceInfoLbl = tk.Label(root,
                          text=f'Replacing files that contain: \'{str_to_replace.get()}\' with \'{replacement_str.get()}\'')

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
                 command = rename_files,
                 state='disabled')

lbl2 = tk.Label(root,
                text = '',
                wraplength=gen_width)

# optional settings
ignore_cap = BooleanVar()
delete_dups = BooleanVar()

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

# scrollable text
fill_str = StringVar()
fill_str = ''.join(['text text text text text text ' for i in range(1, 50)])

bottomText = tk.Text(root, 
                     wrap='char', 
                     height=10, 
                     width=gen_width)

bottomText.insert(INSERT, fill_str)

textScroll = tk.Scrollbar(root, 
                          command=bottomText.yview)   

bottomText.config(yscrollcommand=textScroll.set)

# packing order
lbl1.pack(padx=5)
entry1.pack(padx=5)
replacementStrEntry.pack(padx=5, pady=2)
replaceInfoLbl.pack(padx=5)
ignoreCapsCheck.pack(padx=5)
deleteDupsCheck.pack(padx=5)    
dirSelectBtn.pack(pady=5)
checkBtn.pack(pady=5)
downloadBtn.pack(pady=5)
btn1.pack(pady=5)
bottomText.pack(padx=5, pady=5, side='left', fill='both')
textScroll.pack(side='left') 

# tracks the entry widget variables to update label
str_to_replace.trace_add("write", update_replace_lbl)
replacement_str.trace_add("write", update_replace_lbl)

if __name__ == '__main__':
    root.mainloop()
