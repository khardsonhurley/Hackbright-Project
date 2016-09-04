"""Models and database functions for Parrot"""


#allows me to use the session object
from flask_sqlalchemy import SQLAlchemy 


# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. The session in db.session is an objects
# that allows us to design and get information from the database. 

db = SQLAlchemy()

################################################################################
#Model definitions (MVP)

class User(db.Model):
    """User of Parrot website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=True)
    first_name = db.Column(db.String(50),nullable=True)
    last_name = db.Column(db.String(50),nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    #Here will auto seed Spanish until enable other language features. 
    language = db.Column(db.String(20),nullable=True)
    #Consult language proficiency resource
    language_level = db.Column(db.String(15),nullable=True)
    image = db.Column(db.String(500), nullable=True)  
    ##### Relationships #####
    #Note that from the articles table if you call on 'users' it will return a
    #list of article objects for that user. 
    articles = db.relationship('Article', secondary= 'user_articles', 
                                backref= 'users')

    categories = db.relationship('Category', 
                                  secondary='user_category_preferences',
                                  backref='users')

class Article(db.Model):
    """Articles available to users."""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    mainsite = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(500), nullable=True)
    authors= db.Column(db.String(500), nullable=True)
    language = db.Column(db.String(15), nullable=True)
    category_code = db.Column(db.String(30),
                    db.ForeignKey('categories.category_code'),nullable=False)
    url = db.Column(db.String(500), nullable=True)
    top_image = db.Column(db.String(500),nullable=True)
    # text = db.Column(db.Text, nullable=False)

class UserArticle(db.Model):
    """Association table between users and articles. Shows which articles each
    user read and which users read each article."""

    __tablename__ = "user_articles"

    user_article_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)

class Category(db.Model):
    """Stores all article categories."""

    __tablename__ = "categories"

    category_code = db.Column(db.String(30), primary_key=True)
    url = db.Column(db.String(500), nullable=True)
    english_category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)


class UserCategoryPreference(db.Model):
    """Association table between users and preferences. Shows which preferences
    each user chose.""" 

    __tablename__= "user_category_preferences"

    user_preference_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_code = db.Column(db.String(30), 
                                db.ForeignKey('categories.category_code'), 
                                nullable=False)
    rank = db.Column(db.Integer,nullable=False)

    ##### Relationships #####
    category = db.relationship('Category', backref='usercategorypreference')



class Phrase(db.Model):
    """Stores phrases (1+ words) that the user translates within the article."""

    __tablename__ = "phrases"

    phrase_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)
    phrase = db.Column(db.String(400), nullable=False)
    translation = db.Column(db.String(400), nullable=False)
    
    ##### Relationships #####
    article = db.relationship('Article', backref='phrases')
    user = db.relationship('User', backref='phrases')

class Note(db.Model):
    """Stores the notes a user makes when reading an article."""

    __tablename__ = "notes"

    notes_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)

    text = db.Column(db.Text, nullable=True)

    ##### Relationships #####

    #Note that from the articles table if you call on 'notes' it will return a
    #list of notes for that particular article. 
    article = db.relationship('Article', backref='notes')

    #Note that from the users table if you call on 'notes' it will return a
    #list of notes for that particular article. 
    user = db.relationship('User', backref='notes')



################################################################################
#Model definitions (2.0 Features)

class Comment(db.Model):
    """Stores comments made by user in each channel"""
    
    __tablename__ = "comments"


    comment_id = db.Column(db.Integer,
                        autoincrement=True, primary_key=True)

    phrase_id = db.Column(db.PickleType, nullable=False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer,
                        db.ForeignKey('articles.article_id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)

    ##### Relationships #####
    article = db.relationship("Article", backref='comments')
    user = db.relationship('User', backref='comments')


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///parrot'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."




