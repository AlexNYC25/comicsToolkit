import customtkinter
import tkinter as tk
import ttkbootstrap as ttk
from src.gui.pages.file_conversion import FileConversionPage


class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        fcPage = FileConversionPage(self)

        fcPage.place(in_=master, x=0, y=0, relwidth=1, relheight=1)

        self.master = master
        self.master.title("Main Window")
        self.master.geometry("800x600")

        self.label = tk.Label(self, text="Hello, world!")
        self.label.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", command=fcPage.show)
        self.quit.pack(side="bottom")



