# Parrot

###A full-stack web app built in 4 weeks as Hackbright Fellowship final project.
<img src="/static/img/Screenshots/HomePage.png" alt="Parrot Mainpage Screenshot"/>

## Description
Parrot is an interactive learning tool that makes learning Spanish as a second language easy, fun and social.

Intended for users who have achieved minimum professional language proficiency, Parrot allows users to translate phrases in an article when they get stuck. Users can register, save article preferences and select articles to read. Phrases can be selected and Parrot will show a translation right above the selection! It is user-friendly and intuitive. Users can make comments and respond to comments from other users. The 'Parrot feature' allows the user to send a phrase and its translation to their mobile device for on the go review. Translated phrases are also added to a Vocabulary List that are accessible within the app.

## Table of Contents
* [Technologies Used](#technologiesused)
* [APIs Used](#apisused)
* [Features](#features)
* [Installation Instructions](#installationinstructions)
* [Author](#author)

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

##<a name="apisuser"></a>APIs used
* Google Translate API
* Twilio API

## Features
Users can create an account and log into their account.
<img src="/static/img/Screenshots/LoginPage.png" alt="Parrot Login page Screenshot"/>

Once users have logged in, users are presented with three articles from each of their category preferences.
<img src="/static/img/Screenshots/ProfilePage.png" alt="Parrot Profile page Screenshot"/>

<!-- If the user does not like the articles provided, they may chose to see more from that category.  -->

When the user clicks "Parrot," they are directed to a page displaying the article. As the user is reading, if they get stuck, they can highlight a phrase and a popover will display containing three buttons:
* Translate
* Comment
* Send Message
<img src="/static/img/Screenshots/TranslationButton.png" alt="Translation Button Screenshot"/>
