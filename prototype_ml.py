import tkinter as tk
from tkinter import messagebox
import csv
import os
import pickle
from pathlib import Path

# ONE CSV FILE:
# - Initially contains your 300 labeled training records.
# - New UI records are appended to the same file.
# - After saving a new record, the model is retrained using the same CSV.

BASE_DIR = Path(__file__).resolve().parent
DATASET_FILE = BASE_DIR / "student_performance_dataset_ml_300.csv"
MODEL_FILE = BASE_DIR / "student_performance_model.pkl"

model = None


def load_model():
    global model

    try:
        with open(MODEL_FILE, "rb") as file:
            model = pickle.load(file)
        return True

    except FileNotFoundError:
        messagebox.showerror(
            "Model Missing",
            "student_performance_model.pkl was not found.\n\n"
            "Run this command first:\n"
            "python train_model.py"
        )
        return False


def save_record_to_csv(
    student_id,
    name,
    attendance,
    study_hours,
    internal_marks,
    assignment,
    previous_performance,
    prediction,
    risk,
    recommendation
):
    # The CSV already contains the 300 training rows.
    # This function only APPENDS the new UI record.
    file_exists = DATASET_FILE.exists()

    with open(
        DATASET_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # If the CSV is empty, create its header.
        if not file_exists or DATASET_FILE.stat().st_size == 0:
            writer.writerow([
                "Student ID",
                "Name",
                "Attendance",
                "Study Hours",
                "Internal Mark",
                "Assignment Completion",
                "Previous Performance",
                "Prediction",
                "Risk Level",
                "Recommendation"
            ])

        writer.writerow([
            student_id,
            name,
            attendance,
            study_hours,
            internal_marks,
            assignment,
            previous_performance,
            prediction,
            risk,
            recommendation
        ])


def retrain_model():
    """
    Retrain the same ML model using the SAME CSV file after
    a new UI record has been appended.
    """
    global model

    try:
        from train_model import train_and_save_model

        model, accuracy = train_and_save_model()
        return True, accuracy

    except Exception as error:
        return False, str(error)


def submit():
    student_id = entry_student_id.get().strip()
    name = entry_name.get().strip()

    attendance_text = entry_attendance.get().strip()
    study_hours_text = entry_study_hours.get().strip()
    internal_marks_text = entry_internal_marks.get().strip()
    assignment_text = entry_assignment.get().strip()
    previous_performance_text = entry_previous_performance.get().strip()

    # Check empty fields
    if not all([
        student_id,
        name,
        attendance_text,
        study_hours_text,
        internal_marks_text,
        assignment_text,
        previous_performance_text
    ]):
        messagebox.showerror(
            "Error",
            "Please enter all student details."
        )
        return

    if model is None:
        if not load_model():
            return

    try:
        attendance = float(attendance_text)
        study_hours = float(study_hours_text)
        internal_marks = float(internal_marks_text)
        assignment = float(assignment_text)
        previous_performance = float(previous_performance_text)

        # Validation
        if not (0 <= attendance <= 100):
            messagebox.showerror(
                "Error",
                "Attendance must be between 0 and 100."
            )
            return

        if not (1 <= study_hours <= 8):
            messagebox.showerror(
                "Error",
                "Study Hours must be between 1 and 8."
            )
            return

        if not (0 <= internal_marks <= 100):
            messagebox.showerror(
                "Error",
                "Internal Marks must be between 0 and 100."
            )
            return

        if not (0 <= assignment <= 100):
            messagebox.showerror(
                "Error",
                "Assignment Completion must be between 0 and 100."
            )
            return

        if not (0 <= previous_performance <= 100):
            messagebox.showerror(
                "Error",
                "Previous Performance must be between 0 and 100."
            )
            return

        # ==========================================================
        # ML PREDICTION
        # ==========================================================

        model_input = [[
            attendance,
            study_hours,
            internal_marks,
            assignment,
            previous_performance
        ]]

        prediction = str(model.predict(model_input)[0]).upper()

        # Optional confidence
        confidence = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(model_input)[0]
            confidence = max(probabilities) * 100

        # ==========================================================
        # RESULT INFORMATION
        # ==========================================================

        risk_map = {
            "EXCELLENT": "VERY LOW",
            "GOOD": "LOW",
            "AVERAGE": "MEDIUM",
            "AT RISK": "HIGH"
        }

        recommendation_map = {
            "EXCELLENT":
                "Maintain your current study pattern and continue regular practice.",

            "GOOD":
                "Maintain attendance and continue regular study.",

            "AVERAGE":
                "Increase study hours and improve assignment completion.",

            "AT RISK":
                "Improve attendance, study hours, and assignment completion."
        }

        risk = risk_map.get(prediction, "UNKNOWN")

        recommendation = recommendation_map.get(
            prediction,
            "Review the student's academic performance."
        )

        # ==========================================================
        # SAVE UI DATA INTO THE SAME CSV
        # ==========================================================

        save_record_to_csv(
            student_id,
            name,
            attendance,
            study_hours,
            internal_marks,
            assignment,
            previous_performance,
            prediction,
            risk,
            recommendation
        )

        # ==========================================================
        # RETRAIN USING THE SAME CSV
        # ==========================================================

        retrained, result = retrain_model()

        # ==========================================================
        # DISPLAY RESULT
        # ==========================================================

        prediction_text = f"Prediction: {prediction}"

        if confidence is not None:
            prediction_text += (
                f"\nConfidence: {confidence:.2f}%"
            )

        output_prediction.config(
            text=prediction_text
        )

        output_risk.config(
            text=f"Risk Level: {risk}"
        )

        output_recommendation.config(
            text=f"Recommendation: {recommendation}"
        )

        if retrained:
            messagebox.showinfo(
                "Success",
                "Student data saved to the CSV.\n\n"
                "The ML model was also retrained using the updated CSV."
            )
        else:
            messagebox.showwarning(
                "Saved",
                "Student data was saved, but model retraining failed:\n\n"
                + str(result)
            )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numeric values."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"An unexpected error occurred:\n{error}"
        )


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


# ==============================================================
# MAIN WINDOW
# ==============================================================

root = tk.Tk()
root.title("Smart Student Performance Prediction System")
root.geometry("900x650")


# Heading
heading1 = tk.Label(
    root,
    text="SMART STUDENT PERFORMANCE PREDICTION SYSTEM",
    font=("Arial", 25, "bold")
)
heading1.grid(
    row=0,
    column=0,
    columnspan=8,
    pady=20
)


# Student Information
heading2 = tk.Label(
    root,
    text="Student Information",
    font=("Arial", 14, "bold")
)
heading2.grid(
    row=1,
    column=1,
    columnspan=4,
    pady=10
)


# Student ID
tk.Label(
    root,
    text="Student ID",
    font=("Arial", 12)
).grid(
    row=2,
    column=1,
    padx=10,
    pady=5,
    sticky="w"
)

entry_student_id = tk.Entry(
    root,
    width=30
)
entry_student_id.grid(
    row=2,
    column=2,
    padx=10,
    pady=5
)


# Name
tk.Label(
    root,
    text="Name",
    font=("Arial", 12)
).grid(
    row=3,
    column=1,
    padx=10,
    pady=5,
    sticky="w"
)

entry_name = tk.Entry(
    root,
    width=30
)
entry_name.grid(
    row=3,
    column=2,
    padx=10,
    pady=5
)


# Academic Information
heading3 = tk.Label(
    root,
    text="Academic Information",
    font=("Arial", 14, "bold")
)
heading3.grid(
    row=1,
    column=6,
    columnspan=4,
    pady=10
)


# Attendance
tk.Label(
    root,
    text="Attendance",
    font=("Arial", 12)
).grid(
    row=2,
    column=6,
    padx=10,
    pady=5,
    sticky="w"
)

entry_attendance = tk.Entry(
    root,
    width=30
)
entry_attendance.grid(
    row=2,
    column=7,
    padx=10,
    pady=5
)


# Study Hours
tk.Label(
    root,
    text="Study Hours",
    font=("Arial", 12)
).grid(
    row=3,
    column=6,
    padx=10,
    pady=5,
    sticky="w"
)

entry_study_hours = tk.Entry(
    root,
    width=30
)
entry_study_hours.grid(
    row=3,
    column=7,
    padx=10,
    pady=5
)


# Internal Marks
tk.Label(
    root,
    text="Internal Marks",
    font=("Arial", 12)
).grid(
    row=4,
    column=6,
    padx=10,
    pady=5,
    sticky="w"
)

entry_internal_marks = tk.Entry(
    root,
    width=30
)
entry_internal_marks.grid(
    row=4,
    column=7,
    padx=10,
    pady=5
)


# Assignment Completion
tk.Label(
    root,
    text="Assignment Completion",
    font=("Arial", 12)
).grid(
    row=5,
    column=6,
    padx=10,
    pady=5,
    sticky="w"
)

entry_assignment = tk.Entry(
    root,
    width=30
)
entry_assignment.grid(
    row=5,
    column=7,
    padx=10,
    pady=5
)


# Previous Performance
tk.Label(
    root,
    text="Previous Performance",
    font=("Arial", 12)
).grid(
    row=6,
    column=6,
    padx=10,
    pady=5,
    sticky="w"
)

entry_previous_performance = tk.Entry(
    root,
    width=30
)
entry_previous_performance.grid(
    row=6,
    column=7,
    padx=10,
    pady=5
)


# Buttons
submit_btn = tk.Button(
    root,
    text="Predict Performance",
    command=submit,
    bg="blue",
    fg="white",
    font=("Arial", 11, "bold")
)
submit_btn.grid(
    row=8,
    column=1,
    columnspan=2,
    pady=20
)


clear_btn = tk.Button(
    root,
    text="Clear",
    command=clear,
    bg="green",
    fg="white",
    font=("Arial", 11, "bold")
)
clear_btn.grid(
    row=8,
    column=6,
    pady=20
)


exit_btn = tk.Button(
    root,
    text="Exit",
    command=exit_app,
    bg="red",
    fg="white",
    font=("Arial", 11, "bold")
)
exit_btn.grid(
    row=8,
    column=7,
    pady=20
)


# Predicted Result
heading4 = tk.Label(
    root,
    text="Predicted Result",
    font=("Arial", 14, "bold")
)
heading4.grid(
    row=10,
    column=0,
    columnspan=8,
    pady=10
)


output_prediction = tk.Label(
    root,
    text="Prediction:",
    font=("Arial", 12),
    justify="left"
)
output_prediction.grid(
    row=11,
    column=0,
    columnspan=8,
    pady=5
)


output_risk = tk.Label(
    root,
    text="Risk Level:",
    font=("Arial", 12),
    justify="left"
)
output_risk.grid(
    row=12,
    column=0,
    columnspan=8,
    pady=5
)


output_recommendation = tk.Label(
    root,
    text="Recommendation:",
    font=("Arial", 12),
    justify="left",
    wraplength=800
)
output_recommendation.grid(
    row=13,
    column=0,
    columnspan=8,
    pady=5
)


# Load model before starting UI
if not load_model():
    root.destroy()
else:
    root.mainloop()
