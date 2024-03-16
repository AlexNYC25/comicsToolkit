import ebooklib
from ebooklib import epub
import fitz  # PyMuPDF
import os
import rarfile
import shutil
import tempfile
import zipfile
import rarfile
import os
import shutil
import re

def convert_cbr_to_cbz(cbr_path):
    """
    Converts a .cbr file to a .cbz file.
    """
    return convert_rar_archive_to_cbz(cbr_path)

def convert_rar_to_cbz(rar_path):
    """
    Converts a RAR archive to a .cbz file.
    """
    return convert_rar_archive_to_cbz(rar_path)

def sanitize_filename(filename):
    """
    Sanitizes the given filename by removing invalid characters.
    """
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def convert_rar_archive_to_cbz(rar_path):
    """
    Core function to convert RAR (including .cbr) archives to CBZ.
    """
    rarfile.UNRAR_TOOL = 'unrar'  # Adjust based on your system's configuration

    # get the file name of the RAR archive without the extension
    file_name = os.path.basename(rar_path).replace('.cbr', '').replace('.rar', '')

    # generate a random temporary directory to extract the images
    temp_dir = tempfile.mkdtemp()

    # extract images from RAR archive
    with rarfile.RarFile(rar_path, 'r') as rf:
        for i, entry in enumerate(rf.infolist()):
            if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_name = sanitize_filename(entry.filename)
                image_path = os.path.join(temp_dir, image_name)
                with open(image_path, 'wb') as image_file:
                    image_file.write(rf.read(entry))
            if entry.filename.endswith(('.xml', '.txt')):
                text_name = sanitize_filename(entry.filename)
                text_path = os.path.join(temp_dir, text_name)
                with open(text_path, 'wb') as text_file:
                    text_file.write(rf.read(entry))

    return temp_dir

def convert_zip_to_cbz(zip_path):
    """
    Converts a ZIP file to a CBZ file.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copy(zip_path, temp_dir)
        base_name = os.path.splitext(os.path.basename(zip_path))[0]
        cbz_path = os.path.join(temp_dir, base_name + ".cbz")
        os.rename(os.path.join(temp_dir, os.path.basename(zip_path)), cbz_path)
        return cbz_path

def convert_pdf_to_cbz(pdf_path):
    """
    Converts a PDF file to a CBZ file by extracting images.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copy(pdf_path, temp_dir)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        images_dir = os.path.join(temp_dir, base_name)
        os.makedirs(images_dir)

        doc = fitz.open(os.path.join(temp_dir, os.path.basename(pdf_path)))
        for page_num in range(len(doc)):
            for img in doc.get_page_images(page_num):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_path = os.path.join(images_dir, f"image{page_num}_{xref}.png")
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_bytes)

        cbz_path = os.path.join(temp_dir, base_name + ".cbz")
        with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(images_dir):
                for file in files:
                    zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), images_dir))

        return cbz_path

def convert_epub_to_cbz(epub_path):
    """
    Converts an EPUB file to a CBZ file by extracting images.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copy(epub_path, temp_dir)
        base_name = os.path.splitext(os.path.basename(epub_path))[0]
        images_dir = os.path.join(temp_dir, base_name)
        os.makedirs(images_dir)

        book = epub.read_epub(os.path.join(temp_dir, os.path.basename(epub_path)))
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_IMAGE:
                image_path = os.path.join(images_dir, item.get_name())
                with open(image_path, 'wb') as img_file:
                    img_file.write(item.content)

        cbz_path = os.path.join(temp_dir, base_name + ".cbz")
        with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(images_dir):
                for file in files:
                    zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), images_dir))

        return cbz_path

# Example usage for testing
if __name__ == "__main__":
    # Test paths
    cbr_path = 'path/to/your/file.cbr'
    rar_path = 'path/to/your/file.rar'
    zip_path = 'path/to/your/file.zip'
    pdf_path = 'path/to/your/file.pdf'
    def extract_images_from_rar(rar_path, temp_dir):
        with rarfile.RarFile(rar_path, 'r') as rf:
            for i, entry in enumerate(rf.infolist()):
                if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    image_path = os.path.join(temp_dir, f"image{i}.{entry.filename.split('.')[-1]}")
                    with open(image_path, 'wb') as image_file:
                        image_file.write(rf.read(entry))

    # Example usage
    if __name__ == "__main__":
        rar_path = 'path/to/your/file.rar'
        temp_dir = 'path/to/temp/dir'
        with tempfile.TemporaryDirectory() as temp_dir:
            extract_images_from_rar(rar_path, temp_dir)
    epub_path = 'path/to/your/file.epub'
    
    # Example function calls
    # cbz_path = convert_cbr_to_cbz(cbr_path)
    # print(f"Converted CBZ file path: {cbz_path}")
