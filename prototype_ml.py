import tkinter as tk
from tkinter import messagebox
<<<<<<< HEAD
import pandas as pd
import joblib
import requests
from pathlib import Path


# ============================================================
# FILE PATHS
# ============================================================

BASE = Path(__file__).resolve().parent

CSV_FILE = BASE / "student_performance_dataset_ml_300.csv"
MODEL_FILE = BASE / "student_performance_model.pkl"


# ============================================================
# n8n CLOUD PRODUCTION WEBHOOK
# ============================================================

N8N_WEBHOOK_URL = "https://karthick-r.app.n8n.cloud/webhook/student-performance-prediction"


# ============================================================
# CALL n8n
# ============================================================

def call_n8n(
    name,
    email,
    student_id,
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    attendance,
    study_hours,
    internal_marks,
    assignment,
    previous_performance,
    prediction,
<<<<<<< HEAD
    risk
):

    payload = {
        "student_id": str(student_id),
        "name": str(name),
        "email": str(email),
        "attendance": float(attendance),
        "study_hours": int(study_hours),
        "internal_marks": float(internal_marks),
        "assignment_completion": float(assignment),
        "previous_performance": float(previous_performance),
        "prediction": str(prediction),
        "risk": str(risk)
    }

    try:

        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "n8n request timed out.\n"
            "Check whether the n8n workflow is active and Gemini is responding."
        )

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Could not connect to n8n Cloud.\n\n"
            "Check your internet connection and n8n Production URL."
        )

    except requests.exceptions.HTTPError as e:

        raise RuntimeError(
            f"n8n returned HTTP error:\n\n{e}\n\n"
            f"Response:\n{response.text}"
        )

    # --------------------------------------------------------
    # Read n8n response
    # --------------------------------------------------------

    try:
        result = response.json()

    except ValueError:

        raise RuntimeError(
            "n8n returned a non-JSON response.\n\n"
            f"Response:\n{response.text}"
        )

    # --------------------------------------------------------
    # Find recommendation
    # --------------------------------------------------------

    recommendation = ""

    # Direct response:
    # {"recommendation":"...."}

    if isinstance(result, dict):

        if result.get("recommendation"):
            recommendation = result["recommendation"]

        elif result.get("text"):
            recommendation = result["text"]

        elif result.get("output"):
            recommendation = result["output"]

        elif result.get("response"):
            recommendation = result["response"]

        # Gemini API style response
        elif result.get("candidates"):

            try:

                candidates = result["candidates"]

                if len(candidates) > 0:

                    candidate = candidates[0]

                    content = candidate.get("content", {})

                    parts = content.get("parts", [])

                    texts = []

                    for part in parts:

                        if part.get("text"):
                            texts.append(part["text"])

                    recommendation = " ".join(texts)

            except Exception:
                pass

        # n8n array response
        elif result.get("data"):

            data = result["data"]

            if isinstance(data, dict):

                recommendation = (
                    data.get("recommendation")
                    or data.get("text")
                    or data.get("output")
                    or ""
                )

    # --------------------------------------------------------
    # n8n may return an array
    # --------------------------------------------------------

    elif isinstance(result, list):

        if len(result) > 0:

            first = result[0]

            if isinstance(first, dict):

                recommendation = (
                    first.get("recommendation")
                    or first.get("text")
                    or first.get("output")
                    or ""
                )

                # Handle:
                # [{"json":{"recommendation":"..."}}]

                if not recommendation and isinstance(first.get("json"), dict):

                    recommendation = (
                        first["json"].get("recommendation")
                        or first["json"].get("text")
                        or first["json"].get("output")
                        or ""
                    )

    # --------------------------------------------------------
    # Clean recommendation
    # --------------------------------------------------------

    recommendation = str(recommendation).strip()

    if not recommendation:

        raise RuntimeError(
            "n8n did not return a recommendation.\n\n"
            "Check the 'Respond to Webhook' node."
        )

    return recommendation


# ============================================================
# SAVE DATA TO CSV
# ============================================================

def save_csv(values):

    row = pd.DataFrame([values])

    if CSV_FILE.exists():

        try:
            df = pd.read_csv(CSV_FILE)

        except Exception:

            df = pd.DataFrame()

        # Add missing columns
        for column in row.columns:

            if column not in df.columns:

                df[column] = ""

        # Make sure existing columns are also preserved
        for column in df.columns:

            if column not in row.columns:

                row[column] = ""

        # Same column order
        row = row[df.columns]

        df = pd.concat(
            [df, row],
            ignore_index=True
        )

    else:

        df = row

    df.to_csv(
        CSV_FILE,
        index=False
    )


# ============================================================
# PREDICTION
# ============================================================

def submit():

    try:

        # ----------------------------------------------------
        # Get values from UI
        # ----------------------------------------------------

        student_id = e_sid.get().strip()
        name = e_name.get().strip()
        email = e_email.get().strip()

        attendance = float(e_att.get())

        study_hours = round(
            float(e_study.get())
        )

        internal_marks = float(
            e_internal.get()
        )

        assignment = float(
            e_assign.get()
        )

        previous_performance = float(
            e_prev.get()
        )

        # ----------------------------------------------------
        # Required fields
        # ----------------------------------------------------

        if not student_id:

            raise ValueError(
                "Please enter Student ID."
            )

        if not name:

            raise ValueError(
                "Please enter Name."
            )

        if not email:

            raise ValueError(
                "Please enter Email."
            )

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        if not 0 <= attendance <= 100:

            raise ValueError(
                "Attendance must be between 0 and 100."
            )

        if not 1 <= study_hours <= 24:

            raise ValueError(
                "Study Hours must be between 1 and 24."
            )

        if not 0 <= internal_marks <= 100:

            raise ValueError(
                "Internal Marks must be between 0 and 100."
            )

        if not 0 <= assignment <= 100:

            raise ValueError(
                "Assignment Completion must be between 0 and 100."
            )

        if not 0 <= previous_performance <= 100:

            raise ValueError(
                "Previous Performance must be between 0 and 100."
            )

        # ----------------------------------------------------
        # Check model
        # ----------------------------------------------------

        if not MODEL_FILE.exists():

            raise ValueError(
                "ML model file not found.\n\n"
                "Run:\n"
                "python train_model.py"
            )

        # ----------------------------------------------------
        # Load trained ML model
        # ----------------------------------------------------

        model = joblib.load(
            MODEL_FILE
        )

        # ----------------------------------------------------
        # Prepare ML input
        # ----------------------------------------------------

        x = pd.DataFrame(
            [{
                "Attendance": attendance,
                "Study Hours": study_hours,
                "Internal Marks": internal_marks,
                "Assignment Completion": assignment,
                "Previous Performance": previous_performance
            }]
        )

        # ----------------------------------------------------
        # ML Prediction
        # ----------------------------------------------------

        prediction = str(
            model.predict(x)[0]
        ).upper()

        # ----------------------------------------------------
        # Risk Level
        # ----------------------------------------------------

        risk_map = {

            "EXCELLENT": "VERY LOW",

            "GOOD": "LOW",

            "AVERAGE": "MEDIUM",

            "AT RISK": "HIGH",

            "AT_RISK": "HIGH"
        }

        risk = risk_map.get(
            prediction,
            "MEDIUM"
        )

        # ----------------------------------------------------
        # Show prediction immediately
        # ----------------------------------------------------

        out_pred.config(
            text=f"Prediction: {prediction}"
        )

        out_risk.config(
            text=f"Risk Level: {risk}"
        )

        out_rec.config(
            text="AI Recommendation: Generating through Gemini..."
        )

        root.update_idletasks()

        # ----------------------------------------------------
        # Send data to n8n → Gemini → Gmail
        # ----------------------------------------------------

        recommendation = call_n8n(

            name=name,

            email=email,

            student_id=student_id,

            attendance=attendance,

            study_hours=study_hours,

            internal_marks=internal_marks,

            assignment=assignment,

            previous_performance=previous_performance,

            prediction=prediction,

            risk=risk
        )

        # ----------------------------------------------------
        # Display AI recommendation
        # ----------------------------------------------------

        out_rec.config(
            text=f"AI Recommendation: {recommendation}"
        )

        # ----------------------------------------------------
        # Save result to CSV
        # ----------------------------------------------------

        save_csv({

            "Student ID": student_id,

            "Name": name,

            "Email": email,

            "Attendance": attendance,

            "Study Hours": study_hours,

            "Internal Marks": internal_marks,

            "Assignment Completion": assignment,

            "Previous Performance": previous_performance,

            "Prediction": prediction,

            "Risk Level": risk,

            "Recommendation": recommendation
        })

        # ----------------------------------------------------
        # Success message
        # ----------------------------------------------------

        messagebox.showinfo(

            "Success",

            "Prediction completed successfully!\n\n"

            "ML Prediction: "
            + prediction
            + "\n\n"

            "Risk Level: "
            + risk
            + "\n\n"

            "Gemini AI recommendation generated.\n\n"

            "Recommendation email sent through n8n/Gmail.\n\n"

            "Student data saved to CSV."
        )

    # --------------------------------------------------------
    # Invalid numeric values
    # --------------------------------------------------------

    except ValueError as e:

        messagebox.showerror(
            "Input Error",
            str(e)
        )

    # --------------------------------------------------------
    # Other errors
    # --------------------------------------------------------

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ============================================================
# CLEAR
# ============================================================

def clear():

    entries = [

        e_sid,
        e_name,
        e_email,
        e_att,
        e_study,
        e_internal,
        e_assign,
        e_prev
    ]

    for entry in entries:

        entry.delete(
            0,
            tk.END
        )

    out_pred.config(
        text="Prediction:"
    )

    out_risk.config(
        text="Risk Level:"
    )

    out_rec.config(
        text="AI Recommendation:"
    )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Smart Student Performance Prediction System"
)

root.geometry(
    "1200x800"
)


# ============================================================
# MAIN HEADING
# ============================================================

tk.Label(

    root,

    text="SMART STUDENT PERFORMANCE PREDICTION SYSTEM",

    font=("Arial", 24, "bold")

).grid(

    row=0,

    column=0,

    columnspan=10,

=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    pady=20
)


<<<<<<< HEAD
# ============================================================
# STUDENT INFORMATION
# ============================================================

tk.Label(

    root,

    text="Student Information",

    font=("Arial", 14, "bold")

).grid(

    row=1,

    column=1,

    columnspan=3,

=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    pady=10
)


# Student ID
<<<<<<< HEAD

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

e_sid = tk.Entry(
    root,
    width=30
)

e_sid.grid(
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    row=2,
    column=2,
    padx=10,
    pady=5
)


# Name
<<<<<<< HEAD

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

e_name = tk.Entry(
    root,
    width=30
)

e_name.grid(
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    row=3,
    column=2,
    padx=10,
    pady=5
)


<<<<<<< HEAD
# Email

tk.Label(

    root,

    text="Email",

    font=("Arial", 12)

).grid(

    row=4,

    column=1,

    padx=10,

    pady=5,

    sticky="w"
)

e_email = tk.Entry(
    root,
    width=30
)

e_email.grid(
    row=4,
    column=2,
    padx=10,
    pady=5
)


# ============================================================
# ACADEMIC INFORMATION
# ============================================================

tk.Label(

    root,

    text="Academic Information",

    font=("Arial", 14, "bold")

).grid(

    row=1,

    column=6,

    columnspan=3,

=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    pady=10
)


# Attendance
<<<<<<< HEAD

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

e_att = tk.Entry(
    root,
    width=30
)

e_att.grid(
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    row=2,
    column=7,
    padx=10,
    pady=5
)


# Study Hours
<<<<<<< HEAD

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

e_study = tk.Entry(
    root,
    width=30
)

e_study.grid(
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    row=3,
    column=7,
    padx=10,
    pady=5
)


# Internal Marks
<<<<<<< HEAD

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

e_internal = tk.Entry(
    root,
    width=30
)

e_internal.grid(
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    row=4,
    column=7,
    padx=10,
    pady=5
)


# Assignment Completion
<<<<<<< HEAD

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

e_assign = tk.Entry(
    root,
    width=30
)

e_assign.grid(
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    row=5,
    column=7,
    padx=10,
    pady=5
)


# Previous Performance
<<<<<<< HEAD

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

e_prev = tk.Entry(
    root,
    width=30
)

e_prev.grid(
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    row=6,
    column=7,
    padx=10,
    pady=5
)


<<<<<<< HEAD
# ============================================================
# BUTTONS
# ============================================================

tk.Button(

    root,

    text="Predict Performance",

    command=submit,

    bg="blue",

    fg="white",

    font=("Arial", 11, "bold")

).grid(

    row=8,

    column=1,

    columnspan=2,

=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    pady=20
)


<<<<<<< HEAD
tk.Button(

    root,

    text="Clear",

    command=clear,

    bg="green",

    fg="white",

    font=("Arial", 11, "bold")

).grid(

    row=8,

    column=6,

=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    pady=20
)


<<<<<<< HEAD
tk.Button(

    root,

    text="Exit",

    command=root.destroy,

    bg="red",

    fg="white",

    font=("Arial", 11, "bold")

).grid(

    row=8,

    column=7,

=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    pady=20
)


<<<<<<< HEAD
# ============================================================
# PREDICTED RESULT
# ============================================================

tk.Label(

    root,

    text="Predicted Result",

    font=("Arial", 14, "bold")

).grid(

    row=10,

    column=0,

    columnspan=10,

=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
    pady=10
)


<<<<<<< HEAD
# Prediction

out_pred = tk.Label(

    root,

    text="Prediction:",

    font=("Arial", 12)

)

out_pred.grid(

    row=11,

    column=0,

    columnspan=10,

    pady=5
)


# Risk

out_risk = tk.Label(

    root,

    text="Risk Level:",

    font=("Arial", 12)

)

out_risk.grid(

    row=12,

    column=0,

    columnspan=10,

    pady=5
)


# AI Recommendation

out_rec = tk.Label(

    root,

    text="AI Recommendation:",

    font=("Arial", 12),

    wraplength=1050,

    justify="left"

)

out_rec.grid(

    row=13,

    column=0,

    columnspan=10,

    pady=10
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()
=======
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
>>>>>>> b3440ee6ff4b9bdc330f611408cecb92f28ebc19
