import pandas as pd
import re
import nltk
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

nltk.download("stopwords")
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

# ---------------- CLEANING ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = " ".join(
        word for word in text.split()
        if word not in STOPWORDS and len(word) > 2
    )
    return text

# ---------------- LOAD DATA ----------------
df = pd.read_csv("../../dataset/UpdatedResumeDataSet.csv")
df["clean_resume"] = df["Resume"].apply(clean_text)

X = df["clean_resume"]
y = df["Category"]

# ---------------- VECTORIZE (CONTROLLED) ----------------
vectorizer = TfidfVectorizer(
    max_features=2000,        # 🔻 reduce memorization
    ngram_range=(1, 2),       # learn phrases, not just words
    min_df=3,                 # ignore rare words
    max_df=0.8                # ignore too common words
)

X_vec = vectorizer.fit_transform(X)

# ---------------- MODEL (STRONG REGULARIZATION) ----------------
model = LogisticRegression(
    max_iter=2000,
    C=0.5,
    solver="lbfgs"
)



# ---------------- CROSS VALIDATION ----------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_vec, y, cv=cv, scoring="accuracy")

print("Cross-validation accuracy:", scores)
print("Mean accuracy:", scores.mean())

# ---------------- FINAL TRAIN ----------------
model.fit(X_vec, y)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained with regularization and saved")
