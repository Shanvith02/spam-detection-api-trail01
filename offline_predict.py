import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model and vectorizer
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_spam(message):
    """Function to predict spam messages offline"""
    message_vectorized = vectorizer.transform([message])
    prediction = model.predict(message_vectorized)
    return "Spam" if prediction[0] == 1 else "Ham"

# Test the offline model
if __name__ == "__main__":
    user_input = input("Enter a message: ")
    result = predict_spam(user_input)
    print(f"Prediction: {result}")
