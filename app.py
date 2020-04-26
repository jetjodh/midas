import os
import sys
import psaw
import json

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
#import tensorflow_text
import timestamp
# Some utilites
import numpy as np
from psaw import PushshiftAPI
cat = ['author_patreon_flair','author_premium','can_mod_post','contest_mode',
                             'is_crosspostable','is_meta','is_original_content','is_reddit_media_domain',
                             'is_robot_indexable','is_self','is_video','locked','media_only','no_follow',
                             'parent_whitelist_status','pinned','post_hint','removed_by_category',
                             'send_replies','stickied','whitelist_status','author_cakeday','thumbnail',
                             'spoiler','locked','over_18','is_original_content','is_self',
                           'poll_data','removed_by','banned_by','hidden','brand_safe']
num = ['gilded','score','total_awards_received','num_crossposts','num_comments']                           

the_list = ['AskIndia','Non-Political','Scheduled','Photography','Science/Technology','Politics','Business/Finance','Policy/Economy','Sports','Food','[R]eddiquette']
api = PushshiftAPI()
punctuation = '!"#$%&()*+-/:;<=>?@[\\]^_`{|}~'

def getUrltokens(input):
    tokens_1 = str(input.encode('utf-8')).split('/')
    alls = []
    for i in tokens_1:
        tokens = str(i).split('-')
        dots = []
        for j in range(0,len(tokens)):
            temp = str(tokens[j]).split('.')
            dots = dots + temp
        alls = alls + tokens + dots
    all_tok = list(set(alls))
    if 'html' in all_tok:
        all_tok.remove('html')
    if 'https' in all_tok:
        all_tok.remove('https')    
    return ' '.join(all_tok)

# Declare a flask app
app = Flask(__name__)

def collectSubData(subd):
    subm = getPushshiftData(subd)
    subData = list() 
    title = subm['title']
    url = subm['url']
    domain = subm['domain']
    cate = []
    for i in cat:
        cate.append(subm[i])

    nums = []
    for i in num:
        nums.append(subm[i])

    return cate, nums, title, domain, url

def getPushshiftData(query):
    before = timestamp.now()
    url = 'https://api.pushshift.io/reddit/search/submission/?title='
    +str(query)+'&size=1000&'+'&before='+str(before)
    +'&subreddit=india'
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = r'D:\Projects\webapp\modelz\megav1_3.h5'

#   Loading trained model
model = tf.keras.models.load_model(MODEL_PATH)
#model._make_predict_function()          
print('Model loaded. Start serving...')


def model_predict(url, model):

    cate, nums, title, domain, url = collectSubData(url)
    # Preprocessing the data
    x = cate*1
    x = np.asarray(x).astype(np.float32)
    nums = np.asarray(nums).astype(np.float32)
    title = title.apply(lambda x: ''.join(ch for ch in x if ch not in set(punctuation)))
    title = title.str.lower()
    title = title.apply(lambda x:' '.join(x.split()))

    url =  url.apply(getUrltokens)
    domain =  domain.apply(getUrltokens)
    url = url.str.replace("[0-9]", " ")
    domain = domain.str.replace("[0-9]", " ")

    url = url.apply(lambda x: ''.join(ch for ch in x if ch not in set(punctuation)))
    domain = domain.apply(lambda x: ''.join(ch for ch in x if ch not in set(punctuation)))
    domain = np.asarray(domain)
    url = np.asarray(url)

    preds = model.predict_classes(cat,x,title,domain,url)
    pred = the_list[preds]
    return pred

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the url from post request
        url = request.json
        # Getting input data for model
        result = api.search_submissions(q = url,subreddit='india',limit=1)
        pred = collectSubData(result)
        # Make prediction
        preds = model_predict(url, model)
        # Serialize the result
        return jsonify(result=preds)

    return None

@app.route('/automated_testing', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':
        file = request.files['upload_file']
        lines = file.readlines()
        
        flairs = dict()
        for line in lines:
            url = line.decode()
            pred = model_predict(url,model)
            flairs[url] = pred
        flairs = json.dumps(flairs) 
        flairs = json.loads(flairs) 
        return flairs

if __name__ == '__main__':

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0'), app)
    http_server.serve_forever()
