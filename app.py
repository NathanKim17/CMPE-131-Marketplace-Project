from flask import Flask, flash, url_for, render_template, request, redirect, session
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
        
class User_new(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), unique=True)
    newpassword = db.Column(db.String(80))

    def __init__(self, password, newpassword):
        self.password = password
        self.newpassword = newpassword
        
#card update payment class
class update_payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    cardnumber = db.Column(db.String(80), unique = True)
    expire = db.Column(db.String(80), unique = True)
    cvv = db.Column(db.String(80), unique = True)

    def __init__(self, name, cardnumber, expire, cvv):
        self.name = name
        self.cardnumber = cardnumber
        self.expire = expire
        self.cvv = cvv 

#Item Class
#class Item(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80))
    #idNumber = db.Column(db.String(80), unique=True)
    #price = db.Column(db.Float(80))
    
    # def __init__(self, name, idNumber, price):
    #     self.name = name
    #     self.idNumber = idNumber
    #     self.price = price

    #def __repr__(self):
        #return f'<Item: {self.name}'

class Item2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(80))

    def init(self, name, price):
        self.name = name
        self.price = price


# newItem = Item2(name = 'Coke', price = 1.50)
# db.session.add(newItem)
# db.session.commit()


itemsList = []
itemsList.append(Item2(name = 'Coke', price = 1.50))
db.session.add(itemsList[0])
db.session.commit()

itemsList.append(Item2(name = 'Yoyo', price = 1.75))
db.session.add(itemsList[1])
db.session.commit()

itemsList.append(Item2(name = "Jar", price = 0.50))
db.session.add(itemsList[2])
db.session.commit()

itemsList.append(Item2(name = "Soccer Ball", price = 50.00))
db.session.add(itemsList[3])
db.session.commit()


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
    if request.method == 'POST':
        new_password = User_new(
            password=request.form['password'],
            newpassword=request.form['newpassword'])
        db.session.add(new_password)
        db.session.commit()
        flash('Your password has been updated!')
        return render_template('index.html')
    return render_template('changepassword.html')

@app.route("/updatepayment", methods=['GET', 'POST'])
def updatepayment():
    if request.method == 'POST':
        updatepayment = update_payment(
            name = request.form['name'],
            cardnumber = request.form['cardnumber'],
            expire = request.form['expire'],
            cvv = request.form['cvv'])
        db.session.add(updatepayment)
        db.session.commit()
        flash('Your payment has been updated!')
        return render_template('index.html')
    return render_template('updatepayment.html')

@app.route("/browse")
def browse() :
    #itemOne = Item("Cool Aid", "011223", 1.23)
    # itemsList = []
    # itemsList.append(Item2(name = 'Coke', price = 1.50))
    # itemsList.append(Item2(name = 'Yoyo', price = 1.75))
    # itemsList.append(Item2(name = "Jar", price = 0.50))
    # itemsList.append(Item2(name = "Soccer Ball", price = 50.00))

    #itemId = Item2.query.get(1)
    #iName = Item2.query.get(itemId).name
    #iPrice = Item2.query.get(itemId).price
    #iName = "Nathan"
    #iPrice = "Bao"
    #nI = Item2(name = itemName, price = itemPrice)
    # itemsList.append(nI)
    return render_template('browse.html', list = itemsList)

@app.route('/iI/<int:id>', methods=['GET', 'POST'])
def itemPage(id):
    itemId = Item2.query.get(id)
    iName = Item2.query.get(id).name
    iPrice = Item2.query.get(id).price

    print(itemId)

    return render_template('itemInfo.html', itemName = iName, itemPrice = iPrice)
#@app.route("/itemInfo")
#def itemInfo :
    #return render_template('intemInfo.html', item)
if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
