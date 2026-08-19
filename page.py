import tkinter as tk
root = tk.Tk()
from tkinter import messagebox
root.title("Smart Student Performance Prediction System")
root.geometry("400x400")
def submit():
    first = entry_first.get()
    last = entry_last.get()
    messagebox.showinfo("Submitted")

# Heading1
heading1 = tk.Label(root, text="SMART STUDENT PERFORMANCE PREDICTION SYSTEM",
                   font=("Arial", 14, "bold"))
heading1.grid(row=0, column=8, columnspan=2, pady=10)

# Heading2
heading2 = tk.Label(root, text="Student Information",
                   font=("Arial", 12, "bold"))
heading2.grid(row=1, column=3, columnspan=2, pady=10)

# First Name
tk.Label(root, text="Student ID",font=("Arial", 12)).grid(row=2, column=3, padx=10, pady=5, sticky="w")
entry_first = tk.Entry(root, width=30)
entry_first.grid(row=2, column=4, padx=10, pady=5)

# Last Name
tk.Label(root, text="Name",font=("Arial", 12)).grid(row=3, column=3, padx=10, pady=5, sticky="w")
entry_last = tk.Entry(root, width=30)
entry_last.grid(row=3, column=4, padx=10, pady=5)

# Heading2

heading3 = tk.Label(root, text="Academic Information",
                   font=("Arial", 12, "bold"))
heading3.grid(row=1, column=15, columnspan=2, pady=10)

# First Name
tk.Label(root, text="Attendance",font=("Arial", 12)).grid(row=2, column=14, padx=10, pady=5, sticky="w")
entry_first = tk.Entry(root, width=30)
entry_first.grid(row=2, column=15, padx=10, pady=5)

# Last Name
tk.Label(root, text="Study Hours",font=("Arial", 12)).grid(row=3, column=14, padx=10, pady=5, sticky="w")
entry_last = tk.Entry(root, width=30)
entry_last.grid(row=3, column=15, padx=10, pady=5)
# First Name
tk.Label(root, text="Internal Marks",font=("Arial", 12)).grid(row=4, column=14, padx=10, pady=5, sticky="w")
entry_first = tk.Entry(root, width=30)
entry_first.grid(row=4, column=15, padx=10, pady=5)

# Last Name
tk.Label(root, text="Assignment Completion",font=("Arial", 12)).grid(row=5, column=14, padx=10, pady=5, sticky="w")
entry_last = tk.Entry(root, width=30)
entry_last.grid(row=5, column=15, padx=10, pady=5)
# First Name
tk.Label(root, text="Previous Performance",font=("Arial", 12)).grid(row=6, column=14, padx=10, pady=5, sticky="w")
entry_first = tk.Entry(root, width=30)
entry_first.grid(row=6, column=15, padx=10, pady=5)

# Button
submit_btn = tk.Button(root, text="Predict Performance", command=submit,bg="blue",fg="white")
submit_btn.grid(row=9, column=6, columnspan=2, pady=15)

# Button
submit_btn = tk.Button(root, text="Clear", command=submit,bg="green",fg="white")
submit_btn.grid(row=9, column=8, columnspan=2, pady=15)
# Button
submit_btn = tk.Button(root, text="Exit", command=submit,bg="red",fg="white")
submit_btn.grid(row=9, column=10, columnspan=2, pady=15)

heading2 = tk.Label(root, text="Predicted Result",
                   font=("Arial", 12, "bold"))
heading2.grid(row=11, column=8, columnspan=2, pady=10)

# Output Box (Label)

output_label = tk.Label(root, text="Prediction:", font=("Arial", 12), fg="black", justify="left")
output_label.grid(row=12, column=8, columnspan=2, pady=10)

output_label = tk.Label(root, text="Risk Level:", font=("Arial", 12), fg="black", justify="left")
output_label.grid(row=13, column=8, columnspan=2, pady=10)

output_label = tk.Label(root, text="Recommendation:", font=("Arial", 12), fg="black", justify="left")
output_label.grid(row=14, column=8, columnspan=2, pady=10)

root.mainloop()