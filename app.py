import pickle
import pandas as pd
import re
import nltk
from flask import Flask, request, jsonify
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load trained model and vectorizer
with open("spam_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Initialize Flask app
app = Flask(__name__)

# Text Cleaning Function
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]  # Lemmatization
    return ' '.join(words)

# Route for detecting spam messages
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        message = data['message']
        
        # Clean and preprocess the message
        cleaned_message = clean_text(message)
        
        # Convert message to TF-IDF features
        message_vec = vectorizer.transform([cleaned_message])
        
        # Predict spam or ham
        prediction = model.predict(message_vec)[0]
        
        # Return result
        result = {'message': message, 'prediction': 'Spam' if prediction == 1 else 'Ham'}
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

