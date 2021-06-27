import os

from dotenv import load_dotenv
from flask import Flask, render_template, request,redirect,url_for
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
from flask_mail import Mail, Message
from database import AzureDB
load_dotenv()

app = Flask(__name__)
app.debug = True
app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
github_blueprint = make_github_blueprint(
    client_id=f"{os.getenv('CLIENT_ID')}",
    client_secret=f"{os.getenv('CLIENT_SECRET')}",
)
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = bool(int(os.getenv("MAIL_USE_TLS")))
app.config["MAIL_USE_SSL"] = bool(int(os.getenv("MAIL_USE_SSL")))
app.register_blueprint(github_blueprint, url_prefix='/login')

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


@app.route('/guestbook',methods=['GET','POST'])
def guestbook():
    with AzureDB() as db:
        if request.method == 'POST':
            name = request.form.get('Name')
            comment = request.form.get('Comments')
            db.azureAddData(name,comment)
        data = db.azureGetData()
        return render_template("guestbook.html",data=data)

@app.route('/login')
def github_login():
    if not github.authorized:
        return redirect(url_for('github_login'))
    else:
        account_info = github.get('/user')
    if account_info.ok:
        return redirect(url_for('guestbook'))

    return '<h1>Request failed!</h1>'
if __name__ == '__main__':
    app.debug = True
    app.run()