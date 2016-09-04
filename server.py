
"""
Hackbright Project
Parrot: An learning tool for users seeking to learn Spanish as a second
language. 
by: Krishelle Hardson-Hurley
"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)

from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Article, UserArticle, Phrase, Note, UserCategoryPreference, Category, Comment)

import requests 
# This allows you to access the variables store in the environment on your 
# computer. 
import os 

import json 

import newspaper

from random import sample

import urllib

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "7hsfbiksf82083208hdbousf792389kjnkjbfsvpomysrtrc"

#Google translate key for API
key = os.environ['GOOGLE_TRANSLATE_KEY']

# Keeps jinja from failing silently because of undefined variables.
app.jinja_env.undefined = StrictUndefined

########################### ROUTES TO DISPLAY PAGES ###########################

@app.route('/')
def index():
    """Homepage with description and BEGIN button."""

    return render_template("home.html")

@app.route('/signup', methods=["GET", "POST"])
def signup_process(): 
    """Users sign up for an account."""
    
    if request.method == "GET":
        #Show the signup form to the user. 
        return render_template("signup_form.html")
        
    if request.method == "POST":
        #Process the sign up information and add user to database.
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]
        #Change later if expanding to other language. Now just hard code. 
        language = "Spanish"
        language_level = request.form["langlevel"]
        #Creates new user. LATER CHECK IF USER EXISTS!! 
        new_user = User(email=email, username=username, password=password,
                        first_name=first_name, last_name=last_name,
                        phone=phone, language=language, 
                        language_level=language_level)

        db.session.add(new_user)
        db.session.commit()

        print language_level

        session["user_id"] = new_user.user_id

        flash("Username: %s has been added." % username)

        return redirect("/preferences/%s" % new_user.user_id)



@app.route('/preferences/<int:user_id>', methods=["GET","POST"])
def set_preferences(user_id):
    """After user initiates sign up process, they enter their preferences 
    (topics they are interested in)."""
    
    if request.method == "GET":
        user = User.query.get(user_id)
        categories = Category.query.all()
        return render_template("preferences.html", user=user, categories=categories)

    if request.method == "POST":

        #Later, for "adjust preferences" delete all from database and recreate.

        #Getting the user_id from the session. 
        user_id = session.get("user_id")

        #Getting the user's preferences from the form. 
        preference1 = request.form['preference_1']
        preference2 = request.form['preference_2']
        preference3 = request.form['preference_3']

        #Creating UserPreference objects with the new preferences. 
        userpreference1 = UserCategoryPreference(user_id=user_id, 
                                        category_code=preference1, rank=1)
        userpreference2 = UserCategoryPreference(user_id=user_id, 
                                        category_code=preference2, rank=2)
        userpreference3 = UserCategoryPreference(user_id=user_id, 
                                        category_code=preference3, rank=3)
  
        
        #Can I add them all at once? 
        db.session.add(userpreference1)
        db.session.add(userpreference2)
        db.session.add(userpreference3)

        db.session.commit()

        return redirect('/profile/%s' % user_id)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Users who already have an account can log in"""

    if request.method == "GET":
        return render_template("login_form.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Invalid username.")
            return redirect("/login")
        
        if user.password != password:
            flash("Incorrect password.")
            return redirect("/login")

        session["user_id"] = user.user_id

        flash("You are logged in to Parrot!")

        # return redirect("/profile/%s" % user.user_id)
        return redirect("/profile/%s" % user.user_id)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    """Users have a dashboard profile page that displays their name, previously
    read articles, recommended articles."""
    
    user = User.query.get(user_id)
    #Get the users three category preferences.
    #Find three articles from each of these categories. 
    preferences = UserCategoryPreference.query.filter(UserCategoryPreference.user_id==user.user_id).all()
    
    preferences_dict = {}
    for preference in preferences:
        articles = Article.query.filter(Article.category_code==preference.category_code).all()
        preferences_dict[preference]=sample(articles,3)

    print preferences_dict  
    print 'im in the profile route'

    return render_template("profile.html", user=user, preferences_dict=preferences_dict)

@app.route('/article/<int:article_id>')
def article(article_id): 
    """Page where article will be rendered and user can start translating."""
    #Need this to get the article object from the DB. Note this object does not
    #contain the text of the object, just selected metadata that is stored in the DB. 
    articleobj = Article.query.filter(Article.article_id==article_id).first()

    #Instantiate an instance of the class Article [from newspaper library], the
    #__init__ for this class requires a url retrieved from the articleobj above.
    #This allows us to instantiate another object that has all of the metadata 
    #including the text of the article.  
    articleobj = newspaper.Article(articleobj.url)
    #Download the article.
    articleobj.download()
    #Parse through the article. 
    articleobj.parse()

    #Remove an article_id that is in the session and replace it with new 
    #article_id, note that if you return to the same article, its okay becuase
    #article_id will keep it honest since it never changes. 
    session["article_id"] = article_id

    return render_template("article.html", article=articleobj)

@app.route('/articletest')
def article_test():
    return render_template("ARTICLETEXT.html")


@app.route('/category/<category_code>')
def category(category_code):
    """Page where many articles from one category are displayed.""" 
    #get all of the articles from that category code. and send them with the html.

    articles = Article.query.filter(Article.category_code==category_code).all()

    return render_template("categorypage.html", articles=articles)



@app.route('/translate', methods = ["GET", "POST"])
def translating():
    """In this url is in the following format:
    https://www.googleapis.com/language/translate/v2?parameters
        parameters include: 
            key: the api key defined above
            source: the language of the article (es = Spanish)
            target: the language you want translated to (en = English)
            q: Specifies the text to translate.
    """ 

    if request.method == "GET":
        return render_template("translate.html")


    if request.method == "POST":
        #Getting the value in the dictionary sent by JS. 
        phrase = request.form.get("phrase")

        #Change phrase to unicode. Has new variable because need to access later
        #to add to the database. 
        uni_phrase=unicode(phrase)

        #encodes the phrase into utf-8 format.
        phrase=uni_phrase.encode('utf-8')

        #replace any reserved characters with the escape functions for it so 
        #these do not break in the request to google api. Ex: 45.2% was not 
        #readible in the api because google turns it into 45.2%%20, % is a 
        #special character. The url.quote function below turns that into 45.2%25
        #because %25 is the escape character for %. To google it because 45.2%25%20.
        phrase = urllib.quote(phrase)

        #Splitting the words into a list. 
        word_list = phrase.split(' ')

        #Googles url, pulling secret key into url. 
        google_url = "https://www.googleapis.com/language/translate/v2?key=%s&source=es&target=en&q=" % (key)

        #Google requires words separated by %20. 
        text = "%20".join(word_list)

        #The results I get back here is going to be JSON
        results = requests.get(google_url + text)

        #Converts the results from the http response object from json to a dictionary.
        dictresults= json.loads(results.text)

        #Gets the translated text out of the dictionary in list in dictionary.
        translation= dictresults['data']['translations'][0]['translatedText']

        #Adds phrase and its translation to the DB using helper function. 
        add_phrase_to_db(uni_phrase,translation)

        return translation

@app.route('/checkcomments', methods = ['POST'])
def check_comments():

    start = request.form.get('start')
    end = request.form.get('end')
    article_id = session.get('article_id')

    phrase_key = (article_id, start, end)

    print phrase_key

    #This returns a list of comments associated with the comment key. 
    comments = Comment.query.filter(Comment.phrase_id==phrase_key).all()

    print comments

    comment_data = []

    for comment in comments: 
        comment_dict={}
        comment_dict['userName'] = comment.user.username
        comment_dict['userComment'] = comment.comment
        comment_dict['userImage'] = comment.user.image
        comment_data.append(comment_dict)
    
    session["start"] = start
    session["end"] = end
    
    print "\n\n\n\n\n\n %s \n\n\n\n\n\n" % comment_data
    return jsonify(commentData=comment_data)



@app.route('/comments', methods = ["POST"])
def test_comments():
    comment = request.form.get('comment')

    #Comment Location data
    start = session.get('start')
    end = session.get('end')
    article_id = session.get('article_id')

    user_id = session.get('user_id')

    phrase_key = (article_id, start, end)
    
    new_comment = Comment(phrase_id = phrase_key,       
                            user_id=user_id, article_id=article_id, 
                            comment=comment)
    db.session.add(new_comment)
    db.session.commit()
    
    user = User.query.get(user_id)

    user_name=user.first_name

    image = user.image
 
    commentData = [{'userName': user_name, 'userComment': comment, 'userImage': image}]


    print "\n\n\n\n\n\n %s \n\n\n\n\n\n" % commentData
    return jsonify(commentData=commentData)

@app.route('/logout')
def logout_user():
    """Log out the user and delete user from session"""
    
    flash('You have successfully logged out.')
    del session['user_id']

    return redirect("/")

############################### HELPER FUNCTIONS ###############################

def add_phrase_to_db(phrase,translation):
    """Takes in phrase and its translation and adds it to the DB"""
    #Both user_id and article_id are stored in the flask session.
    user_id = session.get('user_id')
    article_id = session.get('article_id')
    
    #Instantiated an instance of the class Phrase. 
    phrase_pair= Phrase(user_id=user_id, article_id=article_id, phrase=phrase, translation=translation)
    
    #Add phrase_pair instance to the database and commits it. .
    db.session.add(phrase_pair)
    db.session.commit()

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
