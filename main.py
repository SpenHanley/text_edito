# -*- coding: utf-8 -*-

import datetime
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

__author__ = 'Spen Hanley'

# TODO: Make the root title update when it is changed
# TODO: Implement the actions for the context menu aswell as the remaining menu items
# TODO: Implement either a library or a custom print dialog as no print dialog is included
# TODO: Trigger undo command from menu item for both edit and context menu


class ShowGUI:
    def __init__(self):
        self.root = self.config_root()
        self.frame = self.config_frame(self.root)
        self.dir = tk.END
        self.text_area = self.text_widget(self.frame)
        self.bind_all()
        self.file = None
        self.file_opts = options = {}
        self.cont_menu = self.context_menu(self.root)
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('All Files', '*.*'), ('Text Files', '*.txt')]
        self.root.mainloop()

    def config_root(self):
        rt = tk.Tk()
        rt.wm_iconbitmap('image/notepad_icon.ico')
        rt.title = "PyNotepad"
        rt.config(menu=self.make_menu_bar(rt))
        rt.update()
        rt.minsize(rt.winfo_width(), rt.winfo_height())
        tk.Grid.rowconfigure(rt, 0, weight=1)
        tk.Grid.columnconfigure(rt, 0, weight=1)
        return rt

    def trigger_find(self, what, dir):
        pos = '1.0'
        idx = self.text_area.search(what, tk.INSERT, stopindex=dir)
        if not idx:
            self.show_error(what=what) # Break
        else:
            pos = '{}+{}c'.format(idx, len(what))
            self.text_area.tag_config('passed', background='blue')
            self.text_area.tag_add('passed', 'sel.first', 'sel.last')

    @staticmethod
    def show_error(what):
        messagebox.showerror('PyNotepad', 'Cannot find "{}"'.format(what))

    @staticmethod
    def config_frame(root):
        fr = tk.Frame(root)
        fr.grid(row=0, column=0, sticky='nsew')
        tk.Grid.columnconfigure(fr, 0, weight=1)
        tk.Grid.rowconfigure(fr, 0, weight=1)
        return fr

    def bind_all(self):
        self.text_area.bind("<Button-3>", self.popup)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-S>", self.save_as_file)
        self.root.bind("<Control-n>", self.reset)
        self.root.bind("<F5>", self.insert_date)
        self.root.bind("<Control-f>", self.show_find)

    def popup(self, event):
        self.cont_menu.post(event.x_root, event.y_root)

    # Commands

    def save_as_file(self, event):
        if self.file is None:
            self.file = filedialog.asksaveasfilename(**self.file_opts)
            file = open(self.file, 'w+')
            file.write(self.text_area.get(0.0, tk.END))
            print(self.file)
        else:
            self.save_file(None)

    def save_file(self, event):
        if self.file:
            file = open(self.file, 'w+')
            file.write(self.text_area.get(0.0, tk.END))

    def open_file(self, event):
        self.file = filedialog.askopenfilename(**self.file_opts)
        i = 1.0
        if self.file:
            with open(self.file, 'r') as f:
                self.text_area.insert(1.0, f.read())
                self.set_title(self.file)

    def reset(self, event):
        self.text_area.delete('1.0', tk.END)
        self.file = None
        self.set_title('Untitled - PyNotepad')

    def quit(self):
        sys.exit(0)  # Exit out

    # %c and %x do not give the correct time and date formats
    def insert_date(self, event):
        date_obj = datetime.datetime.now()
        date = date_obj.strftime("%d/%m/%Y")
        time = date_obj.strftime("%H:%M")
        self.text_area.insert(self.text_area.index(tk.INSERT), time + ' ' + date)

    def text_widget(self, frame):
        y_scroll = tk.Scrollbar(frame)
        y_scroll.grid(row=0, column=1, sticky="nsew")
        x_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        x_scroll.grid(row=1, column=0, sticky="nsew")
        t = tk.Text(self.frame, wrap="none", yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set, undo=True)
        t.grid(row=0, column=0, sticky='nsew')
        y_scroll.config(command=t.yview)
        x_scroll.config(command=t.xview)
        return t

    def show_find(self, event):
        fdialog = self.find_dialog()

    def find_dialog(self):
        xpad = 3
        ypad = 3
        dir = ""
        v = tk.StringVar()
        top = tk.Tk()
        top.wm_iconbitmap('image/hidden_icon.ico')
        top.resizable(False, False)
        top.wm_title('Find')
        find_what = tk.Label(top, text='Find what: ')
        find_what.grid(row=0, column=0, padx=xpad, pady=ypad, sticky=tk.W)
        to_find = tk.Entry(top)
        to_find.grid(row=0, column=1, columnspan=2, padx=xpad, pady=ypad)
        trigger_find = tk.Button(top, text='Find Next', command=lambda: self.trigger_find(to_find.get(), self.dir))
        trigger_find.grid(row=0, column=3, padx=xpad, pady=ypad)
        trigger_find.config(width=8)
        cancel = tk.Button(top, text='Cancel', command=lambda: top.destroy())
        cancel.grid(row=2, column=3, padx=xpad, pady=ypad)
        cancel.config(width=8)
        match = tk.Checkbutton(top, text='Match case')
        match.grid(row=3, column=0, padx=xpad, pady=ypad)
        direction_container = tk.LabelFrame(top, text='Direction')
        direction_container.grid(row=2, column=2, rowspan=2, padx=xpad, pady=ypad)
        dir_up = tk.Radiobutton(direction_container, text='Up', value=0, command=lambda: self.change_dir('up'))
        dir_up.grid(row=0, column=0)
        dir_down = tk.Radiobutton(direction_container, text='Down', value=1, command=lambda: self.change_dir('down'))
        dir_down.grid(row=0, column=1)
        return top

    def change_dir(self, dir):
        if dir == 'up':
            self.dir = '0.0'
        else:
            self.dir = tk.END

    # Create the menus
    def make_menu_bar(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_cascade(label="File", menu=self.file_menu(root))
        m.add_cascade(label="Edit", menu=self.edit_menu(root))
        m.add_cascade(label="Format", menu=self.format_menu(root))
        m.add_cascade(label="View", menu=self.view_menu(root))
        m.add_cascade(label="Help", menu=self.help_menu(root))
        return m

    def edit_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        # These items rely on already available key binds, just need to find a way to trigger the events
        m.add_command(label="Undo", accelerator="Ctrl+Z")
        m.add_separator()
        m.add_command(label="Cut", accelerator="Ctrl+X")
        m.add_command(label="Copy", accelerator="Ctrl+C")
        m.add_command(label="Paste", accelerator="Ctrl+V")
        m.add_command(label="Delete", accelerator="Del")
        m.add_separator()
        m.add_command(label="Find...", accelerator="Ctrl+F", command=lambda: self.show_find(None))
        m.add_command(label="Find Next", accelerator="F3")
        m.add_command(label="Replace...", accelerator="Ctrl+H")
        m.add_command(label="Go To...", accelerator="Ctrl+G")
        m.add_separator()
        m.add_command(label="Select All", accelerator="Ctrl+A")
        m.add_command(label="Time/Date", accelerator="F5",
                      command=lambda: self.insert_date(None))  # Adds the current time and date to the document
        return m

    def file_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="New", accelerator="Control+N", command=lambda: self.reset(None))
        m.add_command(label="Open...", accelerator="Ctrl+O", command=lambda: self.open_file(None))
        m.add_command(label="Save", accelerator="Ctrl+S", command=lambda: self.save_as_file(None))
        m.add_command(label="Save As...", command=lambda: self.save_as_file(None))
        m.add_separator()
        m.add_command(label="Print...", accelerator="Ctrl+P")  # ^
        m.add_separator()
        m.add_command(label="Exit", command=self.quit)
        return m

    def help_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="View Help")
        m.add_separator()
        m.add_command(label="About PyNotepad")
        return m

    def context_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="Undo", accelerator="Ctrl+Z")
        m.add_separator()
        m.add_command(label="Cut", accelerator="Ctrl+X")
        m.add_command(label="Copy", accelerator="Ctrl+C")
        m.add_command(label="Paste", accelerator="Ctrl+V")
        m.add_command(label="Delete", accelerator="Del")
        m.add_separator()
        m.add_command(label="Select All", accelerator="Ctrl+A")
        return m

    def format_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="Word Wrap")
        m.add_command(label="Font...")
        return m

    def view_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="Status Bar")  # No idea what this does
        return m

    def set_title(self, title):
        self.root.title = title


if __name__ == '__main__':
    top = ShowGUI()
