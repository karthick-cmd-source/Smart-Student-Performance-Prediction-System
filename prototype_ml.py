import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import pickle


MODEL_FILE = Path(__file__).with_name("student_performance_model.pkl")

# Load the trained ML model once when the application starts.
try:
    with open(MODEL_FILE, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    model = None


def submit():
    student_id = entry_student_id.get().strip()
    name = entry_name.get().strip()
    attendance_text = entry_attendance.get().strip()
    study_hours_text = entry_study_hours.get().strip()
    internal_marks_text = entry_internal_marks.get().strip()
    assignment_text = entry_assignment.get().strip()
    previous_performance_text = entry_previous_performance.get().strip()

    if not all([
        student_id,
        name,
        attendance_text,
        study_hours_text,
        internal_marks_text,
        assignment_text,
        previous_performance_text
    ]):
        messagebox.showerror("Error", "Please enter all student details.")
        return

    if model is None:
        messagebox.showerror(
            "Model Missing",
            "student_performance_model.pkl was not found.\n\n"
            "Run train_model.py first."
        )
        return

    try:
        attendance = float(attendance_text)
        study_hours = float(study_hours_text)
        internal_marks = float(internal_marks_text)
        assignment = float(assignment_text)
        previous_performance = float(previous_performance_text)

        if not (0 <= attendance <= 100):
            messagebox.showerror(
                "Error", "Attendance must be between 0 and 100."
            )
            return

        if not (1 <= study_hours <= 8):
            messagebox.showerror(
                "Error", "Study Hours must be between 1 and 8."
            )
            return

        if not (0 <= internal_marks <= 100):
            messagebox.showerror(
                "Error", "Internal Marks must be between 0 and 100."
            )
            return

        if not (0 <= assignment <= 100):
            messagebox.showerror(
                "Error", "Assignment Completion must be between 0 and 100."
            )
            return

        if not (0 <= previous_performance <= 100):
            messagebox.showerror(
                "Error", "Previous Performance must be between 0 and 100."
            )
            return

        # ML model input: exactly the five features used during training.
        model_input = [[
            attendance,
            study_hours,
            internal_marks,
            assignment,
            previous_performance
        ]]

        # ML prediction -- no rule-based performance thresholds here.
        prediction = model.predict(model_input)[0]

        # Optional model confidence.
        confidence = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(model_input)[0]
            confidence = max(probabilities) * 100

        # Risk and recommendation are mapped from the ML class.
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

        prediction_text = f"Prediction: {prediction}"

        if confidence is not None:
            prediction_text += f"\nConfidence: {confidence:.2f}%"

        output_prediction.config(text=prediction_text)
        output_risk.config(text=f"Risk Level: {risk}")
        output_recommendation.config(
            text=f"Recommendation: {recommendation}"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numeric values."
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


root = tk.Tk()
root.title("Smart Student Performance Prediction System")
root.geometry("900x650")


heading1 = tk.Label(
    root,
    text="SMART STUDENT PERFORMANCE PREDICTION SYSTEM",
    font=("Arial", 25, "bold")
)
heading1.grid(row=0, column=0, columnspan=8, pady=20)


heading2 = tk.Label(
    root,
    text="Student Information",
    font=("Arial", 14, "bold")
)
heading2.grid(row=1, column=1, columnspan=4, pady=10)


tk.Label(
    root,
    text="Student ID",
    font=("Arial", 12)
).grid(row=2, column=1, padx=10, pady=5, sticky="w")

entry_student_id = tk.Entry(root, width=30)
entry_student_id.grid(row=2, column=2, padx=10, pady=5)


tk.Label(
    root,
    text="Name",
    font=("Arial", 12)
).grid(row=3, column=1, padx=10, pady=5, sticky="w")

entry_name = tk.Entry(root, width=30)
entry_name.grid(row=3, column=2, padx=10, pady=5)


heading3 = tk.Label(
    root,
    text="Academic Information",
    font=("Arial", 14, "bold")
)
heading3.grid(row=1, column=6, columnspan=4, pady=10)


tk.Label(
    root,
    text="Attendance",
    font=("Arial", 12)
).grid(row=2, column=6, padx=10, pady=5, sticky="w")

entry_attendance = tk.Entry(root, width=30)
entry_attendance.grid(row=2, column=7, padx=10, pady=5)


tk.Label(
    root,
    text="Study Hours",
    font=("Arial", 12)
).grid(row=3, column=6, padx=10, pady=5, sticky="w")

entry_study_hours = tk.Entry(root, width=30)
entry_study_hours.grid(row=3, column=7, padx=10, pady=5)


tk.Label(
    root,
    text="Internal Marks",
    font=("Arial", 12)
).grid(row=4, column=6, padx=10, pady=5, sticky="w")

entry_internal_marks = tk.Entry(root, width=30)
entry_internal_marks.grid(row=4, column=7, padx=10, pady=5)


tk.Label(
    root,
    text="Assignment Completion",
    font=("Arial", 12)
).grid(row=5, column=6, padx=10, pady=5, sticky="w")

entry_assignment = tk.Entry(root, width=30)
entry_assignment.grid(row=5, column=7, padx=10, pady=5)


tk.Label(
    root,
    text="Previous Performance",
    font=("Arial", 12)
).grid(row=6, column=6, padx=10, pady=5, sticky="w")

entry_previous_performance = tk.Entry(root, width=30)
entry_previous_performance.grid(row=6, column=7, padx=10, pady=5)


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


heading4 = tk.Label(
    root,
    text="Predicted Result",
    font=("Arial", 14, "bold")
)
heading4.grid(row=10, column=0, columnspan=8, pady=10)


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
