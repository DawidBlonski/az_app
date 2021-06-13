import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = bool(int(os.getenv("MAIL_USE_TLS")))
app.config["MAIL_USE_SSL"] = bool(int(os.getenv("MAIL_USE_SSL")))

mail = Mail(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/galery")
def gallery():
    return render_template("gallery.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        subject = request.form.get("subject")
        messange = request.form.get("messange")
        sender = request.form.get("sender")
        recipients = request.form.get("recipients")
        if all([subject, messange, sender, recipients]):
            msg = Message(subject, sender=sender, recipients=[recipients])
            msg.body = messange
            mail.send(msg)
            return render_template("contact.html", status=f"Email sent to {recipients}")
        else:
            render_template("contact.html", status=f"Please fill out the form")

    return render_template("contact.html")
