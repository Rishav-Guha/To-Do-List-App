import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import json

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("To-Do List App")
        self.geometry("400x400")
        style = Style(theme="flatly")
        style.configure("Custom.TEntry", foreground="gray")

        # Create input field to add tasks
        self.task_input = ttk.Entry(self, font=("TkDefaultFont", 16), width=30, style="Custom.TEntry")
        self.task_input.pack(pady=10)

        # Set placeholder in the input field
        self.task_input.insert(0, "Type Note")

        # Clear placeholder when user clicks in the input field
        self.task_input.bind("<FocusIn>", self.clear_placeholder)

        # Restore placeholder when input field loses focus
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        # Button to add task
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        # Create a listbox to display the tasks added by the user
        self.task_list = tk.Listbox(self, font=("TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons for marking task as complete and deleting tasks
        ttk.Button(self, text="Mark Complete", style="success.TButton",
                   command=self.mark_complete).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton",
                   command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)

        # Button to view task data
        ttk.Button(self, text="Task Data", style="info.TButton",
                   command=self.view_task_data).pack(side=tk.BOTTOM, pady=10)

        self.load_tasks()

    # Function to view task data
    def view_task_data(self):
        completed_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                completed_count += 1
        messagebox.showinfo("Task Data",
                            f"Total Tasks: {total_count}\nCompleted Tasks: {completed_count}")

    # Function to add tasks
    def add_task(self):
        task = self.task_input.get().strip()  # Remove leading/trailing whitespace
        if task and task != "Type Note":  # Check against the correct placeholder
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.sort_tasks()
            self.task_input.delete(0, tk.END)
            self.restore_placeholder()
            self.save_tasks()
        else:
            messagebox.showerror("Error", "Please enter a valid task.")

    # Function to mark a task as complete
    def mark_complete(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            self.sort_tasks()
            self.save_tasks()
        else:
            messagebox.showerror("Error", "Please select the task you want to complete.")

    # Function to delete a task
    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.sort_tasks()
            self.save_tasks()
        else:
            messagebox.showerror("Error", "Please select the task you want to delete.")

    # Clear the placeholder
    def clear_placeholder(self, event=None):
        if self.task_input.get() == "Type Note":  # Ensure matching placeholder value
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    # Restore the placeholder if input is empty
    def restore_placeholder(self, event=None):
        if not self.task_input.get():
            self.task_input.insert(0, "Type Note")  # Ensure matching placeholder value
            self.task_input.configure(style="Custom.TEntry")

    # Function to load saved tasks
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.task_list.itemconfig(tk.END, fg=task["color"])
                    self.sort_tasks()
        except FileNotFoundError:
            pass

    # Function to save tasks
    def save_tasks(self):
        data = []  # Create a list to store tasks
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

    # Function to sort tasks alphabetically
    def sort_tasks(self):
        # Get all tasks from the list
        tasks = [self.task_list.get(idx) for idx in range(self.task_list.size())]
        # Sort the tasks alphabetically
        tasks.sort()
        # Clear the list and reinsert sorted tasks
        self.task_list.delete(0, tk.END)
        for task in tasks:
            self.task_list.insert(tk.END, task)


if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
