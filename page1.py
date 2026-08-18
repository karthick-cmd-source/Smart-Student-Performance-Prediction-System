import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Smart Student Performance Prediction System")
root.geometry("900x650")


def submit():
    student_id = entry_student_id.get()
    name = entry_name.get()
    attendance = entry_attendance.get()
    study_hours = entry_study_hours.get()
    internal_marks = entry_internal_marks.get()
    assignment = entry_assignment.get()
    previous_performance = entry_previous_performance.get()

    if not student_id or not name or not attendance or not study_hours or not internal_marks or not assignment or not previous_performance:
        messagebox.showerror("Error", "Please enter all student details.")
        return

    try:
        attendance = float(attendance)
        study_hours = float(study_hours)
        internal_marks = float(internal_marks)
        assignment = float(assignment)
        previous_performance = float(previous_performance)

        if not (0 <= attendance <= 100):
            messagebox.showerror("Error", "Attendance must be between 0 and 100.")
            return

        if not (0 <= study_hours <= 24):
            messagebox.showerror("Error", "Study Hours must be between 0 and 24.")
            return

        if not (0 <= internal_marks <= 100):
            messagebox.showerror("Error", "Internal Marks must be between 0 and 100.")
            return

        if not (0 <= assignment <= 100):
            messagebox.showerror("Error", "Assignment Completion must be between 0 and 100.")
            return

        if not (0 <= previous_performance <= 100):
            messagebox.showerror("Error", "Previous Performance must be between 0 and 100.")
            return

        study_hours_score = min((study_hours / 8) * 100, 100)

        performance_score = (
            attendance * 0.20
            + study_hours_score * 0.20
            + internal_marks * 0.40
            + assignment * 0.20
        )

        final_score = (
            performance_score * 0.80
            + previous_performance * 0.20
        )

        if final_score >= 80:
            performance = "EXCELLENT"
            risk = "LOW"
            recommendation = "Maintain your current study pattern and continue regular practice."

        elif final_score >= 65:
            performance = "GOOD"
            risk = "LOW"
            recommendation = "Maintain attendance and continue regular study."

        elif final_score >= 50:
            performance = "AVERAGE"
            risk = "MEDIUM"
            recommendation = "Increase study hours and improve assignment completion."

        else:
            performance = "AT RISK"
            risk = "HIGH"
            recommendation = "Improve attendance, study hours, and assignment completion."

        output_prediction.config(
            text=f"Prediction: {performance}\nPerformance Score: {final_score:.2f}"
        )

        output_risk.config(
            text=f"Risk Level: {risk}"
        )

        output_recommendation.config(
            text=f"Recommendation: {recommendation}"
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")


def clear():
    entry_student_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_attendance.delete(0, tk.END)
    entry_study_hours.delete(0, tk.END)
    entry_internal_marks.delete(0, tk.END)
    entry_assignment.delete(0, tk.END)
    entry_previous_performance.delete(0, tk.END)

    output_prediction.config(text="Prediction:")
    output_risk.config(text="Risk Level:")
    output_recommendation.config(text="Recommendation:")


def exit_app():
    root.destroy()


# Heading1
heading1 = tk.Label(
    root,
    text="SMART STUDENT PERFORMANCE PREDICTION SYSTEM",
    font=("Arial", 25, "bold")
)
heading1.grid(row=0, column=0, columnspan=8, pady=20)


# Heading2
heading2 = tk.Label(
    root,
    text="Student Information",
    font=("Arial", 14, "bold")
)
heading2.grid(row=1, column=1, columnspan=4, pady=10)


# Student ID
tk.Label(
    root,
    text="Student ID",
    font=("Arial", 12)
).grid(row=2, column=1, padx=10, pady=5, sticky="w")

entry_student_id = tk.Entry(root, width=30)
entry_student_id.grid(row=2, column=2, padx=10, pady=5)


# Name
tk.Label(
    root,
    text="Name",
    font=("Arial", 12)
).grid(row=3, column=1, padx=10, pady=5, sticky="w")

entry_name = tk.Entry(root, width=30)
entry_name.grid(row=3, column=2, padx=10, pady=5)


# Academic Information
heading3 = tk.Label(
    root,
    text="Academic Information",
    font=("Arial", 14, "bold")
)
heading3.grid(row=1, column=6, columnspan=4, pady=10)


# Attendance
tk.Label(
    root,
    text="Attendance",
    font=("Arial", 12)
).grid(row=2, column=6, padx=10, pady=5, sticky="w")

entry_attendance = tk.Entry(root, width=30)
entry_attendance.grid(row=2, column=7, padx=10, pady=5)


# Study Hours
tk.Label(
    root,
    text="Study Hours",
    font=("Arial", 12)
).grid(row=3, column=6, padx=10, pady=5, sticky="w")

entry_study_hours = tk.Entry(root, width=30)
entry_study_hours.grid(row=3, column=7, padx=10, pady=5)


# Internal Marks
tk.Label(
    root,
    text="Internal Marks",
    font=("Arial", 12)
).grid(row=4, column=6, padx=10, pady=5, sticky="w")

entry_internal_marks = tk.Entry(root, width=30)
entry_internal_marks.grid(row=4, column=7, padx=10, pady=5)


# Assignment Completion
tk.Label(
    root,
    text="Assignment Completion",
    font=("Arial", 12)
).grid(row=5, column=6, padx=10, pady=5, sticky="w")

entry_assignment = tk.Entry(root, width=30)
entry_assignment.grid(row=5, column=7, padx=10, pady=5)


# Previous Performance
tk.Label(
    root,
    text="Previous Performance",
    font=("Arial", 12)
).grid(row=6, column=6, padx=10, pady=5, sticky="w")

entry_previous_performance = tk.Entry(root, width=30)
entry_previous_performance.grid(row=6, column=7, padx=10, pady=5)


# Buttons
submit_btn = tk.Button(
    root,
    text="Predict Performance",
    command=submit,
    bg="blue",
    fg="white",
    font=("Arial", 11, "bold")
)
submit_btn.grid(row=8, column=1, columnspan=2, pady=20)


clear_btn = tk.Button(
    root,
    text="Clear",
    command=clear,
    bg="green",
    fg="white",
    font=("Arial", 11, "bold")
)
clear_btn.grid(row=8, column=6, columnspan=1, pady=20)


exit_btn = tk.Button(
    root,
    text="Exit",
    command=exit_app,
    bg="red",
    fg="white",
    font=("Arial", 11, "bold")
)
exit_btn.grid(row=8, column=7, columnspan=1, pady=20)


# Predicted Result
heading4 = tk.Label(
    root,
    text="Predicted Result",
    font=("Arial", 14, "bold")
)
heading4.grid(row=10, column=0, columnspan=8, pady=10)


# Output
output_prediction = tk.Label(
    root,
    text="Prediction:",
    font=("Arial", 12),
    fg="black",
    justify="left"
)
output_prediction.grid(row=11, column=0, columnspan=8, pady=5)


output_risk = tk.Label(
    root,
    text="Risk Level:",
    font=("Arial", 12),
    fg="black",
    justify="left"
)
output_risk.grid(row=12, column=0, columnspan=8, pady=5)


output_recommendation = tk.Label(
    root,
    text="Recommendation:",
    font=("Arial", 12),
    fg="black",
    justify="left",
    wraplength=800
)
output_recommendation.grid(row=13, column=0, columnspan=8, pady=5)


root.mainloop()
