from flask import Flask, render_template, request, redirect
from helper import preprocessing, vectorizer, get_prediction

app = Flask(__name__)

data = dict()
reviews = []
positive = 0
negative = 0  # Fixed syntax error

@app.route("/")
def index():
    # Populate data dictionary for the template
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative
    return render_template("index.html", data=data)

@app.route("/", methods=['post'])
def my_post():
    text = request.form['text']  # Handle missing 'text' key gracefully
    preprocessed_txt = preprocessing(text)
    vectorized_txt = vectorizer(preprocessed_txt)
    prediction = get_prediction(vectorized_txt)

    global positive, negative  # Declare as global to modify
    if prediction == 'negative':
        negative += 1
    else:
        positive += 1

    reviews.insert(0, text)  # Add the new review to the top
    return redirect("/")  # Redirect to the index route

if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for better error messages
