from enum import unique
import json
import re
from time import sleep
from flask import Flask, flash, jsonify, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sqlite3

f = open("secrets.json")
db_creds = json.load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_creds['DATABASEURI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=db_creds['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['SECRET_KEY'] = db_creds['DATABASESECRETKEY']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.app_context().push()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class LicensePlate(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(80))
    phone = db.Column(db.String(10), nullable=False)
    platenumber = db.Column(db.String(10), nullable=False, unique=True)
    isdeleted = db.Column(db.String(5), nullable=False)

class RegisterForm(FlaskForm):
    print("inclass")
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Username"})

    email = EmailField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password", "pattern":"[a-zA-Z0-9]*[!#$%&][a-zA-Z0-9]*"})
    passwordcfm = PasswordField( validators=[
        InputRequired(), Length(min=8, max=20)
    ], render_kw={"placeholder": "Confirm Password"})

    Phone_no= StringField(validators=[
                           InputRequired(), Length(min=10, max=10)], render_kw={"placeholder": "Phone Number"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')



class LoginForm(FlaskForm):

    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


# ---------------------------------------------------------------------------------------------------------------------------


@app.route('/', methods=['GET', 'POST'])
def login_1():
    form = LoginForm()
    print(form.username.data)
    print(form.password.data)

    # if form.validate_on_submit():
    if request.method == "POST":
        print(form.username.data)

        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                sleep(1.0)
                return redirect(url_for('add1'))
            else:
                msg="Incorrect Password"
                return render_template('login_1.html', form=form, msg = msg)
        else:
            msg="Incorrect"
            return render_template('login_1.html', form=form, msg = msg)
    return render_template('login_1.html', form=form, msg = "")

@app.route('/register1', methods=['GET','POST'])
def register1():
    form = RegisterForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        if form.password.data == form.passwordcfm.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            print(new_user.username)
            try:
                db.session.add(new_user)
                db.session.commit()
                print("REGISTERED")
                #Regestered flashing message
                sleep(0.5)
                return redirect(url_for('login_1'))
            except Exception as e:
                print("in except")
                print(e)
                return render_template('register1.html', form=form, msg="Already Present")
        else:
             return render_template('register1.html', form=form, msg="Password not matched")   

    return render_template('register1.html', form=form, msg="")
            

# ---------------------------------------------------------------------------------------------------------------------------


@app.route("/add")  
@login_required
def add():  
    print("in add")
    con = sqlite3.connect("licenseplate.db")  
    cur = con.cursor()  
    cur.execute("select * from LicensePlate")  
    rows = cur.fetchall()  
    print(rows)
    return render_template("add.html", rows=rows)

@app.route("/add1")  
@login_required
def add1():  
    print("in add1")
    rows = LicensePlate.query.filter_by().all()
    print(rows)
    return render_template("add.html", rows=rows)
 

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_1'))


@app.route("/savedetails",methods = ["POST"])  
def saveDetails():  
    print("11111111111111")
    msg = ""  
    if request.method == "POST":  
        try: 
            name=request.form['Name']
            address=request.form['Address']
            phone=request.form['Phone Number']
            platenumber=request.form['licenseplate']
            with sqlite3.connect("licenseplate.db") as con:
                cur = con.cursor()  
                cur.execute("INSERT into LicensePlate (name, address, phone, platenumber, isdeleted) values (?,?,?,?, 0)",(name,address,phone,platenumber))  
                con.commit()  
                msg = "Employee successfully Added"  
                # return render_template("add.html", rows=rows)  
        except:  
            con.rollback()  
            msg = "We can not add the employee to the list"  
        finally:   
            con = sqlite3.connect("licenseplate.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from LicensePlate")
            rows = cur.fetchall()
            return render_template("add.html",msg = msg,rows=rows)
            con.close()
      

@app.route("/savedetails1",methods = ["POST"])  
def saveDetails1():  
    print("11111111111111")
    msg = ""  
    if request.method == "POST":  
        try: 
            name=request.form['Name']
            address=request.form['Address']
            phone=request.form['Phone Number']
            platenumber=request.form['licenseplate']
            new_record = LicensePlate(name=name, address=address, phone=phone, platenumber=platenumber, isdeleted='0')
            db.session.add(new_record)
        except:  
            msg = "We can not add the employee to the list"  
        finally:   
            db.session.commit()
            return redirect(url_for("add1"))
       

@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    platenumber = request.json['platenumber']
    print(platenumber)
    with sqlite3.connect("licenseplate.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("UPDATE LicensePlate SET isdeleted = 1 WHERE platenumber = ?",[platenumber])  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
            
@app.route("/deleterecord1",methods = ["POST"])  
def deleterecord1():  
    platenumber = request.json['platenumber']
    print(platenumber)
    try:  
        db.session.query(LicensePlate).filter(LicensePlate.platenumber == platenumber).update({LicensePlate.isdeleted: '1'}, synchronize_session=False)
        msg = "record successfully deleted" 
    except:  
        msg = "can't be deleted"  
    finally:
        db.session.commit()
        return {"msg": msg}
            
  


@app.route("/restore")
def restore():
    with sqlite3.connect("licenseplate.db") as con:
        cur = con.cursor()
        msg = ''
        try:
            cur.execute("UPDATE LicensePlate SET isdeleted = 0 WHERE isdeleted = 1")
            msg = "Restored all records"
        except Exception as e:
            print(e)
        finally:
            con = sqlite3.connect("licenseplate.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from LicensePlate")
            rows = cur.fetchall()
            return render_template("add.html",msg = msg,rows=rows)
            con.close()
@app.route("/restore1")
def restore1():
    with sqlite3.connect("licenseplate.db") as con:
        cur = con.cursor()
        msg = ''
        try:
            db.session.query(LicensePlate).filter(LicensePlate.isdeleted == '1').update({LicensePlate.isdeleted: '0'}, synchronize_session=False)
            msg = "Restored all records"
        except Exception as e:
            print(e)
        finally:
            db.session.commit()
            return render_template("add.html")
            


@app.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    a = db.session.query(LicensePlate).distinct(LicensePlate.address).all()
    print("Distinct",a[0])
    return render_template('analytics.html')

@app.route('/analytics_data', methods=['GET','POST'])
def analytics_data():
    con = sqlite3.connect("licenseplate.db")
    cur = con.cursor()
    cur.execute("select distinct address from LicensePlate")
    address = cur.fetchall()
    print(address)
    print(len(address))
    data_list=[]
    for i in range(len(address)):
        print(address[i][0])
        cur.execute("select count(platenumber) from LicensePlate where address='{}'".format(address[i][0]))
        count_v=cur.fetchone() 
        data = {}
        data['label'] = address[i][0]
        data['y'] = count_v[0]
        json_data = json.dumps(data)
        data_list.append(json_data)
    return jsonify(data_list)




@app.route("/update",methods = ["POST","GET"])
def update():
    msg = "msg"
    if request.method == "POST":
        print("INSIDE TRY OF UPDATE")
        name=request.form['Name']
        address=request.form['Address']
        phone=request.form['Phone Number']
        platenumber=request.form['licenseplate']
        query = "UPDATE LicensePlate SET "
        data = {"name":name, "address":address, "phone":phone}
        for i in data:
            if data[i]:
                query+= f"{i} = '{data[i]}', "
        query = query[0:-2:1]
        query+= f" where platenumber = '{platenumber}'"
        print(query)
        try: 
            with sqlite3.connect("licenseplate.db") as con:
                cur = con.cursor() 
                # cur.execute("UPDATE LicensePlate SET name = ?, address = ?, phone = ? WHERE  platenumber = ?",(name,address,phone,platenumber))
                cur.execute(query)
                con.commit()
                msg = "Patient record updated"
        except Exception as e: 
            print(e)
            con.rollback()
            msg = "We can not update the Patient to the list"
        finally:
            con = sqlite3.connect("licenseplate.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from LicensePlate")
            rows = cur.fetchall()
            return render_template("add.html",msg = msg,rows=rows)
            con.close()
    return render_template("add.html")


@app.route("/update1",methods = ["POST","GET"])
def update1():
    msg = "msg"
    if request.method == "POST":
        print("INSIDE TRY OF UPDATE")
        name=request.form['Name']
        address=request.form['Address']
        phone=request.form['Phone Number']
        platenumber=request.form['licenseplate']
        query = {}
        data = {LicensePlate.name :name, LicensePlate.address:address, LicensePlate.phone:phone}
        for i in data:
            if data[i]:
                query[i] = data[i]
        print(query)
        try: 
            ds = platenumber.split()
            for plate in ds:
                db.session.query(LicensePlate).filter(LicensePlate.platenumber == plate).update(query, synchronize_session = False)
            msg = "Patient record updated"
        except Exception as e: 
            print(e)
            msg = "We can not update the Patient to the list"
        finally:
            db.session.commit()
            rows = LicensePlate.query.filter_by().all()
            return redirect(url_for("add1"))

@app.route("/search", methods=["POST"])
def search():
    name=request.form['Name']
    address=request.form['Address']
    phone=request.form['Phone Number']
    platenumber=request.form['licenseplate']
    try:
        with sqlite3.connect("licenseplate.db") as conn:
            cur = conn.cursor()
            cur.execute(f"select * from LicensePlate where (name like '{name}%' and address like '{address}%' and phone like '{phone}%' and platenumber like '{platenumber}%')")
            rows = cur.fetchall()
            print("11111111111111111111111",rows)
            msg = "Search complete"
            return render_template("add.html", rows=rows)
    except Exception as e:
        print(e)
        msg = "Search Unsuccessful"

@app.route("/search1", methods=["POST"])
def search1():
    name="%"+request.form['Name']+"%" if request.form['Name'] else "%"  
    address="%"+request.form['Address']+"%" if request.form['Address'] else "%"
    phone="%"+request.form['Phone Number']+"%" if request.form['Phone Number'] else "%"
    platenumber="%"+request.form['licenseplate']+"%" if request.form['licenseplate'] else "%"
    try:
        rows = db.session.query(LicensePlate).filter(
            LicensePlate.name.like(name),
            LicensePlate.address.like(address),
            LicensePlate.phone.like(phone),
            LicensePlate.platenumber.like(platenumber)
        ).all()
        msg = "Search complete"
        print(rows)
        return render_template("add.html", rows=rows)
    except Exception as e:
        print(e)
        msg = "Search Unsuccessful"
    return render_template("add.html", msg=msg,rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
