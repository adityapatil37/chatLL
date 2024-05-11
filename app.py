from flask import Flask, render_template, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from datetime import datetime
import generator

app = Flask(__name__)
app.secret_key = "Seal_tod"
bcrypt = Bcrypt(app)
client = MongoClient("mongodb://localhost:27017/")
db = client["Med"]

# MongoDB models
users_collection = db["users"]
messages_collection = db["messages"]

# Routes
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if username or email already exists
        if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
            return render_template("signup.html", error="Username or email already exists.")

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert user into the database
        users_collection.insert_one({"username": username, "email": email, "password": hashed_password})

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user exists
        user = users_collection.find_one({"username": username})
        if user and bcrypt.check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))

    chat_history = list(messages_collection.find({"$or": [{"sender": session["username"]}, {"recipient": session["username"]}]}))

    return render_template("chat.html", chat_history=chat_history)

@app.route("/send_message", methods=["POST"])
def send_message():
    if "username" not in session:
        return redirect(url_for("login"))

    message = request.form["message"]
    recipient = "chatll"  # Assuming "chatll" is the recipient (the machine)

    # Extract chat history for the user
    chat_history = list(messages_collection.find({"$or": [{"sender": session["username"]}, {"recipient": session["username"]}]}))

    # Prepare the prompt for generating reply
    prompt_for_generating_reply = ""
    for index in range(-5, 0, 2):
        if abs(index) > len(chat_history):
            break  # Avoid index out of range error
        user_message = chat_history[index]["message"]
        bot_message = chat_history[index + 1]["message"]
        next_prompt = f"<s>[INST] {user_message} [\\INST] {bot_message} <\\s>"
        prompt_for_generating_reply += next_prompt

    # If no chat history found, prompt with user's current message only
    if not chat_history:
        prompt_for_generating_reply = f"<s>[INST] {message} [\\INST]"

    # Generate reply based on the prompt
    reply = generator.generate_reply(prompt_for_generating_reply)

    # Insert user's message into the database
    messages_collection.insert_one({"sender": session["username"], "recipient": recipient, "message": message, "timestamp": datetime.now()})

    # Insert machine's reply into the database
    messages_collection.insert_one({"sender": recipient, "recipient": session["username"], "message": reply, "timestamp": datetime.now()})

    return redirect(url_for("chat"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
