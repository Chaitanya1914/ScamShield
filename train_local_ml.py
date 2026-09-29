import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import os

print("🚀 Initializing Local ML Model Training...")

# 1. Load the Dataset
csv_path = "India_Cyber_Scam_Hinglish_Dataset.csv"
if not os.path.exists(csv_path):
    print(f"Error: Dataset not found at {csv_path}")
    exit()

print("📊 Loading dataset...")
df = pd.read_csv(csv_path)

# Drop any empty rows
df = df.dropna(subset=['text', 'label'])

X = df['text']
y = df['label'] # 0 for safe, 1 for scam

print(f"✅ Loaded {len(df)} messages for training.")

# 2. Build the Machine Learning Pipeline (TF-IDF + Naive Bayes)
# TF-IDF converts the Hinglish text into numerical vectors
# MultinomialNB is a classic algorithm for text classification (spam detection)
model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), max_df=0.9, min_df=2),
    MultinomialNB()
)

print("🧠 Training the local ML model...")
model.fit(X, y)

# 3. Evaluate basic accuracy on training data
accuracy = model.score(X, y)
print(f"🎯 Model Training Complete! Accuracy on dataset: {accuracy * 100:.2f}%")

# 4. Save the model to disk so it can be used offline without Gemini
joblib_file = "local_scam_model.pkl"
joblib.dump(model, joblib_file)
print(f"💾 Model saved successfully as '{joblib_file}'.")
print("\nYou can now proudly tell the judges: 'We trained our own local TF-IDF Naive Bayes classifier!'")
