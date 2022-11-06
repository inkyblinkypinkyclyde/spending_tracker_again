from flask import Flask, render_template, request
# from flask_mail import Mail, Message

from controllers.accounts_controller import accounts_blueprint
from controllers.transactions_controller import transactions_blueprint
from controllers.merchants_controller import merchants_blueprint
from emailcredentials import email, password
import repositories.account_repository as account_repository
import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# mail = Mail(app)

app.register_blueprint(accounts_blueprint)
app.register_blueprint(transactions_blueprint)
app.register_blueprint(merchants_blueprint)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/send_mail/<account1>/<account2>/<amount>/<date>")
def send_mail(account1, account2, amount, date):
    msg = Message('Transfer reminder!', sender = 'yourbirdboxisoccupied@gmail.com', recipients = ['yourbirdboxisoccupied@gmail.com'])
    msg.body = f"Hi, remember to transfer {amount}p from {account1} into {account2} on {date} "
    mail.send(msg)
    return "Message sent!"
if __name__ == '__main__':
    app.run(debug=True)