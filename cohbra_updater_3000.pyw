import tkinter as tk
import csv
import os
from tkinter import ttk
import git

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("CSV Updater")

        # Define the directories containing the CSV files
        self.csv_dirs = [
            r"C:/Users/Joey/Desktop/cohbra-2/progress"

        ]

        # Get a list of all CSV files in the directories
        self.csv_files = []
        for csv_dir in self.csv_dirs:
            self.csv_files += [os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.endswith(".csv")]

        # Create a label for the input boxes
        self.label = ttk.Label(self.master, text="", font=("Arial", 12))
        self.label.pack(pady=10)

        # Create a frame to hold the labels, dropdowns, and input boxes
        self.frame = ttk.Frame(self.master)
        self.frame.pack()

        # Create a list of labels, dropdowns, and input boxes for each CSV file
        self.labels = []
        self.dropdowns = []
        self.inputs = []
        self.b_values = []
        for i, csv_file in enumerate(self.csv_files):
            # Create a frame to hold the label, dropdown, and input box
            file_frame = ttk.Frame(self.frame, padding=10)
            file_frame.pack()

            # Create a label for the CSV file
            label = ttk.Label(file_frame, text=os.path.basename(csv_file), font=("Arial", 12))
            label.pack(side="left")

            # Create a dropdown for the CSV file
            var = tk.StringVar()
            dropdown = ttk.Combobox(file_frame, textvariable=var, font=("Arial", 12))
            dropdown.pack(side="left")

            # Create a label to display the value in column B of the selected row
            b_value = tk.StringVar()
            b_label = ttk.Label(file_frame, textvariable=b_value, font=("Arial", 12))
            b_label.pack(side="left")

            # Create an input box for the CSV file
            var2 = tk.StringVar()
            entry = ttk.Entry(file_frame, textvariable=var2, font=("Arial", 12))
            entry.pack(side="left")

            # Add the label, dropdown, and input box to the lists
            self.labels.append(label)
            self.dropdowns.append(dropdown)
            self.inputs.append(var2)
            self.b_values.append(b_value)

            # Populate the dropdown with the values from column A of the CSV file
            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)
                values = [row[0] for row in rows if row[0]]
                dropdown["values"] = values

            # Bind the dropdown to a function that displays the value in column B of the selected row
            dropdown.bind("<<ComboboxSelected>>", lambda event, i=i: self.show_b_value(i))

        # Create a button to update the CSV files
        self.update_button = ttk.Button(self.master, text="Update", command=self.update_csv, style="my.TButton")
        self.update_button.pack(pady=10)

        # Create a style object
        style = ttk.Style()

        # Set the background color of all widgets to gray
        style.configure(".", background="#d4d4d4")

        # Set the theme to 'clam'
        style.theme_use('classic')

        # Set the style for the update button
        style.configure("my.TButton", foreground="#fff", background="#007bff", font=("Arial", 12))

    def show_b_value(self, i):
        # Display the value in column B of the selected row
        selected_cell = self.dropdowns[i].get()

        with open(self.csv_files[i], "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            for row in rows:
                if row and row[0] == selected_cell:
                    self.b_values[i].set(row[2])
                    break

    def update_csv(self):
        # Update each CSV file with the corresponding input value
        for i, csv_file in enumerate(self.csv_files):
            value = self.inputs[i].get()
            selected_cell = self.dropdowns[i].get()

            # Open the CSV file and find the row with the selected cell in column A
            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)
                for row in rows:
                    if row and row[0] == selected_cell:
                        if row[2] != value:  # Check if the value has changed
                            row[2] = value
                            break

            # Write the updated CSV file
            with open(csv_file, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            # Push the updated CSV file to Git
            repo = git.Repo(r"C:/Users/Joey/Desktop/cohbra-2/.git")
            if repo.is_dirty(path=csv_file):  # Check if the file has changes to commit
                repo.git.add(csv_file)
                repo.git.commit(m="Update {}".format(os.path.basename(csv_file)))
                repo.git.push()

            # Clear the input box
            self.inputs[i].set("")

root = tk.Tk()
root.configure(bg="#d4d4d4")  # Set the background color of the main app window
app = App(root)
root.geometry("600x800")
root.title("Cohbra updater 3000")
# Set the icon bitmap for the window
icon_path = "C:/Users/Joey/Pictures/icons/snakey.ico"
root.iconbitmap(icon_path)

root.mainloop() 