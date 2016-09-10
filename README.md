# Parrot

####A full-stack web application built in 4 weeks as Hackbright Fellowship final project.
<img src="/static/img/Screenshots/HomePage.png" alt="Parrot Mainpage Screenshot"/>

## Description
Parrot is an interactive learning tool that makes learning Spanish as a second language easy, fun and social.

Intended for users who have achieved minimum professional language proficiency, Parrot allows users to translate phrases in an article when they get stuck. Users can register, save article preferences and select articles to read. Phrases can be selected and Parrot will show a translation right above the selection! It is user-friendly and intuitive. Users can make comments and respond to comments from other users. The 'Parrot feature' allows the user to send a phrase and its translation to their mobile device for on the go review. Translated phrases are also added to a Vocabulary List that are accessible within the app.

## Table of Contents
* [Technologies Used](#technologiesused)
* [APIs Used](#apisused)
* [Features](#features)
* [Design](#design)
* [Project Next Steps](#nextsteps)
* [Installation Instructions](#installation)
* [About the Author](#author)

## <a name="technologiesused"></a>Technologies Used
* Python 2
* JavaScript
* Flask
* HTML5
* CSS3
* jQuery
* AJAX
* JSON
* PostgreSQL
* SQLAlchemy
* Jinja 
* Bootstrap 
* [Newspaper Python Library](https://pypi.python.org/pypi/newspaper)

##<a name="apisused"></a>APIs used
* Google Translate API
* Twilio API

## Features
Users can create an account and log into their account.
<img src="/static/img/Screenshots/LoginPage.png" alt="Parrot Login page Screenshot"/>

Once logged in, users are presented with three articles from each of their category preferences.
<img src="/static/img/Screenshots/ProfilePage.png" alt="Parrot Profile page Screenshot"/>

<!-- If the user does not like the articles provided, they may chose to see more from that category.  -->

When the user clicks "Parrot," they are directed to a page displaying the article. As the user is reading, if they get stuck, they can highlight a phrase and a popover will display containing three buttons:
* [Translate](#translate)
* [Comment](#comment)
* [Send SMS](#twilio)
<img src="/static/img/Screenshots/TranslationButton.png" alt="Translation Button Screenshot"/>

####<a name="translate"></a>Translate
If the user clicks the "Translate" Button, a call is made to Google Translate API and the translation is displayed in the popover. The phrase and translation are also stored in the database.
<img src="/static/img/Screenshots/TranslationPopover.png" alt="Translation Popover Screenshot"/>

####<a name="comment"></a>Comment
If the user finds a phrase that might be an idiom or perhaps a phrase that might require additional context, they could chose to click the "Comment" Button. 
<img src="/static/img/Screenshots/CommentButton.png" alt="Comment Button Screenshot"/>

A comment window will display in-line with the selection. 
<img src="/static/img/Screenshots/CommentWindow.png" alt="Comment Window Screenshot"/>


When the user makes a comment, a grey rectangle will appear over the phrase that has an attached comment. The user can click the words inside of the grey rectangle to view the comments which are viewable to other users who read the same article. 
<img src="/static/img/Screenshots/CommentLink.png" alt="Grey Rectangle Screenshot"/> 
<img src="/static/img/Screenshots/CommentLinkWindow.png" alt="Comment Link Screenshot"/>

The user can even see older comments made by other users and comment back to them. 
<img src="/static/img/Screenshots/ArticleComments.png" alt="Article Comments Screenshot"/>

####<a name="twilio"></a>Send SMS Message
If the user is reading and wants to remember the new phrase they have learned and study on-the-go, they can send a text message to their mobile device containing the origin phrase and its translation. 
<img src="/static/img/Screenshots/TwilioButton.png" alt="Twilio Button Screenshot"/>
<img src="/static/img/Screenshots/TwilioMessage.png" alt="Twilio Message Screenshot"/>

## <a name="design"></a>Design
* Design elements implemented using [Bootstrap](http://getbootstrap.com/), HTML5 and CSS3. 
* All logo design done by the [author](https://www.linkedin.com/in/khardsonhurley) using Adobe Illustrator.
* Photograph taken by author.
* Bold typeface chosen for article titles to draw attention to strong headlines.
* Serif typeface for article body chosen to mimic the look of a physical newspaper. 
* Use of various shades of white to create a clean and crisp look and maintain focus on learning while reading.

## <a name="nextsteps"></a>Project Next Steps
* Offer Parrot in other languages. 
* Allow the user to chose their news source.
* Allow for live rss feed.
* Schedule SMS messenger to send quiz questions to check if the user remembers meaning of words they have looked up.
* Recommend articles to the user.
* Recommend commonly translated words for the user to read over before reading the article. 

## <a name="installation"></a>Installation Instructions
#### Parrot has not yet been deployed, to run the app locally on your machine follow these instructions:

* You must have the following programs already installed on your machine:
    * [Python 2.7](https://www.python.org/downloads/)
    * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
    * [PostgresSQL](https://www.postgresql.org/download/)

* Create and activate a virtual environment inside your project directory:
```
$ virtualenv env
$ source env/bin/activate
```
* Clone the directory and install all dependencies:
```bash
(env)$ git clone https://github.com/khardsonhurley/Hackbright-Project.git
```
* Install the requirements:
```
(env)$ pip install -r requirements.txt
```
* Create a new postgreSQL database:
```bash    
(env)$ createdb parrot
```
* Exit the PostgreSQL server (ctrl+d), open the model.py in interactive mode, and create the tables in your database:
```bash
(env)$ python -i model.py
>>> db.create_all()
```
* Exit interactive mode (ctrl+d). Seed the database with article and dummy user data. This will take some time.
```bash
(env)$ python seed.py
```
* Create a <kbd>secrets.sh</kbd> file. 
```
(env)$ touch secrets.sh YOUR_DIRECTORY_NAME_HERE
```
* While the database is seeding, get secret keys for [Twilio API](https://www.twilio.com/) and [Google Translate API](https://cloud.google.com/translate/docs/). Save them to secrets.sh.

```
export GOOGLE_TRANSLATE_KEY="REPLACE_WITH_YOUR_KEY"  
export TWILIO_SECRET_KEY="REPLACE_WITH_YOUR_KEY"  
```
* Source the variables to your virtual environment.
```
(env)$ source secrets.sh
```
*  Start up the flask server.
```bash
(env)$ python server.py
```
* Go to http://0.0.0.0:5000/ to see the web app

## <a name="author"></a>About the Author

Krishelle graduated Summa Cum Laude from the University of San Diego with a dual major in Mathematics and Spanish and a Teaching Credential. Prior to Hackbright, she taught High School Math and Spanish, while she pursued a Masters Degree focused on Math and Technology Education. After teaching for six years, Krishelle discovered her passion for designing tools that make processes more efficient. She realized that software engineering would be the perfect opportunity to combine this passion with her love for problem solving. Krishelle's love for learning and making an impact run strong, and she is excited to contribute her creativity to a full-stack software development role. Learn more about Krishelle [here](https://www.linkedin.com/in/khardsonhurley). 











