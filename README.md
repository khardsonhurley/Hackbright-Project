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

Once logged in, users are presented with three articles from each of their category preferences.
<img src="/static/img/Screenshots/ProfilePage.png" alt="Parrot Profile page Screenshot"/>

<!-- If the user does not like the articles provided, they may chose to see more from that category.  -->

When the user clicks "Parrot," they are directed to a page displaying the article. As the user is reading, if they get stuck, they can highlight a phrase and a popover will display containing three buttons:
* [Translate][#translate]
* [Comment][#comment]
* [Send Message][#twilio]
<img src="/static/img/Screenshots/TranslationButton.png" alt="Translation Button Screenshot"/>

####<a name="translate"></a>Translate
If the user clicks the "Translate" Button, a call is made to Google Translate API and the translation is displayed in the popover. The phrase and translation are also stored in the database.
<img src="/static/img/Screenshots/TranslationPopover.png" alt="Translation Popover Screenshot"/>

####<a name="comment"></a>Comments
If the user finds a phrase that might be an idiom or perhaps a phrase that might require additional context, they could chose to click the "Comment" Button. 
<img src="/static/img/Screenshots/CommentButton.png" alt="Comment Button Screenshot"/>

A comment window will display in-line with the selection. When the user makes a comments, a grey rectangle will appear over the phrase that has an attached comment. These comments are viewable to other users who read the same article. 
<img src="/static/img/Screenshots/CommentLinkWindow.png" alt="Comment Link Screenshot"/>

Once comments are made, the user can click the words inside of the grey rectangle to view the comments.
<img src="/static/img/Screenshots/CommentLink.png" alt="Parrot Loginpage Screenshot"/> 

The user can even see older comments made by other users and comment back to them. 
<img src="/static/img/Screenshots/ArticleComments.png" alt="Article Comments Screenshot"/>

####<a name="twilio"></a>Send Message
If the user is reading and wants to remember the new phrase they have learned and study on-the-go, they can send a text message to their mobile device containing the origin phrase and its translation. 
<img src="/static/img/Screenshots/TwilioButton.png" alt="Twilio Button Screenshot"/>
<img src="/static/img/Screenshots/TwilioMessage.png" alt="Twilio Message Screenshot"/>











