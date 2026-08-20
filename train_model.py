import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

DATASET_FILE = "student_performance_dataset_ml_300.csv"
MODEL_FILE = "student_performance_model.pkl"
FEATURES = ["Attendance","Study Hours","Internal Marks","Assignment Completion","Previous Performance"]
TARGET = "Prediction"

df = pd.read_csv(DATASET_FILE)
missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

for c in FEATURES:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df[TARGET] = df[TARGET].astype(str).str.strip().str.upper()
df = df.dropna(subset=FEATURES + [TARGET])

if len(df) < 20:
    raise ValueError("At least 20 valid training rows are required.")
if df[TARGET].nunique() < 2:
    raise ValueError("At least two Prediction classes are required.")

X, y = df[FEATURES], df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.20, random_state=42, stratify=y
)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=2000, random_state=42))
])
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Training rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")
print(f"Accuracy: {accuracy*100:.2f}%")
print(classification_report(y_test, y_pred, zero_division=0))

labels = sorted(y.unique())
disp = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred, labels=labels), display_labels=labels)
disp.plot(xticks_rotation=45)
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

with open("model_evaluation.txt","w",encoding="utf-8") as f:
    f.write("Smart Student Performance Prediction - Model Evaluation\n")
    f.write(f"Model: Logistic Regression\nTraining rows: {len(X_train)}\nTesting rows: {len(X_test)}\nAccuracy: {accuracy*100:.2f}%\n\n")
    f.write(classification_report(y_test, y_pred, zero_division=0))

joblib.dump(model, MODEL_FILE)
print(f"Model saved as {MODEL_FILE}")
