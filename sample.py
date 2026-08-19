# Smart Student Performance Prediction System
# Day 1 Prototype

print("==============================================")
print("  SMART STUDENT PERFORMANCE PREDICTION SYSTEM")
print("==============================================")

# Get student details
student_name = input("Enter Student Name: ")

attendance = float(input("Enter Attendance (%): "))

study_hours = float(input("Enter Study Hours per Day: "))

internal_marks = float(input("Enter Internal Marks (%): "))

assignment_completion = float(
    input("Enter Assignment Completion (%): ")
)

# Convert study hours into a score
study_hours_score = min((study_hours / 8) * 100, 100)

# Calculate performance score
performance_score = (
    attendance * 0.20
    + study_hours_score * 0.20
    + internal_marks * 0.40
    + assignment_completion * 0.20
)

# Determine performance level
if performance_score >= 80:
    performance_level = "EXCELLENT"

elif performance_score >= 65:
    performance_level = "GOOD"

elif performance_score >= 50:
    performance_level = "AVERAGE"

else:
    performance_level = "AT RISK"

# Generate recommendation
if performance_level == "EXCELLENT":
    recommendation = (
        "Excellent performance. Maintain your current study "
        "pattern and continue regular practice."
    )

elif performance_level == "GOOD":
    recommendation = (
        "Maintain attendance and continue regular study."
    )

elif performance_level == "AVERAGE":
    recommendation = (
        "Increase study hours, improve assignment completion, "
        "and focus on internal assessments."
    )

else:
    recommendation = (
        "Improve attendance, increase study hours, complete "
        "assignments regularly, and seek academic guidance."
    )

# Display result
print("\n==============================================")
print("          STUDENT PERFORMANCE RESULT")
print("==============================================")

print("Student Name:", student_name)
print("Performance Score:", round(performance_score, 2))
print("Performance Level:", performance_level)
print("Recommendation:", recommendation)

print("==============================================")