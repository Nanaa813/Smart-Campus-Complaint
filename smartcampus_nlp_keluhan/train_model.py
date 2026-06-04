import pandas as pd
import joblib
import re
import string
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

DATA_PATH = Path("data_keluhan_dummy.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

def train_target(df, target_col, model_name):
    X = df["keluhan_bersih"]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    candidates = {
        "Naive Bayes": MultinomialNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Linear SVM": LinearSVC(),
        "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42)
    }

    results = []
    best_pipeline = None
    best_score = -1
    best_name = ""

    for name, clf in candidates.items():
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("model", clf)
        ])

        pipeline.fit(X_train, y_train)
        pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, pred)

        results.append({
            "target": target_col,
            "algorithm": name,
            "accuracy": round(acc, 4)
        })

        if acc > best_score:
            best_score = acc
            best_pipeline = pipeline
            best_name = name
            best_pred = pred
            best_y_test = y_test

    joblib.dump(best_pipeline, MODEL_DIR / model_name)

    print(f"\n=== Target: {target_col} ===")
    print(f"Best model: {best_name}")
    print(f"Accuracy: {best_score:.4f}")
    print("\nClassification report:")
    print(classification_report(best_y_test, best_pred))
    print("Confusion matrix:")
    print(confusion_matrix(best_y_test, best_pred))

    return results

def main():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["keluhan", "kategori", "prioritas"])
    df["keluhan_bersih"] = df["keluhan"].apply(clean_text)

    result_kategori = train_target(df, "kategori", "model_kategori.joblib")
    result_prioritas = train_target(df, "prioritas", "model_prioritas.joblib")

    result_df = pd.DataFrame(result_kategori + result_prioritas)
    result_df.to_csv("hasil_evaluasi_model.csv", index=False)
    print("\nHasil evaluasi disimpan ke hasil_evaluasi_model.csv")
    print("Model disimpan di folder models/")

if __name__ == "__main__":
    main()
