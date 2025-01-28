import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from configparser import ConfigParser
from tkinter.font import families
from ttkthemes import ThemedTk  # Import ThemedTk for theming

# Global settings
settings = {
    "font_style": "Arial",
    "font_size": 12,
    "theme": "arc"  # Default theme is arc (you can change it later)
}

# Load settings from an .ini file
def load_settings():
    config = ConfigParser()
    if config.read("settings.ini"):
        settings["font_style"] = config.get("Settings", "font_style")
        settings["font_size"] = config.getint("Settings", "font_size")
        settings["theme"] = config.get("Settings", "theme")

# Save settings to an .ini file
def save_settings():
    config = ConfigParser()
    config["Settings"] = {
        "font_style": settings["font_style"],
        "font_size": settings["font_size"],
        "theme": settings["theme"]
    }
    with open("settings.ini", "w") as configfile:
        config.write(configfile)

# Function to apply settings
def apply_settings():
    selected_font = font_style_combobox.get() or settings["font_style"]
    selected_size = font_size_combobox.get() or settings["font_size"]
    selected_theme = theme_combobox.get() or settings["theme"]

    settings["font_style"] = selected_font
    settings["font_size"] = int(selected_size)
    settings["theme"] = selected_theme

    save_settings()  # Save the changes to the .ini file
    update_theme()
    messagebox.showinfo("Settings Applied", "Your changes have been applied!")

# Function to reset settings to default values
def reset_settings():
    settings["font_style"] = "Arial"
    settings["font_size"] = 12
    settings["theme"] = "arc"
    font_style_combobox.set("Arial")
    font_size_combobox.set(12)
    theme_combobox.set("arc")
    save_settings()
    update_theme()

# Function to update the theme using ttkthemes
def update_theme():
    window.set_theme(settings["theme"])
    for widget in window.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button)):
            widget.configure(font=(settings["font_style"], settings["font_size"]))
        elif isinstance(widget, ttk.Combobox):
            widget.configure(font=(settings["font_style"], settings["font_size"]))

# Function to create tooltips
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(window)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{widget.winfo_rootx()}+{widget.winfo_rooty() + 25}")
    label = tk.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1)
    label.pack()

# Function to convert the image with a progress bar
def convert_image():
    input_file = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("All Files", "*.*")]
    )
    
    if not input_file:
        return  # User canceled

    selected_format = format_combobox.get()
    if not selected_format:
        messagebox.showerror("Error", "Please select a format to convert to.")
        return

    output_file = filedialog.asksaveasfilename(
        title=f"Save as {selected_format.upper()}",
        defaultextension=f".{selected_format.lower()}",
        filetypes=[(f"{selected_format.upper()} Files", f"*.{selected_format.lower()}")]
    )
    
    if not output_file:
        return  # User canceled

    try:
        progress_bar.start()  # Start the progress bar
        img = Image.open(input_file)
        img.save(output_file, format=selected_format.upper())
        progress_bar.stop()  # Stop the progress bar
        messagebox.showinfo("Success", f"File converted and saved as {output_file}")
    except FileNotFoundError:
        progress_bar.stop()
        messagebox.showerror("Error", "File not found. Please check the file path.")
    except PermissionError:
        progress_bar.stop()
        messagebox.showerror("Error", "You don't have permission to save in this location.")
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", f"Failed to convert image: {e}")

# Create the main GUI window using ThemedTk for theming support
window = ThemedTk()
window.title("PixFormat")
window.geometry("500x500")

pixformat_themes = window.get_themes()

# Create a Notebook for tabs
notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")

# Tab 1: Image Converter
converter_frame = ttk.Frame(notebook)
notebook.add(converter_frame, text="Converter")

label = ttk.Label(converter_frame, text="Image Format Converter", font=(settings["font_style"], 16))
label.pack(pady=10)

format_label = ttk.Label(converter_frame, text="Choose a format to convert to:", font=(settings["font_style"], settings["font_size"]))
format_label.pack(pady=5)

supported_formats = sorted([
    "BMP", "DDS", "EPS", "GIF", "ICO", "IM", "JPEG", "JPEG2000",
    "MSP", "PCX", "PNG", "PPM", "SGI", "SPIDER", "TGA", "TIFF", "WEBP", "XBM"
])
format_combobox = ttk.Combobox(converter_frame, values=supported_formats, state="readonly", font=(settings["font_style"], settings["font_size"]))
format_combobox.pack(pady=5)
format_combobox.set("PNG")

convert_button = ttk.Button(converter_frame, text="Convert Image", command=convert_image)
convert_button.pack(pady=20)

# Progress bar for image conversion
progress_bar = ttk.Progressbar(converter_frame, length=300, mode='indeterminate')
progress_bar.pack(pady=10)

# Tab 2: Settings
settings_frame = ttk.Frame(notebook)
notebook.add(settings_frame, text="Settings")

settings_label = ttk.Label(settings_frame, text="Settings", font=(settings["font_style"], 16))
settings_label.pack(pady=10)

font_style_label = ttk.Label(settings_frame, text="Font Style:", font=(settings["font_style"], settings["font_size"]))
font_style_label.pack(pady=5)

# Fetch all system fonts
available_fonts = sorted(families())
font_style_combobox = ttk.Combobox(settings_frame, values=available_fonts, state="readonly")
font_style_combobox.pack(pady=5)
font_style_combobox.set(settings["font_style"])

font_size_label = ttk.Label(settings_frame, text="Font Size:", font=(settings["font_style"], settings["font_size"]))
font_size_label.pack(pady=5)

font_size_combobox = ttk.Combobox(settings_frame, values=[8, 10, 12, 14, 16, 18, 20, 24, 28, 32], state="readonly")
font_size_combobox.pack(pady=5)
font_size_combobox.set(settings["font_size"])

theme_label = ttk.Label(settings_frame, text="Theme:", font=(settings["font_style"], settings["font_size"]))
theme_label.pack(pady=5)

theme_combobox = ttk.Combobox(settings_frame, values=pixformat_themes, state="readonly")
theme_combobox.pack(pady=5)
theme_combobox.set(settings["theme"])

apply_button = ttk.Button(settings_frame, text="Apply Settings", command=apply_settings)
apply_button.pack(pady=5)

reset_button = ttk.Button(settings_frame, text="Reset to Default", command=reset_settings)
reset_button.pack(pady=5)

# Tab 3: About
about_frame = ttk.Frame(notebook)
notebook.add(about_frame, text="About")

about_label = ttk.Label(about_frame, text="PixFormat - Image Format Converter", font=(settings["font_style"], 16))
about_label.pack(pady=10)

about_text = """
PixFormat is a simple image format converter tool built with Python.
It allows you to convert images between various formats like PNG, JPG, BMP, TIFF, and more.
This tool also allows you to customize fonts and themes for a better user experience.

Version: 1.0.0
Author: Sheekovic
"""
about_info = ttk.Label(about_frame, text=about_text, font=(settings["font_style"], settings["font_size"]))
about_info.pack(pady=10)

# Create tooltips
create_tooltip(theme_combobox, "Select a theme for the application")
create_tooltip(font_style_combobox, "Select a font style")
create_tooltip(font_size_combobox, "Select a font size")

# Run the GUI application
update_theme()
window.mainloop()
