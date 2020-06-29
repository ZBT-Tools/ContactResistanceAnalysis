import tkinter.filedialog
import tkinter as tk
from GUI_doc import importData

filename = ''
def getFile():
    filename = tk.filedialog.askopenfilename(initialdir = "C:/Users/Kapp/Desktop/CR/", title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
    importData(filename)

