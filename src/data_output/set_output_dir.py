import json
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

CONFIG_FILE = Path("output_config.json")

def show_info_on_top(title, message):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo(title, message, parent=root)
    root.destroy()

def show_yesno_on_top(title, message):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    result = messagebox.askyesno(title, message, parent=root)
    root.destroy()
    return result

def show_warning_on_top(title, message):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showwarning(title, message, parent=root)
    root.destroy()

def show_retrycancel_on_top(title, message):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    result = messagebox.askretrycancel(title, message, parent=root)
    root.destroy()
    return result

def show_error_on_top(title, message):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showerror(title, message, parent=root)
    root.destroy()

def ask_directory_on_top(title):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    path = filedialog.askdirectory(title=title, parent=root)
    root.destroy()
    return path

def get_output_dir():
    # If config exists, load it
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open() as f:
                config = json.load(f)
                saved_path = Path(config["output_dir"])

            use_saved = show_yesno_on_top(
                "Use Saved Output Folder",
                f"An output folder is already set:\n\n{saved_path}\n\n"
                "Do you want to use this folder?"
            )

            if use_saved:
                return saved_path

        except Exception:
            show_warning_on_top("Invalid Config", "Saved output path is corrupted or unreadable.")

    # Show initial info message
    show_info_on_top(
        "Select Output Folder",
        "Before proceeding, please select the folder where output files will be saved."
    )

    # Ask user to choose a directory
    while True:
        selected = ask_directory_on_top("Select Output Folder")

        if selected:
            output_dir = Path(selected)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save the selected path to the config file
            with CONFIG_FILE.open("w") as f:
                json.dump({"output_dir": str(output_dir)}, f)

            return output_dir
        else:
            retry = show_retrycancel_on_top(
                "No folder selected",
                "You must select a folder to continue.\nTry again?"
            )

            if not retry:
                show_error_on_top(
                    "No folder selected",
                    "You must select a folder to continue."
                )
                raise Exception("No output directory selected.")



# import json
# from pathlib import Path

# # Load the output_dir from the config file
# try:
#     with open("output_config.json") as f:
#         config = json.load(f)
#         output_dir = Path(config["output_dir"])
# except (FileNotFoundError, KeyError, json.JSONDecodeError):
#     print("Couldn't read output_config.json. Did you run set_output_dir.py?")
#     exit(1)

# # Make sure the directory exists
# output_dir.mkdir(parents=True, exist_ok=True)

# print(f"Using output directory: {output_dir}")

# Now you can use output_dir for saving files
# Example:
# with open(output_dir / "output.txt", "w") as f:
#     f.write("Some output")

# import json
# from pathlib import Path

# try:
#     with open("output_config.json") as f:
#         config = json.load(f)
#         output_dir = Path(config["output_dir"])
# except Exception:
#     # Use a default output directory if config not found
#     output_dir = Path(__file__).resolve().parent / "output"
#     output_dir.mkdir(parents=True, exist_ok=True)
#     print("No config found. Using default output folder.")

# print(f"Output will be saved to: {output_dir}")

