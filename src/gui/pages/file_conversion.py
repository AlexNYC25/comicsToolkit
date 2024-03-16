import tkinter as tk
import customtkinter as ctk
import ttkbootstrap
import json
import os

from tkinterdnd2 import DND_FILES
from PIL import Image, ImageTk

from src.utils.conversion import convert_cbr_to_cbz, convert_rar_to_cbz, convert_zip_to_cbz, convert_pdf_to_cbz, convert_epub_to_cbz

class FileConversionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.file_list_info = []
        self.slider_value = tk.IntVar(value=85)

        self.pane = tk.PanedWindow(self, orient=tk.HORIZONTAL)

        self.left_frame = ctk.CTkFrame(self.pane, width=300)
        self.left_frame.pack(fill=tk.BOTH, expand=True)  # Force left_frame to expand
        self.pane.add(self.left_frame)

        self.heading_frame = ctk.CTkFrame(self.left_frame, height=50)
        self.heading_return_button = ctk.CTkButton(self.heading_frame, 
                                                   command=lambda: controller.show_frame("StartPage"), 
                                                   text='Home', 
                                                   width=50, 
                                                   height=50, 
                                                   corner_radius=0, 
                                                   fg_color='#6C6392')
        self.heading_return_button.pack(side=tk.LEFT)
        self.heading_label = ctk.CTkLabel(self.heading_frame, 
                                          text="File Conversion", 
                                          bg_color="#6C6392", 
                                          height=50)
        self.heading_label.pack(fill=tk.X)
        self.heading_frame.pack(fill=tk.X)

        self.heading_intro_text = ctk.CTkTextbox(self.left_frame)
        self.heading_intro_text.insert(tk.END, 
                                       "Welcome to the file conversion page. Here you can convert your files to CBZ format. Simply drag and drop your files into the right pane and click the 'Convert Files' button.")
        self.heading_intro_text.configure(state="disabled", wrap="word", height=110)
        self.heading_intro_text.pack(fill=tk.X)
        
        self.options_label = ctk.CTkLabel(self.left_frame, text="Conversion Options", bg_color="gray", height=50)
        self.options_label.pack(fill=tk.X)

        self.options_label_spacer = ctk.CTkLabel(self.left_frame, text="", height=15)
        self.options_label_spacer.pack(fill=tk.X)

        self.convert_button = ctk.CTkButton(self.left_frame, text="Convert Files", command=self.convert_files, anchor="center")
        self.convert_button.pack(padx=20, fill=tk.X)

        self.convert_button_spacer = ctk.CTkLabel(self.left_frame, text="", height=10)
        self.convert_button_spacer.pack(fill=tk.X)

        self.conversion_slider_label_frame = ctk.CTkFrame(self.left_frame)
        self.conversion_slider_label_frame.pack(fill=tk.X)

        self.conversion_slider_desc_label = ctk.CTkLabel(self.conversion_slider_label_frame, text="Image Conversion Rate")
        self.conversion_slider_desc_label.pack()

        self.conversion_slider_value_label = ctk.CTkLabel(self.conversion_slider_label_frame, textvariable=self.slider_value)
        self.conversion_slider_value_label.pack()

        self.conversion_slider_frame_spacer = ctk.CTkLabel(self.left_frame, text="", height=10)
        self.conversion_slider_frame_spacer.pack(fill=tk.X)

        self.conversion_rate_slider = ctk.CTkSlider(self.left_frame, from_=0, to=100, variable=self.slider_value)
        self.conversion_rate_slider.pack(padx=20, fill=tk.X)

        self.conversion_slider_button_spacer = ctk.CTkLabel(self.left_frame, text="", height=10)
        self.conversion_slider_button_spacer.pack(fill=tk.X)

        self.convert_compress_button = ctk.CTkButton(self.left_frame, text="Convert and Compress", command=self.convert_files, anchor="center")
        self.convert_compress_button.pack(padx=20, fill=tk.X)

        self.convert_compress_text_spacer = ctk.CTkLabel(self.left_frame, text="", height=10)
        self.convert_compress_text_spacer.pack(fill=tk.X)

        self.convert_compress_text = ctk.CTkTextbox(self.left_frame)
        self.convert_compress_text.insert(tk.END,
                                            "This option will convert the files to CBZ format and compress the images to the specified quality.")
        self.convert_compress_text.configure(state="disabled", wrap="word", height=70)
        self.convert_compress_text.pack(fill=tk.X)


        self.right_frame = ctk.CTkFrame(self.pane, width=500)
        self.right_frame.pack(fill=tk.BOTH, expand=True)  # Force right_frame to expand
        self.pane.add(self.right_frame)

        self.file_list_options = ctk.CTkFrame(self.right_frame, width=500, height=25)
        self.file_list_options.pack(fill=tk.X, expand=True)

        self.file_list_options_label = ctk.CTkLabel(self.file_list_options, text="Files", bg_color="blue", height=25)
        self.file_list_options_label.pack(fill=tk.X)

        self.file_list = ctk.CTkFrame(self.right_frame, width=500, height=550)
        self.file_list.pack(fill=tk.BOTH, expand=True)  # Force file_list to expand
        self.file_list.drop_target_register(DND_FILES)
        self.file_list.dnd_bind('<<Drop>>', self.drop_files)

        self.status_label = ctk.CTkLabel(self.right_frame, text="Status: Idle", height=25, width=500, bg_color="gray")
        self.status_label.pack(fill=tk.BOTH, expand=True)

        self.pane.pack(fill=tk.BOTH, expand=True)  # Force pane to expand

    def parse_dropped_files(self, dropped_files_str):
        # Initialize an empty list to hold the file paths
        files = []
        temp_path = ""
        inside_braces = False

        # Iterate through each character in the dropped files string
        for char in dropped_files_str:
            if char == '{':
                inside_braces = True
                temp_path += char  # Start capturing a path with spaces
            elif char == '}':
                inside_braces = False
                temp_path += char
                files.append(temp_path)  # Complete a path and add to the list
                temp_path = ""  # Reset the temporary path holder
            elif char == ' ' and not inside_braces:
                if temp_path:  # If there's a path outside braces, add it to the list
                    files.append(temp_path)
                    temp_path = ""  # Reset the temporary path holder
            else:
                temp_path += char  # Continue building the current path

        # Add the last path if it wasn't added yet
        if temp_path:
            files.append(temp_path)

        # Handle paths with braces by removing the leading and trailing braces
        files = [file.strip('{}') for file in files]

        return files
    
    def get_file_size(self, file_path):
        return os.path.getsize(file_path)

    def convert_files(self):
        print("Converting files to CBZ")

    def drop_files(self, event):
        print("Dropped files")

        # split the event.data into a list of the paths of the files dropped
        files = self.parse_dropped_files(event.data)

        for file in files:
            # for each file path, get the file name and the file type
            file_name = file.split("/")[-1]
            file_type = file.split(".")[-1]

            # we now want to get the size of the file
            file_size = self.get_file_size(file)

            print(f"File size: {file_size}")

            new_file_info = {
                "file_name": file_name,
                "file_type": file_type,
                "file_size": file_size,
                "file_path": file
            }

            self.file_list_info.append(new_file_info)
