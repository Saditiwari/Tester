from flask import Flask, flash, redirect, url_for, render_template, session
from flask import request

from flask_sqlalchemy import SQLAlchemy

DB_HOST = "localhost"
DB_NAME = "new_schema"
DB_USERNAME = "root"
DB_Password = "12345"

database_file = f"mysql+pymysql://{DB_USERNAME}:{DB_Password}@{DB_HOST}:3306/{DB_NAME}"

app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Sandwich(db.Model):
    __tablename__ = 'sandwiches'
    id = db.Column(db.Integer, primary_key=True)
    sandwich_size = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, sandwich_size, price):
        self.sandwich_size = sandwich_size
        self.price = price



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/sandwich")
def sandwich():
    sandwiches = Sandwich.query.all()
    return render_template("sandwiches/list.html", sandwiches=sandwiches)


@app.route('/addsandwich', methods=['GET', 'POST'])
def add_sandwich():
    if request.method == 'POST':
        if not request.form['item'] or not request.form['amount']:
            flash('Please enter all the fields', 'error')
        else:
            sandwich = Sandwich(request.form['item'], request.form['amount'])

            db.session.add(resource)
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('sandwich'))
    return render_template("sandwiches/add.html")


@app.route('/updatesandwich/<int:id>/', methods=['GET', 'POST'])
def update_sandwich(id):
    if request.method == 'POST':
        if not request.form['item'] or not request.form['amount']:
            flash('Please enter all the fields', 'error')
        else:
            sandwich = Sandwich.query.filter_by(id=id).first()
            sandwich.item = request.form['item']
            sandwich.amount = request.form['amount']
            db.session.commit()

            flash('Record was successfully updated')
            return redirect(url_for('resource'))
    sandwich = Sandwich.query.filter_by(id=id).first()
    return render_template("sandwiches/update.html", sandwich=sandwich)

@app.route('/deletesandwich/<int:id>/', methods=['GET', 'POST'])
def delete_sandwich(id):
    if request.method == 'POST':
        sandwich = Sandwich.query.filter_by(id=id).first()
        db.session.delete(sandwich)
        db.session.commit()

        flash('Record was successfully deleted')
        return redirect(url_for('sandwich'))
    return render_template("sandwiches/delete.html", sandwich=sandwich)

if __name__ == '__main__':
    app.run(port=3001, host="localhost", debug=True)



