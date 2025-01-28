from flask import Flask, render_template, request, redirect
from helper import preprocessing, vectorizer, get_prediction
from logger import logging

app = Flask(__name__)

logging.info("Flask server started")#take configurations from logger

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

    logging.info("=======Open home page=======")

    return render_template("index.html", data=data)

@app.route("/", methods=['post'])
def my_post():
    text = request.form['text']  # Handle missing 'text' key gracefully
    logging.info(f'Text : {text}')

    preprocessed_txt = preprocessing(text)
    logging.info(f'Preprocessed_txt  : { preprocessed_txt }')

    vectorized_txt = vectorizer(preprocessed_txt)
    logging.info(f'Vectorized_txt  : {vectorized_txt}')

    prediction = get_prediction(vectorized_txt)
    logging.info(f'Prediction : {prediction}') 

    global positive, negative  # Declare as global to modify
    if prediction == 'negative':
        negative += 1
    else:
        positive += 1

    reviews.insert(0, text)  # Add the new review to the top
    return redirect("/")  # Redirect to the index route

if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for better error messages
