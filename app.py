from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# FastAPI Backend URL
FASTAPI_URL = "http://127.0.0.1:8000/code"

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    
    if request.method == "POST":
        input_text = request.form["input_text"]
        task = request.form["task"]

        # Send request to FastAPI backend
        api_response = requests.post(FASTAPI_URL, json={"input_text": input_text, "task": task})

        if api_response.status_code == 200:
            response_text = api_response.text  # Use raw text instead of JSON
        else:
            response_text = "Error: " + api_response.text

    return render_template("index.html", response_text=response_text)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
