import numpy as np
import pandas as pd
import pickle
from flask import Flask, jsonify, render_template, request,redirect 
from flask_ngrok import run_with_ngrok
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import h5py
from keras.models import load_model
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# load the dataset but only keep the top n words, zero the rest
top_words = 10000
max_words = 500

#load the csv file saved

df = pd.read_csv('./data/movie_data.csv', encoding='utf-8')

tokenizer_obj = Tokenizer(num_words=top_words)
tokenizer_obj.fit_on_texts(df.loc[:50000, 'review'].values)

def pred(usermoviereview):
    test_samples = [usermoviereview]
    review_tokens = tokenizer_obj.texts_to_sequences(test_samples)
    review_tokens_pad = pad_sequences(review_tokens, maxlen=max_words)

    print("call predict")
    # Load in pretrained model
    loaded_model = load_model('./models/movie_sa_model.h5')
    print("Loaded model from disk")
    sentiment = loaded_model.predict(x=review_tokens_pad)
    print(sentiment)
    if sentiment[0] > 0.5:
        sentiment_s = float(sentiment[0])
    else:
        sentiment_s = float(sentiment[0])
    return sentiment_s

# webapp
app = Flask(__name__, template_folder='./') 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/my_data'

db = SQLAlchemy(app)

run_with_ngrok(app)

class shakuntala(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.DateTime, default = datetime.now)

class chhalaang(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.DateTime, default = datetime.now)

class harry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.DateTime, default = datetime.now)

class avengers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.DateTime, default = datetime.now)

class laxmii(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Float)
    date_entered = db.Column(db.DateTime, default = datetime.now)

def shakuntala_rev(request):
    sentiment_s = pred(request.form['message'])
    rev = shakuntala(name=request.form['name'], review=request.form['message'], percent=sentiment_s)
    db.session.add(rev)
    db.session.commit()


def hp_rev(request):
    sentiment_s = pred(request.form['message'])
    rev = harry(name=request.form['name'], review=request.form['message'], percent=sentiment_s)
    db.session.add(rev)
    db.session.commit()


def avengers_rev(request):
    sentiment_s = pred(request.form['message'])
    rev = avengers(name=request.form['name'], review=request.form['message'], percent=sentiment_s)
    db.session.add(rev)
    db.session.commit()


def laxmii_rev(request):
    sentiment_s = pred(request.form['message'])
    rev = laxmii(name=request.form['name'], review=request.form['message'], percent=sentiment_s)
    db.session.add(rev)
    db.session.commit()



def chhalaang_rev(request):
    sentiment_s = pred(request.form['message'])
    rev = chhalaang(name=request.form['name'], review=request.form['message'], percent=sentiment_s)
    db.session.add(rev)
    db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def main():
   
    if request.method == "POST":
        if 'sd' in request.form:
            shakuntala_rev(request)
            sdf = shakuntala.query.all()
            return render_template("home.html", revs1=sdf)
        if 'hp' in request.form:
            hp_rev(request)
            sdf = harry.query.all()
            return render_template("home.html", revs2=sdf)
        if 'av' in request.form:
            avengers_rev(request)
            sdf = avengers.query.all()
            return render_template("home.html", revs3=sdf)
        if 'ch' in request.form:
            chhalaang_rev(request)
            sdf = chhalaang.query.all()
            return render_template("home.html", revs4=sdf)
        if 'laxmii' in request.form:
            laxmii_rev(request)
            sdf = laxmii.query.all()
            return render_template("home.html", revs5=sdf)
        
    return render_template('home.html')





if __name__ == '__main__':
    app.run()
