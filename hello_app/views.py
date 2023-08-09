from datetime import datetime
from flask import Flask, render_template, request, jsonify
from .gpt import process_prompt
from . import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.put("/sessions/<session>")
def create_session(session = None):
    return render_template(
        "hello_there.html",
        name="session",
        date=datetime.now()
    )

@app.post("/completions/execute")
def execute_completion():
    payload = request.get_json()
    message = payload.get("message")
    return jsonify({"message": process_prompt(message)})

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
