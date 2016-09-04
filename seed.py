"""Utility file to seed the articles database from newspaper API"""

from sqlalchemy import func
from model import (Article, Category, User, UserCategoryPreference)
from server import app, db, connect_to_db
import newspaper
        
# Global variables. 
category_dict = {'politica':'Politics', 
                 'one': 'Media',
                 'deportes': 'Sports',
                 'escuela': 'Education',
                 'cultura': 'Culture',
                 'smoda': 'Fashion',
                 'resultados': 'Olympics',
                 'internacional': 'International',
                 'tecnologia':'Technology',
                 'elpaissemanal':'Weekly News',
                 'elviajero': 'Travel',
                 'economia': 'Economics',
                 'elcomidista':'Food'
                 }

category_urls = ['http://politica.elpais.com', 'http://one.elpais.com',
    'http://deportes.elpais.com','http://escuela.elpais.com', 
    'http://cultura.elpais.com', 'http://smoda.elpais.com', 'http://resultados.elpais.com', 
    'http://internacional.elpais.com', 'http://tecnologia.elpais.com', 
    'http://elpaissemanal.elpais.com', 'http://elviajero.elpais.com', 
    'http://economia.elpais.com', 'http://elcomidista.elpais.com']

def add_categories():
    """Loads categories into the database."""
    for category in category_dict:
        url = 'http://%s.elpais.com' % category
        db_category = Category(category_code=category, url=url,
                            english_category=category_dict[category])
        #Verifying that the category has been added. 
        db.session.add(db_category)
        db.session.commit()

    print "\n\n\n\n\n DONE WITH ADDING CATEGORIES \n\n\n\n\n"

def load_articles():
    """Load articles into articles table. Adds categories to categories table."""
    
    for url in category_urls:
        #creates a newspaper object. 
        category_newspaper = newspaper.build(url, memoize_articles=False)
        #gets the category code from the url. 
        category_name = url[7:-11]
        
        #Queries for the category in the database. 
        result = Category.query.filter_by(category_code=category_name)

        # #If the category is not already in the database, adds 
        # #to the categories table.
        if not result: 
            #Adds category to the database in the categories table. 
            db_category = Category(category_code=category_name, url=url,
                            english_category=category_dict[category_name])

            #Verifying that the category has been added. 
            db.session.add(db_category)
            db.session.commit()

        print "\n\n\n\n\nArticle Category: %s \n\n\n\n\n" % (category_name)
        
        #creates a list of article objects. 
        category_articles = category_newspaper.articles[:21]


        #iterates over the list of article objects. 
        for article in category_articles:
            #downloads and parses through the article. 
            article.download()
            print 'after download'
            article.parse()
            print 'after parse'

            #instantiates an instance in the articles table. 
            db_article = Article(mainsite=url, title=article.title, 
                            authors=article.authors, language='es',
                            url=article.url, category_code=category_name, 
                            top_image=article.top_image)

            #adds the article content to the database. 
            db.session.add(db_article)
            db.session.commit()
            #Verifying article is committed. 
            print "commited %s" % (db_article)


def load_users():
    """Load users from u.user into database"""

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        user_id,email,username,password,first_name,last_name,phone,language,language_level,image = row.split("|")
        user = User(user_id=user_id, username=username, password=password,
                    first_name=first_name, last_name=last_name, phone=phone,
                    language=language, language_level=language_level, image=image)
        db.session.add(user)

    db.session.commit()

    print "\n\n\n\n\n DONE WITH ADDING USERS \n\n\n\n\n"

def load_user_preferences():
    """Load user preferences into the database"""
    for i, row in enumerate(open("seed_data/u.preferences")):
        row = row.rstrip()
        user_preference_id,user_id,category_code,rank=row.split("|")
        user_preference=UserCategoryPreference(user_preference_id=user_preference_id, user_id=user_id,
                                                category_code=category_code, rank=rank)
        db.session.add(user_preference)

    db.session.commit()

    print "\n\n\n\n\n DONE WITH ADDING USER PREFERENCES \n\n\n\n\n"

###################### HELPER FUNCTIONS ########################


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    # add_categories()
    # load_articles()
    # load_users()   
    load_user_preferences()