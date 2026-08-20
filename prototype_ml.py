import tkinter as tk
from tkinter import messagebox
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
    attendance,
    study_hours,
    internal_marks,
    assignment,
    previous_performance,
    prediction,
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

    pady=20
)


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

e_sid = tk.Entry(
    root,
    width=30
)

e_sid.grid(
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

e_name = tk.Entry(
    root,
    width=30
)

e_name.grid(
    row=3,
    column=2,
    padx=10,
    pady=5
)


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

e_att = tk.Entry(
    root,
    width=30
)

e_att.grid(
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

e_study = tk.Entry(
    root,
    width=30
)

e_study.grid(
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

e_internal = tk.Entry(
    root,
    width=30
)

e_internal.grid(
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

e_assign = tk.Entry(
    root,
    width=30
)

e_assign.grid(
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

e_prev = tk.Entry(
    root,
    width=30
)

e_prev.grid(
    row=6,
    column=7,
    padx=10,
    pady=5
)


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

    pady=20
)


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

    pady=20
)


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

    pady=20
)


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

    pady=10
)


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