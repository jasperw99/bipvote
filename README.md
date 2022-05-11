# bipvote
## Table of contents

- [Quick start](#quick-start)
- [Status](#status)
- [What's included](#whats-included)
- [Bugs and feature requests](#bugs-and-feature-requests)
- [Contributing](#contributing)
- [Creators](#creators)
- [Thanks](#thanks)
- [Copyright and license](#copyright-and-license)


## Quick start
### Prerequisites
For this project to work you need to install the following prerequisites:
- [Django](https://docs.djangoproject.com/en/4.0/intro/install/) as our main framework
- [PostgreSQL](https://www.postgresql.org/download/) for our database
- [Psycopg2](https://docs.djangoproject.com/en/4.0/ref/databases/#postgresql-notes-1) for integrating PostgreSQL with Django

### Set-up
The first thing you need to do is set up a PostgeSQL-database with the credentials from Django's `settings.py`. The password for the database is loaded from `secret_key_db.txt` which needs to be created in the same folder as `manage.py`, here we also need to create a file for Django's secret key as `secret_key.txt`. 

Last thing to make the dashboard itself work locally is to set up a folder which can be accessed from the web with [Apache](https://www.apache.org/) or some other webserver. You need to create two folders `/var/www/ict4d/opinions/` for storing the audio files and `/var/www/ict4d/public_img/` for storing your VoiceXML files. 

When this is all set up, the dashboard itself should work. To test this you can set `DEBUG = True` in `settings.py` and run the following command to start a Django server: 
> `python3 manage.py runserver`
 
 Now the dashboard works, we should set up the server part of our application. It is preferable to run our service on a VPS with it's own IP-address to make it easier to deploy it. We used Apache as a reverse proxy to make our whole website available to the internet, but in a real use-case it is preferable to keep the dashboard itself local and only make the page to access the POST-requests for voting public. This is due to the fact that everyone can access the dashboard and listen to the opinions as well as creating new topics, which is undesirable.
 
 Changes need to be made to the `.vxml` files to put in the IP-address of your server, also the `ALLOWED_HOSTS` in `settings.py` need to be altered. If you have set the URLS to the right values the dashboard should now work.
 
 ## Usage
<img src="bipvote.ml/public_img/dashboard.png"/>
The usage of the dashboard is quite straightforward, in the *Topics* tab you can create a new topic for your radio broadcast. From that point on the votes will be counted for this topic, the results will be plot in a pie chart. When a listener also drops an opinion to strenghten their vote, they can be listened from the two columns at the bottom. The most recent opinions are shown at top with a timestamp.
