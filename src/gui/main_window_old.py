from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import filedialog
from tkinter import messagebox
import shutil
import zipfile

from src.utils.conversion import convert_cbr_to_cbz, convert_rar_to_cbz, convert_zip_to_cbz, convert_pdf_to_cbz, convert_epub_to_cbz

class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_list_info = []

        self.root = master
        self.root.title("Drag and Drop Example")
        self.root.geometry("800x600")

        # Create a style object
        style = Style(theme='darkly')

        # Configure the Treeview's background, field background, and font color
        style.configure('Treeview',
                        background='#343a40',  # Dark gray background
                        fieldbackground='#343a40',  # Matching field background
                        foreground='white',  # Text color
                        rowheight=25)  # Adjust row height as needed

        # Configure the Treeview Heading to match
        style.configure('Treeview.Heading',
                        background='#343a40',
                        foreground='white',
                        font=('Helvetica', 10, 'bold'))  # Example font configuration

        # Adjust the style of the selected row to enhance visibility
        style.map('Treeview',
                background=[('selected', '#007bff')])  # Use a bootstrap primary color for selection
        
        # Configure a more visible label style
        style.configure('Visible.TLabel', foreground='white', font=('Helvetica', 14, 'bold'))

        style.configure('Large.TButton', padding=[10, 5], font=('Helvetica', 12, 'bold'))

        # Create a PanedWindow
        self.paned_window = ttk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill='both', expand=True)

        # Left Pane (Settings)
        self.left_pane = tk.Frame(self.paned_window, width=100, height=600)
        self.paned_window.add(self.left_pane)

        # Button for converting files to CBZ
        self.convert_button = ttk.Button(self.left_pane, text="Convert to CBZ file", command=self.convert_to_cbz, bootstyle='primary')
        self.convert_button.pack(pady=50, padx=40)

        self.compression_frame = tk.Frame(self.left_pane)  # Set your desired background color here
        self.compression_frame.pack(padx=10, pady=10, fill=tk.X)

        # Set up the scale value and its formatting
        self.scale_value = tk.DoubleVar(value=85)
        self.formatted_scale_value = tk.StringVar()
        self.update_formatted_value()  # Initial update
        self.scale_value.trace("w", self.update_formatted_value)

        # Use ttkbootstrap Scale with corrected bootstyle usage
        self.compression_scale = ttk.Scale(self.compression_frame, from_=1, to=100, orient='horizontal', bootstyle='primary', variable=self.scale_value)
        self.compression_scale.pack(padx=10, pady=10, fill='x')

        # Create a Label to display the current value of the scale
        self.value_label = ttk.Label(self.compression_frame, textvariable=self.formatted_scale_value, style='Visible.TLabel')
        self.value_label.pack(pady=10)

        # Button for converting and compressing
        self.convert_compress_button = ttk.Button(self.compression_frame, text="Convert to CBZ and compress", command=self.convert_and_compress, bootstyle='primary', style='Large.TButton')
        self.convert_compress_button.pack(pady=10)

        # Right Pane (File List)
        self.right_pane = tk.Frame(self.paned_window, width=300, bg='white', height=600, borderwidth=0, relief="flat")
        self.paned_window.add(self.right_pane)

        # Enable drag and drop for the right pane
        self.right_pane.drop_target_register(DND_FILES)
        self.right_pane.dnd_bind('<<Drop>>', self.on_drop)

        # Initialize Treeview for the right pane to display file information
        self.file_list = ttk.Treeview(self.right_pane, style='Treeview')
        self.file_list.pack(fill=tk.BOTH, expand=True)

        # Define columns
        self.file_list['columns'] = ('File Name', 'Extension', 'Size')
        self.file_list.column("#0", width=0, stretch=tk.NO)  # Hide the first empty column
        self.file_list.column("File Name", anchor=tk.W, width=120)
        self.file_list.column("Extension", anchor=tk.W, width=40)
        self.file_list.column("Size", anchor=tk.CENTER, width=60)

        # Create Headings
        self.file_list.heading("#0", text="", anchor=tk.W)
        self.file_list.heading("File Name", text="File Name", anchor=tk.W)
        self.file_list.heading("Extension", text="Extension", anchor=tk.W)
        self.file_list.heading("Size", text="Size", anchor=tk.CENTER)

        # Bind the selection event
        self.file_list.bind("<<TreeviewSelect>>", self.on_file_select)
    

    def display_info_message(self, message):
        # Ensure the message is not too long
        #if len(message) > 44:
            #message = message[:41] + '...'

        # Create a new top-level window
        dialog = tk.Toplevel(self)

        # Set the window size and position
        dialog.geometry("400x200+300+300")  # Width x Height + X position + Y position

        # Create a label with the message
        message_label = tk.Label(dialog, text=message, wraplength=350)
        message_label.pack(padx=20, pady=20)

        # Create an OK button that destroys the dialog
        ok_button = tk.Button(dialog, text="OK", command=dialog.destroy)
        ok_button.pack(pady=10)

    def update_formatted_value(self, *args):
        formatted_value = f"{self.scale_value.get():.2f}"
        self.formatted_scale_value.set(formatted_value)
        
    def scale_updated(self, *args):
        print(f"Compression level updated: {self.compression_scale.get()}")

    def print_file_path(file_path):
        print('from file path callback ' + file_path)

    def convert_to_cbz(self):
        selected_items = self.file_list.selection()

        
        for item_id in selected_items:
            file_name = self.file_list.item(item_id)['values'][0]

            item = self.file_list.item(item_id)
            file_path = item['values'][0]  # Adjust this index if necessary
            file_extension = os.path.splitext(file_path)[-1].lower()

            just_file_name = os.path.basename(file_path)
            # create a dialog to select where to save the file
            save_path = filedialog.askdirectory(title='Select where to save the file')
            
            # Map file extensions to their respective conversion functions
            conversion_map = {
                '.cbr': convert_cbr_to_cbz,
                '.rar': convert_rar_to_cbz,
                '.zip': convert_zip_to_cbz,
                '.pdf': convert_pdf_to_cbz,
                '.epub': convert_epub_to_cbz
            }
            
            conversion_func = conversion_map.get(file_extension)

            if not conversion_func:
                print(f"Unsupported file format for {file_path}")
                continue

            try:
                temp_path = conversion_func(file_path)

                where_to_save = filedialog.asksaveasfilename(defaultextension='.cbz', filetypes=[('CBZ Files', '*.cbz')], initialfile=just_file_name)

                print(f"Where to save: {where_to_save}")
                
                cbz_path = os.path.join(where_to_save)
                with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root, dirs, files in os.walk(temp_path):
                        for file in sorted(files):
                            zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_path))

                # remove the temporary directory
                shutil.rmtree(temp_path)
            except Exception as e:
                print(f"Error converting {file_name}: {e}")

            self.display_info_message(f"Conversion of {just_file_name} complete!")
    def convert_and_compress(self):
        compression_level = self.compression_scale.get()  # Get the current value of the slider
        print(f"Converting and compressing with compression level: {compression_level}")
        # Implement the conversion and compression logic here

    def on_drop(self, event):
        """
        Handle files dropped onto the application, adding them to the Treeview
        with their full file paths.
        """
        # Split the dropped files into a list (file paths are received as a string)
        dropped_files = self.root.tk.splitlist(event.data)
        
        for file_path in dropped_files:
            # Here you could add additional logic to filter for specific file types or to ignore certain files
            
            # Extract information about the file for display in the Treeview
            file_name = os.path.abspath(file_path)
            file_extension = os.path.splitext(file_name)[1].lower()
            
            # Optionally, get file size or other properties here
            file_size = os.path.getsize(file_name)
            
            # Insert the file into the Treeview
            # Assuming your Treeview is set up with columns like ('File Name', 'Extension', 'Full Path')
            # Adjust the column identifiers based on your setup
            self.file_list.insert("", "end", values=(file_name, file_extension, file_size))



    def process_file(self, filepath):
        # Define the allowed extensions
        allowed_extensions = ('.cbz', '.cbr', '.zip', '.rar', '.pdf', '.epub')
        
        # Extract the file extension and basename
        file_extension = os.path.splitext(filepath)[1].lower()  # Convert to lowercase to ensure case-insensitive comparison
        file_name = os.path.basename(filepath)

        # Check if the file has an allowed extension and does not start with '.'
        if file_extension in allowed_extensions and not file_name.startswith('.'):
            file_size_bytes = os.path.getsize(filepath)
            
            # Format the file size as KB or MB
            if file_size_bytes < 1024 * 1024:  # Smaller than 1 MB
                readable_size = f"{file_size_bytes / 1024:.2f} KB"
            else:
                readable_size = f"{file_size_bytes / (1024 * 1024):.2f} MB"

            # Append file details to the list (if you still need this for other purposes)
            self.file_list_info.append({
                "path": filepath,
                "extension": file_extension,
                "size": readable_size  # Store the formatted size
            })

            # Insert the file into the Treeview
            self.file_list.insert("", "end", values=(file_name, file_extension, readable_size))
        else:
            print(f"Skipped: {filepath} (unsupported file type or hidden file)")



    def on_file_select(self, event):
        # Get the item IDs of the selected items
        selected_items = self.file_list.selection()
        # Iterate through the selected items
        for item_id in selected_items:
            # Retrieve the item's information
            item = self.file_list.item(item_id)
            # Assuming the first value in the 'values' list is the file name
            file_name = item['values'][0]
            # Print the file name to the console
            print(f"Selected file: {file_name}")



def create_app(theme='darkly'):
    root = ttk.Window(themename=theme)
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    create_app()
