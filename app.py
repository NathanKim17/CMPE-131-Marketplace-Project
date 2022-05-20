from pdb import post_mortem
import sqlite3
from wsgiref.validate import validator
from flask import Flask, flash, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#These are for reading from the databases
connection = sqlite3.connect("test.db")
crsruser = connection.cursor()
crsrid = connection.cursor()
crsrreview = connection.cursor()

crsrid = connection.cursor()
crsrname = connection.cursor()
crsrprice = connection.cursor()

#This is a search form for searching items
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")
    
#User Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
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

#this is the database for browsing items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(80))

    def init(self, name, price):
        self.name = name
        self.price = price

#this is the database for user reviews
class reviews_table_test(db.Model):
    review_number = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    itemID = db.Column(db.Integer)
    review = db.Column(db.Text)

    def init(self, username, review):
        self.username = username
        self.review = review

#This is for reading the reviews from the database
reviews_list = []
crsruser.execute("SELECT username FROM reviews_table_test")
crsrid.execute("SELECT itemID FROM reviews_table_test")
crsrreview.execute("SELECT review FROM reviews_table_test")
rowuser = crsruser.fetchone()
rowid = crsrid.fetchone()
rowreview = crsrreview.fetchone()
while rowreview is not None:
    rowuser = " ".join(str(x) for x in rowuser)
    rowid = " ".join(str(x) for x in rowid)
    rowreview = " ".join(str(x) for x in rowreview)
    print(rowuser, rowid, rowreview)
    new_review = reviews_table_test(
        username = rowuser,
        itemID = rowid,
        review = rowreview)
    reviews_list.append(new_review)   
    rowuser = crsruser.fetchone()
    rowid = crsrid.fetchone()
    rowreview = crsrreview.fetchone()
        
        
#this is the wishlist database
class wishlist(db.Model):
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
# itemsList.append(Item(name = 'Coke', price = 1.50))
# db.session.add(itemsList[0])
# db.session.commit()

# itemsList.append(Item(name = 'Yoyo', price = 1.75))
# db.session.add(itemsList[1])
# db.session.commit()

# itemsList.append(Item(name = "Jar", price = 0.50))
# db.session.add(itemsList[2])
# db.session.commit()

# itemsList.append(Item(name = "Soccer Ball", price = 50.00))
# db.session.add(itemsList[3])
# db.session.commit()

#This is for reading the items from the database
crsrid.execute("SELECT id FROM item")
crsrname.execute("SELECT name FROM item")
crsrprice.execute("SELECT price FROM item")
rowid = crsrid.fetchone()
rowname = crsrname.fetchone()
rowprice = crsrprice.fetchone()
while rowprice is not None:
    rowid = " ".join(str(x) for x in rowid)
    rowname = " ".join(str(x) for x in rowname)
    rowprice = " ".join(str(x) for x in rowprice)
    print(rowid, rowname, rowprice)
    new_item = Item(
        id = rowid,
        name = rowname,
        price = rowprice)
    itemsList.append(new_item)   
    rowid = crsrid.fetchone()
    rowname = crsrname.fetchone()
    rowprice = crsrprice.fetchone()

wish_list = []

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
                session["username"] = username
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                session['logged_in'] = False
                return '''
            <html>
            <head> Incorrect Log In </head>
            <a href="/login">
            <button>Go back</button>
            </a>    
            </html
            '''
        except:
            session['logged_in'] = False
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
    tempuser = session['username']
    temppuser = User.query.filter_by(username = tempuser).first()
    db.session.delete(temppuser)
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
    tempuser = session['username']
    temppuser = User.query.filter_by(username = tempuser).first()
    tempid = temppuser.id
    temppass = temppuser.password
    print(tempuser)
    print(tempid)
    if request.method == 'POST':
        password=request.form['password']
        temppuser.password =request.form['newpassword']
        if password == temppass:
            db.session.commit()
            flash('Your password has been updated!')
            return render_template('index.html')
        else:
            flash('You entered an incorrect password')
            return render_template('changepassword.html')
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
    itemId = Item.query.get(id)
    iName = Item.query.get(id).name
    iPrice = Item.query.get(id).price

    ReducedPrice = iPrice * .1

    if not session.get('logged_in'):
        return render_template('itemInfo.html', itemName = iName, itemPrice = format(iPrice, '.2f'), IdNum = id, review_list = reviews_list, ReducedPrice = format(ReducedPrice, '.2f'), list = itemsList)

    else:
        tempUser = session['username']

        if request.method == 'POST':
            new_review = reviews_table_test(
                username = tempUser,
                itemID = id,
                review = request.form['review'])
            reviews_list.append(new_review)   
            db.session.add(new_review)
            db.session.commit()
            
        return render_template('itemInfo.html', itemName = iName, itemPrice = format(iPrice, '.2f'), IdNum = id, review_list = reviews_list, ReducedPrice = format(ReducedPrice, '.2f'), list = itemsList)

#@app.route("/itemInfo")
#def itemInfo :
    #return render_template('intemInfo.html', item)
    
@app.route('/addreview', methods=['GET', 'POST'])
def addreview():
 
    # if session['logged_in'] == True:
    
    # new_review = reviews_table_test
    if not session.get('logged_in'):
        return render_template('addreview.html', IdNum = id, review_list = reviews_list, list = itemsList)

    else:    
        tempUser = session['username']
        if request.method == 'POST':
            new_review = reviews_table_test(
                username = tempUser,
                review = request.form['review'])
            reviews_list.append(new_review)   
            db.session.add(new_review)
            db.session.commit()
        
        return render_template('addreview.html', IdNum = id, review_list = reviews_list, list = itemsList)

@app.route('/iI/<int:id>/coupon', methods=['GET', 'POST'])
def addcoupon(id):

    itemId = Item.query.get(id)
    iName = Item.query.get(id).name
    iPrice = Item.query.get(id).price
    #uName = User.query.get(username)
    ReducedPrice = iPrice * .1

    usercoupon = "Test"
    coupons = False
    couponcode = "Rojas"

    if request.method == 'POST':
        usercoupon = request.form['coupon'],
        if usercoupon[0] == couponcode:
            coupons = True
        
        print(usercoupon)
    return render_template('coupon.html', itemName = iName, itemPrice = format(iPrice, '.2f'), IdNum = id, review_list = reviews_list, coupon = coupons, ReducedPrice = format(ReducedPrice, '.2f'))

@app.route('/addWishlist/<int:IdNum>')
def addWishlist(IdNum):
    itemId = Item.query.get(IdNum)
    iName = Item.query.get(IdNum).name
    iPrice = Item.query.get(IdNum).price
    wishlistEntry = wishlist(name = iName, price = iPrice)

    wish_list.append(wishlistEntry)

    db.session.add(wishlistEntry)
    db.session.commit()

    return render_template('successWishlist.html', add = 1, wishList = wish_list)

@app.route('/removeItem/<int:id>')
def removeItem(id):  
    #Deleting from the database
    deleteItem = wishlist.query.filter_by(id= id).first()
    db.session.delete(deleteItem)
    db.session.commit()

    #Deleting the item from the array in app.py
    for item in wish_list:
        if item.id == id:
            wish_list.remove(item)
    return render_template('successWishlist.html', delete = 1, wishList = wish_list)

@app.route('/viewWishList')
def viewWishList():
    return render_template('successWishlist.html', wishList = wish_list)

@app.context_processor
def base():
    form = SearchForm()
    return dict(form = form)
    
@app.route('/iI/<int:id>')
def post(id):
	post = Item.query.get_or_404(id)
	return render_template('itemInfo.html', post=post)

@app.route('/browse', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    posts = Item.query
    if form.validate_on_submit:
        post.searched = form.searched.data
        posts = posts.filter(Item.name.like('%' + post.searched + '%'))
        posts = posts.order_by(Item.name).all()
        
        return render_template("browse.html",form=form, searched=post.searched, posts = posts)
        
if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')

