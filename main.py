from flask import Flask, render_template, request, redirect
import requests, re, smtplib

g_password = "________________" #paslepts drosibas pasverumu del

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():
    passed_recaptcha = check_passed_captcha(request.form.get("g-recaptcha-response"))
    email_verified = verify_email(request.form.get("email"))

    if passed_recaptcha:
        if email_verified:
            msg = f"\n\n{request.form.get('name')} with the email {request.form.get('email')} wanted to send you this: {request.form.get('message')}"
            print(msg)
            send_email("rihardam20@gmail.com", g_password, msg)
        else:
            return "<h1> Nav ievadīts pareizs e-pasts<h1><br><a href='/'>atgriezties</a>"
    else:
        return "<h1> Neizdevās captcha, mēģiniet vēlreiz!<h1><br><a href='/'>atgriezties</a>"
    
    return redirect('/')

def check_passed_captcha(g_recaptcha_response):
    req = requests.post("https://www.google.com/recaptcha/api/siteverify", data={"response": g_recaptcha_response, "secret":"6LfSz2gqAAAAANkI2Ts6pjkK4uJxDCwwruDZxYXO"})
    resp = req.json()
    passed = resp.get("success")

    return passed
def verify_email(email):
    if re.search(r'^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
        return True
    else:
        return False

def send_email(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, 'rihardam20@gmail.com', msg)
    server.quit()

if __name__ == "__main__":
    app.run()
