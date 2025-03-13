import pandas as pd
import re
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Step 1: Create a larger dataset
data = [
    ("spam", "Win a free iPhone now! Click here to claim your prize."),
    ("ham", "Hey, are we still meeting tomorrow?"),
    ("spam", "Congratulations! You have been selected for a $1000 gift card."),
    ("ham", "Let's catch up this weekend!"),
    ("spam", "URGENT: Your bank account is at risk. Verify now: fake-link.com"),
    ("ham", "Can you send me the project report?"),
    ("spam", "Exclusive offer! Buy 1 get 1 free on all products. Limited time only!"),
    ("ham", "Please call me when you're free."),
    ("spam", "You won a free trip to Dubai! Claim your ticket now."),
    ("ham", "Meeting is scheduled for 10 AM tomorrow."),
    ("spam", "Your PayPal account is on hold. Resolve now: phishing-link.com"),
    ("ham", "Did you complete your homework?"),
    ("spam", "Earn $500 daily from home! No experience required."),
    ("ham", "How was your weekend?"),
    ("spam", "Get 90% off on all purchases! Hurry, limited stock available."),
    ("ham", "Let's grab lunch today."),
    ("spam", "Click here to unlock unlimited Netflix for free!"),
    ("ham", "I will be late for the meeting."),
    ("spam", "Special offer! Get free mobile recharge now!"),
    ("ham", "Can you help me with this assignment?"),
    ("spam", "Lottery Winner: You have won $50,000! Claim now."),
    ("ham", "See you at the party tonight."),
    ("spam", "Congratulations! You are selected for a credit card with zero interest."),
    ("spam", "Your computer is infected with a virus! Click here to clean it."),
    ("ham", "Can we reschedule our appointment?"),
    ("spam", "Limited-time deal: Get 75% off on electronics!"),
    ("ham", "The weather is nice today."),
    ("spam", "Win a brand new Tesla! Enter your details now."),
    ("ham", "Let's go for a movie this weekend."),
    ("spam", "Verify your identity now to avoid bank suspension."),
]

# Convert the dataset into a DataFrame
df = pd.DataFrame(data, columns=["label", "message"])

# Convert labels to binary (Spam = 1, Ham = 0)
df['label'] = df['label'].map({'spam': 1, 'ham': 0})

# Text Cleaning Function
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]  # Lemmatization
    return ' '.join(words)

# Apply cleaning function to messages
df['message'] = df['message'].apply(clean_text)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.2, random_state=42)

# Convert text to numerical format using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train an SVM Classifier (more powerful than Naïve Bayes)
model = SVC(kernel='linear', probability=True)
model.fit(X_train_vec, y_train)

# Evaluate the model
accuracy = model.score(X_test_vec, y_test)
print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model and vectorizer
with open("spam_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print("✅ Model training completed and saved as spam_model.pkl and vectorizer.pkl")
