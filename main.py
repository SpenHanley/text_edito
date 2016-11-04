import tkinter as tk
import sys
from tkinter import filedialog
# TODO: Make the frame match the root node when the window is resized
# TODO: Make the root title update when it is changed
# TODO: Implement the actions for the context menu aswell as the remaining menu items
# TODO: Implement either a library or a custom print dialog as no print dialog is included
# TODO: Trigger undo command from menu item for both edit and context menu


class ShowGUI:
    def __init__(self):
        self.root = self.config_root()
        self.frame = self.config_frame(self.root)
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
        return rt

    def config_frame(self, root):
        fr = tk.Frame(root)
        fr.grid(row=0, column=0)
        return fr

    def bind_all(self):
        self.text_area.bind("<Button-3>", self.popup)
        self.root.bind("<Control-o>", self.open_file)
        self.text_area.bind("<Control-o>", self.open_file)

    def popup(self, event):
        self.cont_menu.post(event.x_root, event.y_root)

    def save_as_file(self):
            if self.file is None:
                self.file = filedialog.asksaveasfilename(**self.file_opts)
                file = open(self.file, 'w+')
                file.write(self.text_area.get(0.0, tk.END))
                print(self.file)
            else:
                self.save_file()

    def save_file(self):
        if self.file:
            file = open(self.file, 'w+')
            file.write(self.text_area.get(0.0, tk.END))

    def open_file(self, arg):
        self.file = filedialog.askopenfilename(**self.file_opts)
        i = 1.0
        if self.file:
            with open(self.file, 'r') as f:
                self.text_area.insert(1.0, f.read())
                self.set_title(self.file)

    def reset(self):
        self.text_area.delete('1.0', tk.END)
        self.file = None
        self.set_title('Untitled - PyNotepad')

    def quit(self):
        sys.exit(0) # Exit out

    def text_widget(self, frame):
        y_scroll = tk.Scrollbar(frame)
        y_scroll.grid(row=0, column=1, sticky="nsew")
        x_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        x_scroll.grid(row=1, column=0, sticky="nsew")
        t = tk.Text(self.frame, wrap="none", yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set, undo=True)
        t.grid(row=0, column=0)
        y_scroll.config(command=t.yview)
        x_scroll.config(command=t.xview)
        return t

    # Create the menus
    def make_menu_bar(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_cascade(label="File", menu=self.file_menu(root))
        m.add_cascade(label="Edit", menu=self.edit_menu(root))
        m.add_cascade(label="Format", menu=self.format_menu(root))
        m.add_cascade(label="View",   menu=self.view_menu(root))
        m.add_cascade(label="Help", menu=self.help_menu(root))
        return m

    def edit_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="Undo", accelerator="Ctrl+Z")
        m.add_separator()
        m.add_command(label="Cut", accelerator="Ctrl+X")
        m.add_command(label="Copy", accelerator="Ctrl+C")
        m.add_command(label="Paste", accelerator="Ctrl+V")
        m.add_command(label="Delete", accelerator="Del")
        m.add_separator()
        m.add_command(label="Find...", accelerator="Ctrl+F")
        m.add_command(label="Find Next", accelerator="F3")
        m.add_command(label="Replace...", accelerator="Ctrl+H")
        m.add_command(label="Go To...", accelerator="Ctrl+G")
        m.add_separator()
        m.add_command(label="Select All", accelerator="Ctrl+A")
        m.add_command(label="Time/Date", accelerator="F5") # Adds the current time and date to the document
        return m

    def file_menu(self, root):
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="New", accelerator="Control+N", command=self.reset)
        m.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        m.add_command(label="Save", command=self.save_as_file, accelerator="Ctrl+S")
        m.add_command(label="Save As...", command=self.save_as_file)
        m.add_separator()
        m.add_command(label="Print...", accelerator="Ctrl+P") # See todo above
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
        m.add_command(label="Status Bar") # No idea what this does
        return m

    def set_title(self, title):
        self.root.title = title


if __name__ == '__main__':
    top = ShowGUI()