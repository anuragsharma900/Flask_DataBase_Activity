from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()



app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sahib@localhost/crud'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    student_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(100))
    amount_due = db.Column(db.Integer)

    def __init__(self, first_name, last_name, date_of_birth,amount_due):

        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.amount_due = amount_due


#This is the index route where we are going to
#query on all our student data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", students = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        amount_due = request.form['amount_due']

        my_data = Data(first_name, last_name, date_of_birth, amount_due)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")

        return redirect(url_for('Index'))


#this is our read and update route where we are going to read our student record
@app.route('/read', methods = ['GET', 'POST'])
def read():

    if request.method == 'POST':
        read_data = Data.query.get(request.form.get('read_id'))
        read_data.first_name = request.form['first_name']
        read_data.last_name = request.form['last_name']
        read_data.date_of_birth = request.form['date_of_birth']
        read_data.amount_due = request.form['amount_due']

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our student record
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('student_id'))

        my_data.first_name = request.form['first_name']
        my_data.last_name = request.form['last_name']
        my_data.date_of_birth = request.form['date_of_birth']
        my_data.amount_due = request.form['amount_due']

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our student
@app.route('/delete/<student_id>/', methods = ['GET', 'POST'])
def delete(student_id):
    my_data = Data.query.get(student_id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run(debug=True)