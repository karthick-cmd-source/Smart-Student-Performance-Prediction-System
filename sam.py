import tkinter as tk
from tkinter import messagebox


# ============================================================
# Smart Student Performance Prediction System
# Day 2 - Tkinter Prototype
# ============================================================


# ------------------------------------------------------------
# Function: Validate percentage
# ------------------------------------------------------------
def get_percentage(value, field_name):
    try:
        number = float(value)

        if number < 0 or number > 100:
            messagebox.showerror(
                "Invalid Input",
                f"{field_name} must be between 0 and 100."
            )
            return None

        return number

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            f"Please enter a valid number for {field_name}."
        )
        return None


# ------------------------------------------------------------
# Function: Validate study hours
# ------------------------------------------------------------
def get_study_hours(value):
    try:
        number = float(value)

        if number < 0 or number > 24:
            messagebox.showerror(
                "Invalid Input",
                "Study hours must be between 0 and 24."
            )
            return None

        return number

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number for Study Hours."
        )
        return None


# ------------------------------------------------------------
# Function: Predict Performance
# ------------------------------------------------------------
def predict_performance():

    # Get student information
    student_id = entry_student_id.get().strip()
    student_name = entry_student_name.get().strip()

    # Check Student ID
    if not student_id:
        messagebox.showerror(
            "Missing Information",
            "Please enter Student ID."
        )
        return

    # Check Student Name
    if not student_name:
        messagebox.showerror(
            "Missing Information",
            "Please enter Student Name."
        )
        return

    # Get Attendance
    attendance = get_percentage(
        entry_attendance.get(),
        "Attendance"
    )

    if attendance is None:
        return

    # Get Study Hours
    study_hours = get_study_hours(
        entry_study_hours.get()
    )

    if study_hours is None:
        return

    # Get Internal Marks
    internal_marks = get_percentage(
        entry_internal_marks.get(),
        "Internal Marks"
    )

    if internal_marks is None:
        return

    # Get Assignment Completion
    assignment_completion = get_percentage(
        entry_assignment.get(),
        "Assignment Completion"
    )

    if assignment_completion is None:
        return

    # Get Previous Performance
    previous_performance = get_percentage(
        entry_previous_performance.get(),
        "Previous Performance"
    )

    if previous_performance is None:
        return

    # --------------------------------------------------------
    # Convert Study Hours into score
    # 8 hours/day = 100 score
    # --------------------------------------------------------
    study_hours_score = min((study_hours / 8) * 100, 100)

    # --------------------------------------------------------
    # Calculate performance score
    # --------------------------------------------------------
    performance_score = (
        attendance * 0.20
        + study_hours_score * 0.20
        + internal_marks * 0.40
        + assignment_completion * 0.20
    )

    # Include previous performance for additional assessment
    final_score = (
        performance_score * 0.80
        + previous_performance * 0.20
    )

    # --------------------------------------------------------
    # Determine performance category
    # --------------------------------------------------------
    if final_score >= 80:
        performance_level = "EXCELLENT"
        risk_level = "LOW"

        recommendation = (
            "Excellent performance. Maintain your current "
            "study pattern and continue regular practice."
        )

    elif final_score >= 65:
        performance_level = "GOOD"
        risk_level = "LOW"

        recommendation = (
            "Maintain attendance and continue regular study."
        )

    elif final_score >= 50:
        performance_level = "AVERAGE"
        risk_level = "MEDIUM"

        recommendation = (
            "Increase study hours, improve assignment completion, "
            "and focus more on internal assessments."
        )

    else:
        performance_level = "AT RISK"
        risk_level = "HIGH"

        recommendation = (
            "Improve attendance, increase study hours, complete "
            "assignments regularly, and seek academic guidance."
        )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------
    result_text.set(
        f"Student: {student_name}\n"
        f"Performance Score: {final_score:.2f}\n"
        f"Performance Level: {performance_level}\n"
        f"Risk Level: {risk_level}\n"
        f"Recommendation: {recommendation}"
    )


# ------------------------------------------------------------
# Function: Clear all fields
# ------------------------------------------------------------
def clear_fields():

    entry_student_id.delete(0, tk.END)
    entry_student_name.delete(0, tk.END)
    entry_attendance.delete(0, tk.END)
    entry_study_hours.delete(0, tk.END)
    entry_internal_marks.delete(0, tk.END)
    entry_assignment.delete(0, tk.END)
    entry_previous_performance.delete(0, tk.END)

    result_text.set("")


# ------------------------------------------------------------
# Function: Exit application
# ------------------------------------------------------------
def exit_application():
    root.destroy()


# ============================================================
# Main Window
# ============================================================

root = tk.Tk()

root.title("Smart Student Performance Prediction System")

root.geometry("850x700")

root.minsize(700, 600)


# ============================================================
# Header Frame
# ============================================================

header_frame = tk.Frame(
    root,
    padx=10,
    pady=20
)

header_frame.pack(fill="x")


title_label = tk.Label(
    header_frame,
    text="Smart Student Performance Prediction System",
    font=("Arial", 24, "bold")
)

title_label.pack()


subtitle_label = tk.Label(
    header_frame,
    text="Student Performance Prediction - Day 2 Prototype",
    font=("Arial", 12)
)

subtitle_label.pack(pady=5)


# ============================================================
# Student Information Frame
# ============================================================

student_frame = tk.LabelFrame(
    root,
    text="Student Information",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=15
)

student_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


# Student ID
tk.Label(
    student_frame,
    text="Student ID:",
    font=("Arial", 11)
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

entry_student_id = tk.Entry(
    student_frame,
    font=("Arial", 11),
    width=30
)

entry_student_id.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# Student Name
tk.Label(
    student_frame,
    text="Student Name:",
    font=("Arial", 11)
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

entry_student_name = tk.Entry(
    student_frame,
    font=("Arial", 11),
    width=30
)

entry_student_name.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# Academic Information Frame
# ============================================================

academic_frame = tk.LabelFrame(
    root,
    text="Academic Information",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=15
)

academic_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


# Attendance
tk.Label(
    academic_frame,
    text="Attendance (%):",
    font=("Arial", 11)
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

entry_attendance = tk.Entry(
    academic_frame,
    font=("Arial", 11),
    width=30
)

entry_attendance.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# Study Hours
tk.Label(
    academic_frame,
    text="Study Hours/Day:",
    font=("Arial", 11)
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

entry_study_hours = tk.Entry(
    academic_frame,
    font=("Arial", 11),
    width=30
)

entry_study_hours.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# Internal Marks
tk.Label(
    academic_frame,
    text="Internal Marks (%):",
    font=("Arial", 11)
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

entry_internal_marks = tk.Entry(
    academic_frame,
    font=("Arial", 11),
    width=30
)

entry_internal_marks.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# Assignment Completion
tk.Label(
    academic_frame,
    text="Assignment Completion (%):",
    font=("Arial", 11)
).grid(
    row=3,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

entry_assignment = tk.Entry(
    academic_frame,
    font=("Arial", 11),
    width=30
)

entry_assignment.grid(
    row=3,
    column=1,
    padx=10,
    pady=8
)


# Previous Performance
tk.Label(
    academic_frame,
    text="Previous Performance (%):",
    font=("Arial", 11)
).grid(
    row=4,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

entry_previous_performance = tk.Entry(
    academic_frame,
    font=("Arial", 11),
    width=30
)

entry_previous_performance.grid(
    row=4,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# Action Frame
# ============================================================

action_frame = tk.Frame(
    root,
    pady=15
)

action_frame.pack()


predict_button = tk.Button(
    action_frame,
    text="Predict Performance",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=8,
    command=predict_performance
)

predict_button.grid(
    row=0,
    column=0,
    padx=10
)


clear_button = tk.Button(
    action_frame,
    text="Clear",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8,
    command=clear_fields
)

clear_button.grid(
    row=0,
    column=1,
    padx=10
)


exit_button = tk.Button(
    action_frame,
    text="Exit",
    font=("Arial", 12, "bold"),
    padx=25,
    pady=8,
    command=exit_application
)

exit_button.grid(
    row=0,
    column=2,
    padx=10
)


# ============================================================
# Result Frame
# ============================================================

result_frame = tk.LabelFrame(
    root,
    text="Prediction Result",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=15
)

result_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


result_text = tk.StringVar()

result_label = tk.Label(
    result_frame,
    textvariable=result_text,
    font=("Arial", 13),
    justify="left",
    anchor="nw",
    wraplength=750
)

result_label.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# Start Application
# ============================================================

root.mainloop()