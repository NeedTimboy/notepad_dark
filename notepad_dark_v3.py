import tkinter as tk
from tkinter import filedialog, messagebox

# Function to update window title
def update_title(saved=False):
    if current_file:
        title = f"{current_file.split('/')[-1]} | Notepad Dark"
    else:
        title = "Notepad Dark"
    
    if not saved:
        root.title(f"*{title}")
    else:
        root.title(title)

# Function to save the file with UTF-8 encoding, without the success pop-up
def save_file():
    global text_changed
    if current_file:
        try:
            with open(current_file, 'w', encoding='utf-8') as file:
                file.write(text_area.get("1.0", tk.END))
            text_changed = False
            update_title(saved=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
    else:
        save_as_file()

# Function to "Save As" with UTF-8 encoding
def save_as_file():
    global current_file, text_changed
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_area.get("1.0", tk.END))
            text_changed = False
            update_title(saved=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

# Function to open a file with UTF-8 encoding
def open_file():
    global current_file, text_changed
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.delete("1.0", tk.END)  # Clear current text
                text_area.insert(tk.END, file.read())  # Insert file contents
            text_changed = False
            update_title(saved=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

# Function to insert a ✔️ at the cursor position (without extra space)
def insert_check_mark():
    text_area.insert(tk.INSERT, "✔️")
    mark_as_edited()

# Function to insert a ✘ at the cursor position
def insert_cross_mark():
    text_area.insert(tk.INSERT, "✘")
    mark_as_edited()

# Function to toggle bold on/off for selected text
def toggle_bold(event=None):
    try:
        current_tags = text_area.tag_names(tk.SEL_FIRST)
        if "bold" in current_tags:
            text_area.tag_remove("bold", tk.SEL_FIRST, tk.SEL_LAST)
        else:
            text_area.tag_add("bold", tk.SEL_FIRST, tk.SEL_LAST)
        mark_as_edited()
    except tk.TclError:
        pass

# Mark the text as edited
def mark_as_edited(event=None):
    global text_changed
    if not text_changed:
        text_changed = True
        update_title()

# Handle window closing with unsaved changes prompt
def on_closing():
    if text_changed:
        response = messagebox.askyesnocancel("Quit", "Do you want to save your changes before closing?")
        if response is True:  # "Yes" - Save the file
            save_file()
            if not text_changed:  # Only close if save was successful
                root.destroy()
        elif response is False:  # "No" - Close without saving
            root.destroy()
    else:
        root.destroy()

# Initialize the application
root = tk.Tk()
root.title("Notepad Dark")
current_file = None
text_changed = False

# Configure window dimensions and allow resizing
root.geometry("800x600")
root.resizable(True, True)

# Dark mode styling
root.config(bg='#2d2d2d')

# Create a minimalist scrollbar style
style = {"bg": "#2d2d2d", "highlightthickness": 0}

# Frame to hold the text and scrollbar
frame = tk.Frame(root, **style)
frame.pack(fill=tk.BOTH, expand=True)

# Scrollbar logic
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, bg="white", troughcolor='#1e1e1e', activebackground='#666666',
                         highlightbackground='#2d2d2d')
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Text area (where you type) with word wrap enabled and linked to the scrollbar
text_area = tk.Text(frame, font=("Consolas", 12), wrap=tk.WORD, bg='#1e1e1e', fg='#dcdcdc', insertbackground='white', 
                    yscrollcommand=scrollbar.set, undo=True)
text_area.pack(fill=tk.BOTH, expand=1)

scrollbar.config(command=text_area.yview)

# Define bold tag
text_area.tag_configure("bold", font=("Consolas", 12, "bold"))

# Create menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
menu_bar.add_cascade(label="File", menu=file_menu)

# Toolbar menu with ✔️ and ✘ buttons
toolbar_menu = tk.Menu(menu_bar, tearoff=0)
toolbar_menu.add_command(label="✔️", command=insert_check_mark)
toolbar_menu.add_command(label="✘", command=insert_cross_mark)
menu_bar.add_cascade(label="Toolbar", menu=toolbar_menu)

# Apply the menu to the root window
root.config(menu=menu_bar)

# Bind Ctrl+B to toggle bold formatting
root.bind("<Control-b>", toggle_bold)

# Bind events to mark text as edited
text_area.bind("<Key>", mark_as_edited)

# Handle window close with confirmation for unsaved changes
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()
