import os
import easyocr
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_images_to_text(folder_path, output_file):
    """
    Converts all JPEG and PNG images in a folder to text using EasyOCR
    and continuously updates a single output file.

    :param folder_path: Path to the folder containing the images
    :param output_file: Path to the output file where extracted text will be saved
    """
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", f"The folder '{folder_path}' does not exist.")
        return

    # Create the output file if it does not exist
    if not os.path.exists(output_file):
        open(output_file, 'w', encoding='utf-8').close()

    # Read already processed files to avoid duplicates
    processed_files = set()
    with open(output_file, 'r', encoding='utf-8') as outfile:
        for line in outfile:
            if line.startswith("Text from"):
                processed_files.add(line.split(":")[1].strip())

    # Initialize EasyOCR
    reader = easyocr.Reader(['en', 'it'])  # Add more languages if needed

    # Process each image in the folder
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            if file_name in processed_files:
                print(f"File {file_name} already processed, skipping...")
                continue

            file_path = os.path.join(folder_path, file_name)
            try:
                # Load the image and extract text with EasyOCR
                text = reader.readtext(file_path, detail=0)  # `detail=0` returns only the extracted text

                # Write the text directly to the output file
                with open(output_file, 'a', encoding='utf-8') as outfile:
                    outfile.write(f"Text from {file_name}:\n")
                    outfile.write("\n".join(text))
                    outfile.write("\n" + "=" * 50 + "\n")
                
                print(f"Text extracted and saved from {file_name}.")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    messagebox.showinfo("Completed", f"All texts have been saved in:\n{output_file}")

def main():
    """Main function to select the folder and start processing."""
    # Configure the GUI for folder selection
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Dialog to select a folder
    folder_path = filedialog.askdirectory(title="Select a folder with JPEG or PNG images")
    if not folder_path:
        messagebox.showwarning("Warning", "No folder selected. Exiting.")
        return

    # Define the output file in the same folder
    output_file = os.path.join(folder_path, "extracted_text_output.txt")

    # Start the image-to-text conversion
    convert_images_to_text(folder_path, output_file)

if __name__ == "__main__":
    main()
