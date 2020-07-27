# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, session, url_for
# from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import model

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:8pcd0XmbvbLDNpCf@cluster0.6gvi8.mongodb.net/users?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
# @app.route('/index', methods= ["GET", "POST"])
# def index():
#     return render_template('index.html')

@app.route('/welcomePage', methods= ["GET", "POST"])
def welcomePage():
    return render_template('welcomePage.html')

@app.route('/homePage', methods= ["GET", "POST"])
def homePage():
    data_updates = mongo.db.updates
    updates = data_updates.find({})
    updatesData = []
    for i in updates:
        updatesData.append(i)
    updatesData.reverse()
    data_ads = mongo.db.ads
    ads = data_ads.find({})
    adsData = []
    print(ads)
    for i in ads:
        adsData.append(i)
    adsData.reverse()
    return render_template('homePage.html', updatesData = updatesData, adsData = adsData)

@app.route('/signUp', methods= ["GET", "POST"])
def signUp():
    # add mongo db stuff so that it adds user information when they sign up
    # users>> user, user_password, userbirthday etc
    if request.method == "GET":
        return render_template('signUp.html')
    else:
        user_name = request.form["user_name"]
        user_interest = request.form["user_interest"]
        user_education = request.form["user_education"]
        user_headline = request.form["user_headline"]
        user_linkedin = request.form["user_linkedin"]
        user_email = request.form["user_email"]
        user_password = request.form["psw"]
        user_password_repeat = request.form["psw-repeat"]
        ##Checking if the email is already registered and connecting to database
        data_user_info = mongo.db.user_info
        user_info = data_user_info.find({})
        user_infoData = []
        for i in user_info:
            user_infoData.append(i)
        # user_infoData.sort("user_name")
        existing_user = data_user_info.find_one({'user_email' : user_email})
        if existing_user is None: 
            #Checking that user entered same password
            if not (user_password == user_password_repeat): 
                return ("You entered different passwords, please try again!")
            #Adding new user to database
            data_user_info.insert({"user_name":user_name,"user_email":user_email, "user_password": 
            user_password,"user_password_repeat":user_password_repeat, "user_interest": user_interest, 
            "user_education": user_education, "user_headline": user_headline, 'user_linkedin': user_linkedin })
            # return redirect(url_for('homePage.html'))
            return render_template('homePage.html', existing_user = existing_user, user_infoData = user_infoData)
        return 'That email already exists! Try logging in.'
    return render_template('signUp.html')

@app.route('/signIn', methods= ["GET", "POST"])
def signIn():
    if request.method=="GET":
        return render_template('signIn.html')
    else:
        user_email = request.form["user_email"]
        user_password = request.form["password"]
        ##Connecting to database
        data_user_info = mongo.db.user_info
        user_info = data_user_info.find({})
        user_infoData = []
        for i in user_info:
            user_infoData.append(i)
        #Checking to see if email in database
        login_user = data_user_info.find_one({'user_email' : user_email})
        print(login_user)
        if login_user is None: 
            return ("It seems like you do not have an account, please type your email correctly or sign up!")
        elif user_password != login_user["user_password"]:
            return "Incorrect password, please try again!"
        elif (user_email == login_user["user_email"]) and (user_password == login_user["user_password"]): 
            return "Success! You have signed in! Go to the <a href='/homePage'> home page! </a>"
        return 'Invalid combination!'

@app.route('/add')

def add():
    # connect to the database
    user_email = request.form["user_email"] 
    collection = mongo.db.user_info
    # user_info = collection.find({})
    collection.insert({'user_name': "jameschu", "user_email":"james2@gmail.com", "user_password": "password"})
    # insert new data
    # return a message to the user
    return "Done!"


# @app.route('/signUp', methods = ["GET", "POST"])
# def signUp():
@app.route('/contactPage', methods= ["GET", "POST"])
def contactPage():
    data_user_info = mongo.db.user_info
    user_info = data_user_info.find({})
    user_infoData = []
    for i in user_info:
        user_infoData.append(i)
    # user_infoData.sort()
    return render_template('contactPage.html', user_infoData = user_infoData)

@app.route('/discussionPage')#, methods= ["GET", "POST"])
def discussionPage():
    return render_template('discussionPage.html')

@app.route('/resourcesPage', methods= ["GET", "POST"])
def resourcesPage():
    return render_template('resourcesPage.html')

@app.route('/profilePage', methods= ["GET", "POST"])
def profilePage():
    return render_template('profilePage.html')

@app.route('/artPage', methods= ["GET", "POST"])
def artPage():
    art_description = request.form["art_description"]
    art_link = request.form["art_link"]
    data_arts = mongo.db.arts
    arts = data_arts.find({})
    artsData = []
    for i in arts:
        artsData.append(i)
    artsData.reverse()
    data_arts.insert({'art_description': art_description, 'art_link': art_link})
    return render_template('art_Meme.html', artsData = artsData)

@app.route('/art_Meme', methods= ["GET", "POST"])
def art_Meme():
    data_arts = mongo.db.arts
    arts = data_arts.find({})
    artsData = []
    for i in arts:
        artsData.append(i)
    artsData.reverse()
    return render_template('art_Meme.html', artsData = artsData)

@app.route('/addAds', methods= ["GET", "POST"])
def addAds():
    # connect to the database
    advertisementImage = request.form["adUrl"]
    data_ads = mongo.db.ads
    ads = data_ads.find({})
    adsData = []
    for i in ads:
        adsData.append(i)
    adsData.reverse()
    # insert new ads image url so that can use for html
    data_ads.insert({'advertisementImage': advertisementImage})
    # return a message to the user
    return render_template('homePage.html', adsData = adsData)

@app.route('/addUpdate', methods= ["GET", "POST"])
def addUpdate():
    # connect to the database
    update_heading = request.form["update_heading"]
    update_messenger = request.form["update_messenger"]
    update_text = request.form["update_text"] 
    update_link = request.form["update_link"] 
    data_updates = mongo.db.updates
    updates = data_updates.find({})
    updatesData = []
    for i in updates:
        updatesData.append(i)
    updatesData.reverse()
    # insert new ads image url so that can use for html
    data_updates.insert({'update_heading': update_heading, 'update_text': update_text, 'update_link': update_link, 'update_messenger':update_messenger })
    # return a message to the user
    return render_template('homePage.html', updatesData = updatesData)
