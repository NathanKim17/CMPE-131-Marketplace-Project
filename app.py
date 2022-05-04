from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#User Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
# class User_new(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     User.password = db.Column(db.String(80))
#     newpassword = db.Column(db.String(80), unique=True)
#
#     def __init__(self, password, newpassword):
#         self.password = password
#         self.newpassword = newpassword
        
#Item Class
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    idNumber = db.Column(db.String(80))
    price = db.Column(db.Float(80))
    
    def __init__(self, name, idNumber, price):
        self.name = name
        self.idNumber = idNumber
        self.price = price


class Item2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(80))

    def __init__(self, name, price):
        self.name = name
        self.price = price

newItem = Item2(name = 'Coke', price = 1.50)
db.session.add(newItem)
db.session.commit()

# new_Item = Item("Coke", "1234567890", 1.75)
@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        try:
            data = User.query.filter_by(username=username, password=password).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Incorrect Login'
        except:
            return "Not Logged In"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    session['logged_in'] = True
    User.query.filter_by(id=1).delete()
    db.session.commit()
    session['logged_in'] = False
    return render_template('index.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route("/accountdetails", methods=['GET', 'POST'])
def accountdetails():
     return render_template('accountdetails.html')
 
@app.route("/changepassword", methods=['GET', 'POST'])
def changepassword():
    if request.method =='POST':
        new_password = User_new(
            password = User.password,
            newpassword = request.form['newpassword'])
        db.session.delete(User.password)
        db.session.add(new_password)
        db.session.commit()
        return render_template('index.html')
    return render_template('changepassword.html')

@app.route("/updatepayment", methods=['GET', 'POST'])
def updatepayment():
    return render_template('updatepayment.html')

@app.route("/browse")
def browse() :
    #itemOne = Item("Cool Aid", "011223", 1.23)
    itemsList = []
    itemsList.append(Item("Cool Aid", "011223", 1.23))
    itemsList.append(Item("Coke", "32145", 10.99))
    itemsList.append(Item("Ice Cream", "8787", 0.50))
    itemsList.append(Item("Soccer Ball", "7777", 50.00))
    return render_template('browse.html', list = itemsList)

#@app.route("/itemInfo")
#def itemInfo :
    #return render_template('intemInfo.html', item)


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
