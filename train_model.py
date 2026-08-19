import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATASET_FILE = "student_performance_dataset_ml_300.csv"
MODEL_FILE = "student_performance_model.pkl"

FEATURES = [
    "Attendance",
    "Study Hours",
    "Internal Mark",
    "Assignment Completion",
    "Previous Performance"
]

TARGET = "Prediction"


def main():
    # 1. Load dataset
    df = pd.read_csv(DATASET_FILE)

    # 2. Basic validation
    required_columns = FEATURES + [TARGET]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    df = df.dropna(subset=required_columns)

    # 3. Prepare input and target
    X = df[FEATURES]
    y = df[TARGET]

    print("Dataset shape:", df.shape)
    print("\nClass distribution:")
    print(y.value_counts())

    # This project requires four classes.
    required_classes = {"EXCELLENT", "GOOD", "AVERAGE", "AT RISK"}
    missing_classes = required_classes - set(y.unique())

    if missing_classes:
        raise ValueError(
            "The dataset does not contain all required classes: "
            + ", ".join(sorted(missing_classes))
            + ". Add training examples for these classes before training."
        )

    # 4. Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # 5. Create ML pipeline
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=2000))
    ])

    # 6. Train model
    model.fit(X_train, y_train)

    # 7. Evaluate model
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\nModel: Logistic Regression")
    print("Training rows:", len(X_train))
    print("Testing rows:", len(X_test))
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            labels=["EXCELLENT", "GOOD", "AVERAGE", "AT RISK"],
            zero_division=0
        )
    )

    print("Confusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            y_pred,
            labels=["EXCELLENT", "GOOD", "AVERAGE", "AT RISK"]
        )
    )

    # 8. Save trained model
    with open(MODEL_FILE, "wb") as file:
        pickle.dump(model, file)

    print(f"\nSaved trained model as: {MODEL_FILE}")


if __name__ == "__main__":
    main()
