# Import necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier  # Updated: Decision Tree
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle

# Load the dataset
df = pd.read_csv("combined_emails_with_natural_pii.csv")  

# Extract features and labels
X = df['email'].tolist()
y = df['type'].tolist()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorization using TF-IDF
vectorizer = TfidfVectorizer()  # Added stop words for improvement
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Initialize and train a Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train_vec, y_train)

# Evaluate accuracy on training data
train_preds = clf.predict(X_train_vec)
train_accuracy = accuracy_score(y_train, train_preds)
print("Training Accuracy:", train_accuracy)

# Evaluate accuracy on test data
test_preds = clf.predict(X_test_vec)
test_accuracy = accuracy_score(y_test, test_preds)
print("Testing Accuracy:", test_accuracy)

# Save model and vectorizer
pickle.dump(clf, open('model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))

# Optional: Load back for confirmation
loaded_model = pickle.load(open('model.pkl', 'rb'))
loaded_vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
