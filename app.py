import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

text_contents = dict()


def create_file(content='', title='Untitled'):
    container = ttk.Frame(notebook)
    container.pack()

    textarea = tk.Text(container)
    textarea.insert('end', content)
    textarea.pack(side='left', fill='both', expand=True)

    notebook.add(container, text=title)
    notebook.select(container)

    text_contents[str(textarea)] = hash('')

    text_scroll = ttk.Scrollbar(container, orient='vertical', command=textarea.yview)
    text_scroll.pack(side='right', fill='y')
    textarea['yscrollcommand'] = text_scroll.set


def check_changes():
    current = get_text_widget()
    content = current.get('1.0', 'end-1c')
    name = notebook.tab('current')['text']

    if hash(content) != text_contents[str(current)]:
        if name[-1] != '*':
            notebook.tab('current', text=name + '*')
    elif name[-1] == '*':
        notebook.tab('current', text=name[:-1])


def get_text_widget():
    tab_widget = root.nametowidget(notebook.select())
    text_widget = tab_widget.winfo_children()[0]
    return text_widget


def current_tab_unsaved():
    text_widget = get_text_widget()
    content = text_widget.get('1.0', 'end-1c')
    return hash(content) != text_contents[str(text_widget)]


def confirm_close():
    return messagebox.askyesno(
        message='Do you really want to close?',
        icon='question',
        title='Unsaved changes'
    )


def close_current_tab():
    current = notebook.nametowidget(notebook.select())

    if current_tab_unsaved() and not confirm_close():
        return

    if len(notebook.tabs()) == 1:
        create_file()

    notebook.forget(current)


def confirm_exit():
    unsaved = False

    for tab in notebook.tabs():
        tab_widget = root.nametowidget(tab)
        text_widget = tab_widget.winfo_children()[0]
        content = text_widget.get('1.0', 'end-1c')

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break

    if unsaved and not confirm_close():
        return

    root.destroy()


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename = os.path.basename(file_path)
        text_widget = get_text_widget()
        content = text_widget.get('1.0', 'end-1c')

        with open(file_path, 'w') as file:
            file.write(content)
    except (AttributeError, FileNotFoundError):
        print('Save operation cancelled')
        return

    notebook.tab('current', text=filename)

    text_contents[str(text_widget)] = hash(content)


def open_file():
    file_path = filedialog.askopenfilename()

    try:
        file_name = os.path.basename(file_path)

        with open(file_path, 'r') as file:
            content = file.read()

    except (AttributeError, FileNotFoundError):
        print('File open operation cancelled')
        return

    create_file(content, file_name)


def show_about_info():
    return messagebox.showinfo(
        title='About',
        message='Just a little simple text editor made with Tkinter and ttk'
    )


root = tk.Tk()
root.title('Simple note editor')
root.option_add('*tearOff', False)

main = ttk.Frame(root)
main.pack(fill='both', expand=True, padx=1, pady=(4, 0))

menubar = tk.Menu()
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)

menubar.add_cascade(menu=file_menu, label='File')
menubar.add_cascade(menu=help_menu, label='Help')

file_menu.add_command(label='Add new', command=create_file, accelerator='Ctrl+N')
file_menu.add_command(label='Open...', command=open_file, accelerator='Ctrl+O')
file_menu.add_command(label='Save', command=save_file, accelerator='Ctrl+S')
file_menu.add_command(label='Close Tab', command=close_current_tab, accelerator='Ctrl+Q')
file_menu.add_command(label='Exit', command=confirm_exit)

help_menu.add_command(label='About', command=show_about_info)

notebook = ttk.Notebook(main)
notebook.pack(fill='both', expand=True)
create_file()

root.bind('<KeyPress>', lambda e: check_changes())
root.bind('<Control-n>', lambda e: create_file())
root.bind('<Control-o>', lambda e: open_file())
root.bind('<Control-s>', lambda e: save_file())
root.bind('<Control-q>', lambda e: close_current_tab())

root.mainloop()
