from flask import Flask, request, jsonify  
import pickle  
import requests  
from sklearn.feature_extraction.text import TfidfVectorizer  

app = Flask(__name__)  

# 🔹 Load the trained spam detection model and vectorizer
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# 🔹 Have I Been Pwned API Key (Replace with your actual API key)
HIBP_API_KEY = "your_api_key_here"  # Get an API key from https://haveibeenpwned.com/

# 🔹 Define Sample Lists for Number-Based Categorization
CONTACTS = {"+919876543210", "+917665443210","8790151102"}  # Sample personal contacts
BANK_NUMBERS = {"+18005551234", "+16505559999"}  # Sample bank numbers
EDUCATIONAL_NUMBERS = {"+914001234567"}  # Sample college/school numbers

def check_dark_web(email):
    """Check if an email has been leaked on the dark web."""
    if email == "test@example.com":
        print("✅ DEBUG: Forcing high-risk spam for test@example.com")
        return True  

    try:
        headers = {"hibp-api-key": HIBP_API_KEY}
        response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=headers)
        print(f"✅ DEBUG: Checking email: {email}")
        print(f"✅ DEBUG: Response Status Code: {response.status_code}")

        return response.status_code == 200  # True if breached, False otherwise

    except Exception as e:
        print(f"⚠️ DEBUG: API Error: {str(e)}")
        return False


def categorize_sms(sender):
    """Categorize messages based on sender's phone number."""
    if sender in CONTACTS:
        return "Personal"
    elif sender in BANK_NUMBERS:
        return "Bank Alert"
    elif sender in EDUCATIONAL_NUMBERS:
        return "Educational"
    else:
        return "Unknown"


@app.route("/predict", methods=["POST"])
def predict():
    """Classify SMS messages and categorize them based on sender."""
    try:
        data = request.get_json()

        if "message" not in data:
            return jsonify({"error": "Missing 'message' key in request"}), 400

        message = [data["message"]]
        sender = data.get("sender", "")  
        email_or_phone = data.get("email", "")  

        # 🔹 Categorize SMS based on sender
        category = categorize_sms(sender)
        prediction = None  

        # 🔹 If sender is known, return only category
        if category != "Unknown":
            response = {"message": message[0], "category": category}
        else:
            # 🔹 Perform spam detection for unknown senders
            message_vectorized = vectorizer.transform(message)
            prediction = "Spam" if model.predict(message_vectorized)[0] == 1 else "Ham"

            # 🔹 Check for Dark Web leaks
            if email_or_phone and check_dark_web(email_or_phone):
                prediction = "High-Risk Spam (Leaked Email/Phone Found)"

            response = {"message": message[0], "category": category, "prediction": prediction}

        print(f"✅ DEBUG: Final Response: {response}")  # Debugging
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
