"""Server for fetch points app."""

from flask import Flask, render_template, flash, redirect, request
from jinja2 import StrictUndefined
from account import Account

user = Account()

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_transactions():
    """View all transactions."""

    return render_template("transaction.html", accounts=user._sort_transactions())


@app.route("/add_transaction", methods=['GET'])
def get_transaction():
    """Get list of transaction"""

    name = request.args.get('name')
    points = request.args.get('points')

    if name is not None and points is not None:
        user.add_transaction(name, points)

    return render_template("add_transaction.html")


@app.route("/spend")
def spend_points_transaction():
    """View all points spent."""

    spend = request.args.get('spend')

    if spend is not None:
        data = user.spend_points(int(spend)) 

    else:
        spend = 0
        data = None

    return render_template("spend_points.html", points_spent=data)


@app.route("/balance")
def balance():
    """View all balance."""

    return render_template("balance.html", balance=user.balance())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080" ,debug=True)