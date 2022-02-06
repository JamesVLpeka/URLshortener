

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mizourl.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short



#function to short the URL
def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        random_letters = random.choices(letters, k = 3)
        random_letters = "".join(random_letters)
        short_url = Urls.query.filter_by(short = random_letters).first()
        if not short_url:
            return random_letters

@app.route('/', methods=['Post','Get'])
def home():
    if request.method == 'POST':
        url_received = request.form["url_input"]
        #check if url already exist in database
        found_url = Urls.query.filter_by(long=url_received).first()
        
        if found_url:
            #return short url if found
            #return redirect(url_for("display_short_url", url=found_url.short))
            finalUrl = "127.0.0.1:5000/"+found_url.short #here
            return render_template('index.html', shortUrl = finalUrl)
        else:
            #create short url if not found
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            # return redirect(url_for("display_short_url", url=short_url))
            finalUrl = "127.0.0.1:5000/"+short_url #here
            return render_template('index.html', shortUrl = finalUrl)

    else:
        return render_template('index.html')
   
@app.route('/<short_url>')
def redirection(short_url):
    original_url = Urls.query.filter_by(short=short_url).first()
    if original_url:
        return redirect(original_url.long)
    else:
        return render_template('index.html', url_not_exist = "The URL you entered does not exist")

if __name__== '__main__':
    app.run(port=5000, debug=True) 
