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
import pytz
import math

local_tz = pytz.timezone('Asia/Calcutta')

# load the dataset but only keep the top n words, zero the rest
top_words = 10000
max_words = 500

#load the csv file saved

df = pd.read_csv('./data/movie_data.csv', encoding='utf-8')
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%A %d %B %Y %H:%M:%S')


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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

run_with_ngrok(app)

class shakuntala(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))

class chhalaang(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))

class harry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))

class avengers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))

class laxmii(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Float)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))

def shakuntala_rev(request):
    sentiment_s = pred(str(request.form['message']))
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


def truncate(number) -> float:
    stepper = 10
    return math.trunc(stepper * number) / stepper

@app.route('/', methods=['POST', 'GET'])
def main():
    
    avg_sd = 0
    avg_ch = 0
    avg_hp = 0
    avg_av = 0
    avg_lx = 0
    sdf = shakuntala.query.all()
    count = 0
    for q in sdf:
        avg_sd += q.percent
        count += 1
    if count != 0:
        avg_sd /= count
        avg_sd *= 10

    sdf2 = chhalaang.query.all()
    count = 0
    for q in sdf:
        avg_ch += q.percent
        count += 1
    if count != 0:
        avg_ch /= count
        avg_ch *= 10

    sdf3 = avengers.query.all()
    count = 0
    for q in sdf3:
        avg_av += q.percent
        count += 1
    if count != 0:
        avg_av /= count
        avg_av *= 10

    sdf4 = harry.query.all()
    count = 0
    for q in sdf4:
        avg_hp += q.percent
        count += 1
    if count != 0:
        avg_hp /= count
        avg_hp *= 10

    sdf5 = laxmii.query.all()
    count = 0
    for q in sdf5:
        avg_lx += q.percent
        count += 1
    if count != 0:
        avg_lx /= count
        avg_lx *= 10
    
    avg_sd = truncate(avg_sd)
    avg_ch = truncate(avg_ch)
    avg_av = truncate(avg_av)
    avg_hp = truncate(avg_hp)
    avg_lx = truncate(avg_lx)

    avg_sd_int = int(avg_sd)
    avg_ch_int = int(avg_ch)
    avg_av_int = int(avg_av)
    avg_hp_int = int(avg_hp)
    avg_lx_int = int(avg_lx)


    if request.method == "POST":
        sdf = shakuntala.query.all()
        count = 0
        avg_sd = 0
        for q in sdf:
            avg_sd += q.percent
            count += 1
        if count != 0:
            avg_sd /= count
            avg_sd *= 10

        sdf2 = chhalaang.query.all()
        count = 0
        avg_ch = 0

        for q in sdf:
            avg_ch += q.percent
            count += 1
        if count != 0:
            avg_ch /= count
            avg_ch *= 10

        sdf3 = avengers.query.all()
        count = 0
        avg_av = 0
        for q in sdf3:
            avg_av += q.percent
            count += 1
        if count != 0:
            avg_av /= count
            avg_av *= 10

        sdf4 = harry.query.all()
        count = 0
        avg_hp = 0
        for q in sdf4:
            avg_hp += q.percent
            count += 1
        if count != 0:
            avg_hp /= count
            avg_hp *= 10

        sdf5 = laxmii.query.all()
        count = 0
        avg_lx = 0
        for q in sdf5:
            avg_lx += q.percent
            count += 1
        if count != 0:
            avg_lx /= count
            avg_lx *= 10
        
        avg_sd = truncate(avg_sd)
        avg_ch = truncate(avg_ch)
        avg_av = truncate(avg_av)
        avg_hp = truncate(avg_hp)
        avg_lx = truncate(avg_lx)

        avg_sd_int = int(avg_sd)
        avg_ch_int = int(avg_ch)
        avg_av_int = int(avg_av)
        avg_hp_int = int(avg_hp)
        avg_lx_int = int(avg_lx)
        if 'sd' in request.form:
            shakuntala_rev(request)

            sdf = shakuntala.query.all()
            count = 0
            avg_sd = 0
            for q in sdf:
                avg_sd += q.percent
                count += 1
            if count != 0:
                avg_sd /= count
                avg_sd *= 10
            sdf2 = chhalaang.query.all()
            sdf3 = avengers.query.all()
            sdf4 = harry.query.all()
            sdf5 = laxmii.query.all()

            avg_sd = truncate(avg_sd)
            avg_sd_int = int(avg_sd)

            return render_template("home.html", revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int)
        if 'hp' in request.form:
            hp_rev(request)
            sdf = shakuntala.query.all()
            sdf2 = chhalaang.query.all()
            sdf3 = avengers.query.all()
            sdf4 = harry.query.all()
            count = 0
            avg_hp = 0
            for q in sdf4:
                avg_hp += q.percent
                count += 1
            if count != 0:
                avg_hp /= count
                avg_hp *= 10
            sdf5 = laxmii.query.all()

            avg_hp = truncate(avg_hp)
            
            avg_hp_int = int(avg_hp)
            return render_template("home.html",revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int)
        if 'av' in request.form:
            avengers_rev(request)
            sdf = shakuntala.query.all()
            sdf2 = chhalaang.query.all()
            sdf3 = avengers.query.all()
            count = 0
            avg_av = 0
            for q in sdf3:
                avg_av += q.percent
                count += 1
            if count != 0:
                avg_av /= count
                avg_av *= 10
            sdf4 = harry.query.all()
            sdf5 = laxmii.query.all()


            avg_av = truncate(avg_av)
            avg_av_int = int(avg_av)
            return render_template("home.html", revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int)
        if 'ch' in request.form:
            chhalaang_rev(request)
            sdf = shakuntala.query.all()
            sdf2 = chhalaang.query.all()
            count = 0
            avg_ch = 0
            for q in sdf2:
                avg_ch += q.percent
                count += 1
            if count != 0:
                avg_ch /= count
                avg_ch *= 10
            sdf3 = avengers.query.all()
            sdf4 = harry.query.all()
            sdf5 = laxmii.query.all()

            avg_ch = truncate(avg_ch)
            avg_ch_int = int(avg_ch)
            
            return render_template("home.html", revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int)
        if 'laxmii' in request.form:
            laxmii_rev(request)
            sdf = shakuntala.query.all()
            sdf2 = chhalaang.query.all()
            sdf3 = avengers.query.all()
            sdf4 = harry.query.all()
            sdf5 = laxmii.query.all()
            count = 0
            avg_lx = 0
            for q in sdf5:
                avg_lx += q.percent
                count += 1
            if count != 0:
                avg_lx /= count
                avg_lx *= 10

            avg_lx = truncate(avg_lx)
            avg_lx_int = int(avg_lx)
            return render_template("home.html",revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int)
    
    return render_template('home.html',revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5, avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int)





if __name__ == '__main__':
    app.run()
