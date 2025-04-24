from flask import Flask, Response, request, render_template
from collections import OrderedDict
import pickle
import re
import json

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Function to mask PII
def mask_pii(text):
    entities = []
    masked_text = text

    patterns = {
        "EMAIL": r'[\w\.-]+@[\w\.-]+',
        "PHONE": r'\b\d{10}\b',
        "NAME": r'\b([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,}){0,2})\b',
        "DOB": r'\b(?:\d{2}[/-]){2}\d{4}\b',
        "AADHAR_NUM": r'\b\d{4}\s\d{4}\s\d{4}\b',
        "CREDIT_DEBIT_NO": r'\b(?:\d[ -]*?){13,16}\b',
        "CVV_NO": r'\b\d{3}\b',
        "EXPIRY_NO": r'\b(0[1-9]|1[0-2])/\d{2}\b'
    }

    matches = []

    for label, pattern in patterns.items():
        for match in re.finditer(pattern, masked_text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "label": label,
                "text": match.group()
            })

    matches.sort(key=lambda m: m["start"], reverse=True)

    for idx, match in enumerate(matches):
        placeholder = f"[{match['label']}{idx}]"
        masked_text = masked_text[:match["start"]] + placeholder + masked_text[match["end"]:]
        entity = OrderedDict([
            ("position", [match["start"], match["start"] + len(placeholder)]),
            ("classification", match["label"]),
            ("entity", match["text"])
        ])
        entities.append(entity)

    return masked_text, list(reversed(entities))

# Prediction function
def get_prediction(text):
    if isinstance(text, (list, tuple)):
        text = text[0]
    X = vectorizer.transform([text])
    pred = model.predict(X)
    return str(pred[0])

@app.route('/', methods=['GET'])
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        email = request.form.get("input_email_body")
        masked_email, entities = mask_pii(email)
        category = get_prediction(masked_email)

        response_data = OrderedDict()
        response_data["input_email_body"] = email
        response_data["list_of_masked_entities"] = entities
        response_data["masked_email"] = masked_email
        response_data["category_of_the_email"] = category  # Placed at the end

        json_response = json.dumps(response_data, indent=2, sort_keys=False)
        return Response(json_response, mimetype='application/json')

    except Exception as e:
        error = OrderedDict([
            ("error", str(e))
        ])
        return Response(json.dumps(error), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
