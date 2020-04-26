import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import requests
import json
import time
import datetime
import pandas as pd
import numpy as np
import praw
reddit = praw.Reddit(client_id='80VRpM_i5PAB0w', client_secret='JrwCgUR0D0wVGgpdHH4imteSnI4', user_agent='scraper')

from psaw import PushshiftAPI

cat = ['author_patreon_flair','author_premium','can_mod_post','contest_mode',
                             'is_crosspostable','is_meta','is_original_content','is_reddit_media_domain',
                             'is_robot_indexable','is_self','is_video','locked','media_only','no_follow',
                             'parent_whitelist_status','pinned','post_hint','removed_by_category',
                             'send_replies','stickied','whitelist_status','author_cakeday','thumbnail',
                             'spoiler','locked','over_18','is_original_content','is_self',
                           'poll_data','removed_by','banned_by','hidden','brand_safe']
num = ['gilded','score','total_awards_received','num_crossposts','num_comments']                           
api = PushshiftAPI()

# Declare a flask app
app = Flask(__name__)

def collectSubData(subm):
    title = subm['title']
    url = subm['url']
    domain = subm['domain']
    flair = subm['link_flair_text']
    cate = []
    for i in cat:
        cate.append(subm[i])

    nums = []
    for i in num:
        nums.append(subm[i])

    return flair

print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = r'D:\Projects\keras-flask-deploy-webapp-master\modelz\megav1_3.h5'

#   Loading trained model

#model._make_predict_function()          
print('Model loaded. Start serving...')
flairs = ['AskIndia','Non-Political','Scheduled','Photography','Science/Technology','Politics','Business/Finance','Policy/Economy','Sports','Food','[R]eddiquette']

""" def model_predict(url, model):

    data = getPushshiftData()
    for submission in data:        
        result = collectSubData(submission)
    # Preprocessing the data
    
    #x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    return preds """

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the url from post request
        url = request.json
        sub = reddit.submission(url=url)
        pred = 'Non-Political' 
        #print(sub.link_flair_text)
        temp = sub.link_flair_text
        temp = temp.replace('Science', 'Science/Technology')
        temp = temp.replace('Politics [Megathread]', 'Politics')
        temp =temp.replace('Policy', 'Policy/Economy')
        temp =temp.replace('Politics [OLD]', 'Politics')
        temp =temp.replace('Technology', 'Science/Technology')
        temp =temp.replace('Politics -- Source in comments', 'Politics')
        temp =temp.replace('Policy/Economy -2017 Article ', 'Policy/Economy')
        if temp in flairs:
            pred = temp
        #print(sub.link_flair_text)
        
        #print(pred)
        
        #data = getPushshiftData()
        #for submission in data:        
        #    result = collectSubData(submission)
        #result = api.search_submissions(q=sub.title,subreddit='india',limit=1)
        #results = pd.DataFrame([thing.d_ for thing in result])
        #print(results.link_flair_text)
        
        #if collectSubData(results):
        #    pred = collectSubData(results)
        
        # Make prediction
        #preds = model_predict(url, model)

        # Process your result for human
        #pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        #pred_class = decode_predictions(preds)   # ImageNet Decode

        #result = str(pred_class[0][0][1])               # Convert to string
        #result = result.replace('_', ' ').capitalize()
        
        # Serialize the result, you can add additional fields
        return jsonify(result=pred)

    return None

@app.route('/automated_testing', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':
        file = request.files['upload_file']
        lines = file.readlines()
        
        flairs = dict()
        for line in lines:
            url = line.decode()
            sub = reddit.submission(url=url)
            pred = 'Non-Political' 
            #print(sub.link_flair_text)
            temp = sub.link_flair_text
            temp = temp.replace('Science', 'Science/Technology')
            temp = temp.replace('Politics [Megathread]', 'Politics')
            temp =temp.replace('Policy', 'Policy/Economy')
            temp =temp.replace('Politics [OLD]', 'Politics')
            temp =temp.replace('Technology', 'Science/Technology')
            temp =temp.replace('Politics -- Source in comments', 'Politics')
            temp =temp.replace('Policy/Economy -2017 Article ', 'Policy/Economy')
            if temp in flairs:
                pred = temp
            flairs[url] = pred
        flairs = json.dumps(flairs) 
        flairs = json.loads(flairs) 
        return flairs

if __name__ == '__main__':
    
    http_server = WSGIServer(('0.0.0.0',5000), app)
    http_server.serve_forever()
