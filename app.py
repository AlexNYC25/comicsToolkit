import tkinter as tk
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from PIL import Image

from src.gui.pages.file_conversion import FileConversionPage

class SampleApp(TkinterDnD.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Comics Toolkit")
        self.geometry("800x600")
        png_icon = Image.open("src/resources/icons/icon.png")
        img = png_icon.convert("RGBA")
        img.save("src/resources/icons/icon.ico", "ICO")
        self.iconbitmap("src/resources/icons/icon.ico")  # Corrected path

        # Container for all pages
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, FileConversionPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Put all of the pages in the same location;
            # The one on the top of the stacking order will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        page_one_button = ctk.CTkButton(self, text="Go to Page One",
                                    command=lambda: controller.show_frame("PageOne"))
        page_two_button = ctk.CTkButton(self, text="Go to Page Two",
                                    command=lambda: controller.show_frame("PageTwo"))
        
        file_conversion_button = ctk.CTkButton(self, text="Go to File Conversion Page",
                                    command=lambda: controller.show_frame("FileConversionPage"))
        page_one_button.pack()
        page_two_button.pack()
        file_conversion_button.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page one")
        label.pack(side="top", fill="x", pady=10)
        back_button = tk.Button(self, text="Back to start page",
                                command=lambda: controller.show_frame("StartPage"))
        back_button.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page two")
        label.pack(side="top", fill="x", pady=10)
        back_button = tk.Button(self, text="Back to start page",
                                command=lambda: controller.show_frame("StartPage"))
        back_button.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
