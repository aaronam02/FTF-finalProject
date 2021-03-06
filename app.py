# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import bcrypt
from flask import redirect, session, url_for
from flask_pymongo import PyMongo
import model
import os

# -- Initialization section --
app = Flask(__name__)
app.secret_key = "j324jbkfdsbjou932pbojnljnmsmdfnip932o"
user = os.environ['user']
pw = os.environ['pw']

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = f'mongodb+srv://{user}:{pw}@cluster0.6gvi8.mongodb.net/users?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --

@app.route('/')
@app.route('/welcomePage', methods= ["GET", "POST"])
def welcomePage():
    session.clear()
    return render_template('welcomePage.html')

@app.route('/homePage', methods= ["GET", "POST"])
def homePage():
    if request.method == "GET":
        if session:
            # Retrieving updates and ads for home page
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
        else:
            # Returning user to welcome page to sign in/sign up
            return "You are not signed in. Please navigate to the <a href ='/welcomePage'> welcome page </a> to access the network!"
    else:
        user_email = request.form["user_email"]
        user_password = request.form["password"]
        ##Connecting to database
        data_user_info = mongo.db.user_info
        data_user = data_user_info.find({})
        user_infoData = []
        for i in data_user:
            user_infoData.append(i)
        user_infoData.reverse()
        #Checking to see if email in database
        login_user = data_user_info.find_one({'user_email' : user_email})
        if login_user is None: 
            return ("It seems like you do not have an account, please type your email correctly or sign up!")
        elif (bcrypt.hashpw(user_password.encode('utf-8'), login_user['user_password'].encode('utf-8')) != login_user["user_password"].encode('utf-8')):
            #Checks to see if user typed in the same password twice 
            return "Incorrect password, please try again!"
        elif (user_email == login_user["user_email"]) and (bcrypt.hashpw(user_password.encode('utf-8'), login_user['user_password'].encode('utf-8')) == login_user["user_password"].encode('utf-8')): 
            #Checks to see if user email and password matches the inputted user email and password
            session["user_email"] = user_email
            data_updates = mongo.db.updates
            updates = data_updates.find({})
            updatesData = []
            for i in updates:
                updatesData.append(i)
            updatesData.reverse()
            data_ads = mongo.db.ads
            ads = data_ads.find({})
            adsData = []
            for i in ads:
                adsData.append(i)
            adsData.reverse()
            return render_template('homePage.html', updatesData = updatesData, adsData = adsData)
        #None of the above apply, the inputted email and password aren't a valid combination
        return 'Invalid combination! Please Try Again'

@app.route('/contactPage', methods= ["GET", "POST"])
def contactPage():
    if request.method == "GET":
        data_user_info = mongo.db.user_info
        user_info = data_user_info.find({})
        user_infoData = []
        for i in user_info:
            user_infoData.append(i)
        # user_infoData.sort()
        return render_template('contactPage.html', user_infoData = user_infoData)
    else:
        contact_fname = request.form["firstname"]
        contact_lname = request.form["lastname"]
        contact_email = request.form["email"]
        contact_location = request.form["state"]
        contact_reason = request.form["subject"]
        contact_date =  request.form["date"]
        data_contactUs = mongo.db.contactUs
        contactUs = data_contactUs.find({})
        #array for contact us infomation so that we can use api to email them
        contactUsData = []
        for i in contactUs:
            contactUsData.append(i)
        data_contactUs.insert({'contact_fname': contact_fname, 'contact_lname':contact_lname, 'contact_location': contact_location, 'contact_reason': contact_reason, 'contact_date': contact_date, 'contact_email' : contact_email})
        # return render_template('art_Meme.html', contactUs = contactUs)    
        return "<h1>Thank you for reaching out, your email has been sent. We will get back to you as soon as possible. Navigate to the <a href ='/welcomePage'> welcome page </a> to sign in!"
        

@app.route('/discussionPage')#, methods= ["GET", "POST"])
def discussionPage():
    return render_template('discussionPage.html')

@app.route('/resourcesPage', methods= ["GET", "POST"])
def resourcesPage():
    return render_template('resourcesPage.html')

@app.route('/deleteAccount', methods= ["GET", "POST"])
def deleteAccount():
    if session:
        users = mongo.db.user_info
        email = session['user_email']
        user = users.find_one({"user_email":email})
        users.delete_one({'user_email': email})
        session.clear()
        return "Your account is has been deleted! Sorry for the inconvenience. Please navigate to the <a href ='/welcomePage'> welcome page </a>"
    else:
        return "You are not signed in. Please navigate to the <a href ='/welcomePage'> welcome page </a> to access the network!"

    # return render_template('editProfile.html')

@app.route('/profilePage', methods= ["GET", "POST"])
def profilePage():
    # if request.method == "GET":
    # data_user_info = mongo.db.user_info
    # user_info = data_user_info.find({})
    # user_infoData = []
    # for i in user_info:
    #     user_infoData.append(i)
    # # user_infoData.sort("user_name")
    # session['user_email'] = user_email
    # if session:
    users = mongo.db.user_info
    email = session['user_email']
    user = users.find_one({"user_email":email})
    return render_template('profilePage.html', user=user)
    # else:
    #     return "You are not Signed In, navigate to the <a href ='/welcomePage'> welcome page </a> to log in!"
    # else:

@app.route('/editProflie', methods= ["GET", "POST"])
def editProflie():
    return "<h3 {text-center}> Page under construction, if you need to edit your profile please contact us or delete your account and create a new one! To delete your account, navigate to the bottom of <a href ='/profilePage'> profile page </a> to do so!"
       

@app.route('/signUp', methods= ["GET", "POST"])
def signUp():
        # return "<h3 {text-center}> Page under construction, if you need to edit your profile please contact us or delete your account and create a new one! To delete your account, navigate to the bottom of <a href ='/profilePage'> profile page </a> to do so!"
        # # EDIT PROFILE BLOCK [collectionname].update({"user_email": ""}) example below
        # https://www.w3schools.com/python/showpython.asp?filename=demo_mongodb_update_one
    user_name = request.form["user_name"]
    user_interest = request.form["user_interest"]
    user_education = request.form["user_education"]
    user_headline = request.form["user_headline"]
    user_linkedin = request.form["user_linkedin"]
    user_email = request.form["user_email"]
    user_password = request.form["psw"]
    user_password_repeat = request.form["psw-repeat"]
    bio = request.form["bio"]
    program = request.form["program"]
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
        str(bcrypt.hashpw(user_password.encode("utf-8"), bcrypt.gensalt()), 'utf-8'), "user_interest": user_interest, 
        "user_education": user_education, "user_headline": user_headline, 'user_linkedin': user_linkedin, 'bio': bio, 'program': program, 'user_skills': request.form['user_skills'], 'user_interests': request.form['user_interests']})
        # return redirect(url_for('homePage.html'))
        session["user_email"] = user_email
        # return render_template()
        users = mongo.db.user_info
        email = session['user_email']
        user = users.find_one({"user_email":email})
        return render_template('profilePage.html', user=user, user_infoData = user_infoData, )
    else:
        return 'That email already exists! Try logging in.'

@app.route('/addArt', methods= ["GET", "POST"])
def addArt():
    if session:
        if request.method == "GET":
            return render_template('addArt.html')
        else:
            art_description = request.form["art_description"]
            art_link = request.form["art_link"]
            data_arts = mongo.db.arts
            arts = data_arts.find({})
            artsData = []
            for i in arts:
                artsData.append(i)
            artsData.reverse()
            data_arts.insert({'art_description': art_description, 'art_link': art_link})
            # return render_template('art_Meme.html', artsData = artsData)    
            return "You memory was added, navigate to the <a href ='/art_Meme'> collection </a> to see it!"

    else:
        return "You are not Signed In, navigate to the <a href ='/welcomePage'> welcome page </a> to log in!"


@app.route('/art_Meme', methods= ["GET", "POST"])
def art_Meme():
    if session:
        data_arts = mongo.db.arts
        arts = data_arts.find({})
        artsData = []
        for i in arts:
            artsData.append(i)
        artsData.reverse()
        return render_template('art_Meme.html', artsData = artsData)
    else:
        return "You are not Signed In, navigate to the <a href ='/welcomePage'> welcome page </a> to log in!"



@app.route('/addAds', methods= ["GET", "POST"])
def addAds():
    if request.method == "POST":
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
        return "You have succesfully added an advertisement, please go to <a href ='/homePage'>  home page </a> to see it displayed."
    else: 
        return render_template('addAds.html')

@app.route('/addUpdate', methods= ["GET", "POST"])
def addUpdate():
    if session:
        if request.method == "POST":
            # pulls all the data from the form
            update_heading = request.form["update_heading"]
            update_text = request.form["update_text"] 
            update_link = request.form["update_link"] 
            data_updates = mongo.db.updates
            updates = data_updates.find({})
            updatesData = []
            for i in updates:
                updatesData.append(i)
            updatesData.reverse()
            #Uses session to find the users name
            users = mongo.db.user_info
            email = session['user_email']
            user = users.find_one({"user_email":email})
            # insert new ads image url so that can use for html
            data_updates.insert({'update_heading': update_heading, 'update_text': update_text, 'update_link': update_link, 'update_messenger':user["user_name"] })
            # return a message to the user
            # return render_template('homePage.html', updatesData = updatesData)
            return "Succesfully added an update, navigate to the <a href ='/homePage'> home page </a> to see the lastest update!"

        else:
            return render_template('addUpdate.html')
    else:
        return "You are not Signed In, navigate to the <a href ='/welcomePage'> welcome page </a> to log in!"

@app.route('/communityPage')
def communityPage():
    users = mongo.db.user_info.find({})
    print(users)
    return render_template('communityPage.html', users=users)