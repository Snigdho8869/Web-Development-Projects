from flask import Flask, send_file, jsonify, flash, session, render_template, redirect, url_for,request, make_response, get_flashed_messages, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import InputRequired, Length, EqualTo, Email, DataRequired, NumberRange, ValidationError
from email_validator import validate_email, EmailNotValidError
from flask_mysqldb import MySQL
import os
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import smtplib
import tensorflow
import keras
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
import pickle
import io
import tensorflow_hub as hub
from PIL import Image
import cv2
import PIL.Image
import urllib.parse
import string
import pyshorteners
import qrcode
import base64
from gtts import gTTS
from PIL import Image, ImageFilter
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
import re
import nltk
import pandas as pd
import joblib
import json
import random
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from textblob import Word
import torch
from transformers import BartForConditionalGeneration, BartTokenizer, T5ForConditionalGeneration, T5Tokenizer, GPT2LMHeadModel,GPT2Tokenizer




app = Flask(__name__, template_folder='templates', static_folder='static')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'braindive'
mysql = MySQL(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'
tasks = []

'''
# Language Detection
model_language_detection = load_model('language_detection/language_detection.h5')

with open('language_detection/PipelineModel.pickle', 'rb') as handle:
    PipelineModel = pickle.load(handle)

with open('language_detection/dict.pickle', 'rb') as handle:
    dict = pickle.load(handle)
'''

'''
# Text Summarization
models = {
    'bart': BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn'),
    'gpt': GPT2LMHeadModel.from_pretrained('gpt2'),
}

tokenizers = {
    'bart': BartTokenizer.from_pretrained('facebook/bart-large-cnn'),
    'gpt': GPT2Tokenizer.from_pretrained('gpt2'),
}
'''

'''
# Pneumonia Detection
pneumonia_model = load_model('pneumonia_detection/pneumonia.h5')
app.config['PNEUMONIA_UPLOAD_FOLDER'] = 'pneumonia_detection/uploads'
'''

''''
# Multclass Text Classification
multiclass_text_classification_model = joblib.load('multiclass_text_classification/Text_LR.pkl')
multiclass_text_classification_count_vec = joblib.load('multiclass_text_classification/count_vect.pkl')
multiclass_text_classification_transformer = joblib.load('multiclass_text_classification/transformer.pkl')
'''

'''
# Traffic Sign Detector
app.config['TRAFFIC_UPLOAD_FOLDER'] = 'traffic_sign_detector/uploads'
traffic_model = load_model('traffic_sign_detector/traffic_resnet50.h5')
traffic_df = pd.read_csv('traffic_sign_detector/label_names.csv')
'''

'''
#Cataract
app.config['CATARACT_UPLOAD_FOLDER'] = 'cataract/uploads'
cataract_model = load_model('cataract/cataract_tl.h5')
'''

'''
# Suicide Ideation
suicide_ideation_model = load_model('suicide_ideation/Twitter_Suicidal_Ideation_Detection_GRU.h5')
with open('suicide_ideation/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
'''

'''
#Spam Message Detection
spam_message_detector_model = joblib.load('spam_message_detector/spam_svm.pkl')
transformer = joblib.load('spam_message_detector/tfidf.pkl')
'''


UPLOAD_FOLDER = 'static/profile_pic'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password, first_name, last_name, email, phone_number, blood_group, favorite_number, picture, gender, address, date_of_birth, cash, bank, savings, credit_cards, lifetime_balance, lifetime_spending):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.blood_group = blood_group
        self.favorite_number = favorite_number
        self.picture = picture
        self.gender = gender
        self.address = address
        self.date_of_birth = date_of_birth
        self.cash = cash
        self.bank = bank
        self.savings = savings
        self.credit_cards = credit_cards
        self.lifetime_balance = lifetime_balance
        self.lifetime_spending = lifetime_spending


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')



class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    blood_group = StringField('Blood Group', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    favorite_number = IntegerField('Favorite Number', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')


class ResetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    favorite_number = IntegerField('Favorite Number', validators=[InputRequired()])
    new_password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Reset')


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        user = User(id=user_data[0], username=user_data[3], password=user_data[7], first_name=user_data[1], last_name=user_data[2], email=user_data[4], phone_number=user_data[5], blood_group=user_data[6], favorite_number=user_data[8], picture=user_data[9], gender=user_data[10], address=user_data[11], date_of_birth=user_data[12], cash=user_data[13], bank=user_data[14], savings=user_data[15], credit_cards=user_data[16], lifetime_balance=user_data[17], lifetime_spending=user_data[18])
        return user
    return None




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        phone_number = form.phone_number.data
        blood_group = form.blood_group.data
        password = form.password.data
        favorite_number = form.favorite_number.data
        gender = form.gender.data
        address = form.address.data
        date_of_birth = form.date_of_birth.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, username, email, phone_number, blood_group, password, favorite_number, gender, address, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, username, email, phone_number, blood_group, password, favorite_number, gender, address, date_of_birth))
        mysql.connection.commit()
        cur.close()
        flash('You have been successfully registered', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/check_username/<username>')
def check_username(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", [username])
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [username])
        user_data = cur.fetchone()
        cur.close()
        if user_data and user_data[7] == password:
            user = User(id=user_data[0], username=user_data[3], password=user_data[7], first_name=user_data[1], last_name=user_data[2], email=user_data[4], phone_number=user_data[5], blood_group=user_data[6], favorite_number=user_data[8],picture=user_data[9], gender=user_data[10], address=user_data[11], date_of_birth=user_data[12], cash=user_data[13], bank=user_data[14], savings=user_data[15], credit_cards=user_data[16], lifetime_balance=user_data[17], lifetime_spending=user_data[18])
            login_user(user)
            flash('Login success', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password.', 'error')
            
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logout successfully', 'success')
    return redirect(url_for('login'))

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        favorite_number = form.favorite_number.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT favorite_number FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        if result is None:
            flash('Username is incorrect! Please try again.', 'danger')
            return redirect(url_for('reset_password'))
        user_favorite_number = result[0]
        if favorite_number != user_favorite_number:
            flash('Favorite number is incorrect! Please try again.', 'danger')
            return redirect(url_for('reset_password'))
        cur.execute("UPDATE users SET password = %s WHERE username = %s AND favorite_number = %s", (new_password, username, favorite_number))
        mysql.connection.commit()
        cur.close()
        flash('Password reset successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)




@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT video_file_name, video_title FROM videos_information")
    video_info = cur.fetchall()
    cur.close()
    return render_template('home.html', video_info=video_info, user=current_user)




@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/profile_custom/<string:username>', methods=['GET', 'POST'])
@login_required
def profile_custom(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", [username])
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return render_template('profile_from_search.html', user=user_data)




@app.route('/upload_picture', methods=['POST'])
@login_required
def upload_picture():
    file = request.files['picture']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET picture=%s WHERE id=%s", [filename, current_user.id])
        mysql.connection.commit()
        cur.close()
        flash('Picture uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload a picture with one of the following extensions: jpg, jpeg, png, gif', 'error')
    return redirect(url_for('profile')) 


@app.route('/upload_video', methods=['POST'])
def upload_video():
    title = request.form['title']
    video_file = request.files['video']
    video_filename = video_file.filename
    video_file.save(os.path.join('static/videos', video_filename))
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO videos_information (video_file_name, video_title) VALUES (%s, %s)", (video_filename, title))
    mysql.connection.commit()
    cur.close()
    flash('Video uploaded successfully!', 'success')
    return redirect(url_for('home'))



@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE users SET email = %s, phone_number = %s, favorite_number = %s, address = %s WHERE id = %s', (
        request.form['email'],
        request.form['phone_number'],
        request.form['favorite_number'],
	request.form['address'],
        current_user.id
    ))
    mysql.connection.commit()
    cursor.close()
    flash('Profile Edited successfully', 'success')
    return redirect(url_for('profile'))




@app.route('/search', methods=['POST'])
@login_required
def search():
    blood_group = request.form['blood_group']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE blood_group = %s", [blood_group])
    users = cur.fetchall()
    cur.close()
    return render_template('search_results.html', users=users)

@app.route('/search_results_tables/<string:blood_group>')
@login_required
def search_results_tables(blood_group):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE blood_group = %s", [blood_group])
    users = cur.fetchall()
    cur.close()
    return render_template('search_results_table.html', users=users)



@app.route('/search_results_for_location')
def search_results_for_location():
    address_query = request.args.get('address_query')
    blood_group = request.args.get('blood_group')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    users = [user for user in users if user[6] == blood_group]

    if address_query:
        users = [user for user in users if address_query.lower() in user[11].lower()]

    return render_template('search_results_for_location.html', users=users)




@app.route('/suicide', methods=['GET', 'POST'])
@login_required
def suicide():
    return render_template('suicide_ideation.html')

'''
@app.route('/suicide-ideation', methods=['POST'])
@login_required
def predict():
    text = request.json['text']
    if not text:
        predictionText='Please Enter Some Text'
        response = jsonify({'predictionText': predictionText})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    twt = tokenizer.texts_to_sequences([text])
    twt = pad_sequences(twt, maxlen=60, dtype='int32')
    
    predicted = suicide_ideation_model.predict(twt, batch_size=1, verbose=True)
    
    if np.argmax(predicted) == 0:
        predictionText = 'Potential Suicide Post'
    elif np.argmax(predicted) == 1:
        predictionText = 'Non Suicide Post'
    else:
        predictionText = 'Unknown'
    
    response = jsonify({'prediction': float(predicted[0][0]), 'predictionText': predictionText})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response
'''



@app.route('/NST', methods=['GET', 'POST'])
@login_required
def NST():
    return render_template('style_transfer.html')

'''
@app.route('/style-transfer', methods=['GET', 'POST'])
@login_required
def stylize_image():
    if request.method == 'POST':
        STYLE_IMAGE_NAME = request.form['style_image_name']
      
        corresponding_url = {
            'IMAGE_1': 'https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg',
            'IMAGE_2': 'https://storage.googleapis.com/khanhlvg-public.appspot.com/arbitrary-style-transfer/style23.jpg',
            'IMAGE_3': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/1024px-Tsunami_by_hokusai_19th_century.jpg',
            'IMAGE_4': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg/800px-Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg',
            'IMAGE_5': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/757px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg',
            'IMAGE_6': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project_%28454045%29.jpg/220px-Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project_%28454045%29.jpg',
	          'IMAGE_7': 'https://images.squarespace-cdn.com/content/v1/5511fc7ce4b0a3782aa9418b/1429331653608-5VZMF2UT2RVIUI4CWQL9/abstract-art-style-by-thaneeya.jpg',
	          'IMAGE_8': 'https://www.artmajeur.com/medias/standard/l/a/laurent-folco/artwork/14871329_a75fb86e-1a71-4559-a730-5cd4df09f0c4.jpg',
	          'IMAGE_9': 'https://s3.amazonaws.com/gallea.arts.bucket/e36461e0-551c-11eb-b1d7-c544bb4e051b.jpg',
	          'IMAGE_10': 'https://www.homestratosphere.com/wp-content/uploads/2019/10/Raster-painting-example-woman-oct16.jpg',
	          'IMAGE_11': 'https://images.saatchiart.com/saatchi/419137/art/8609262/additional_f1bab706e54c28c8c824a31008ffd5a34f640806-AICC2-8.jpg',
	          'IMAGE_12': 'https://static01.nyt.com/images/2020/10/23/arts/21lawrence/21lawrence-superJumbo.jpg'
        }

        style_image_path = tf.keras.utils.get_file(
            STYLE_IMAGE_NAME + ".jpg", corresponding_url[STYLE_IMAGE_NAME])
        global content_image
        content_image = Image.open(io.BytesIO(request.files['content_image'].read()))
        img = content_image.convert('RGB')
        img.thumbnail((256, 256))
        img.save('style_transfer/content.jpg')
        content_image = np.array(content_image)

        def load_img(path_to_img):
         max_dim = 512
         img = tf.io.read_file(path_to_img)
         img = tf.image.decode_image(img, channels=3)
         img = tf.image.convert_image_dtype(img, tf.float32)
         
         shape = tf.cast(tf.shape(img)[:-1], tf.float32)
         long_dim = max(shape)
         scale = max_dim / long_dim
         
         new_shape = tf.cast(shape * scale, tf.int32)
         img = tf.image.resize(img, new_shape)
         img = img[tf.newaxis, :]
         return img 

        def tensor_to_image(tensor):
          tensor = tensor*255
          tensor = np.array(tensor, dtype=np.uint8)
          if np.ndim(tensor)>3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
          return PIL.Image.fromarray(tensor)  
        content_image_path="style_transfer/content.jpg"
        content_image = load_img(content_image_path)
        style_image = load_img(style_image_path)

        hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

        stylized_image = hub_model(tf.constant(content_image ), tf.constant(style_image))[0]
        stylized_image = tensor_to_image(stylized_image)
        stylized_image.save('static/NST/NST_image.jpeg')
       
        return render_template('style_transfer_result.html')
'''



@app.route('/spam', methods=['GET', 'POST'])
@login_required
def spam():
    return render_template('spam_detector.html')

'''
@app.route('/spam-detector', methods=['POST'])
@login_required
def spredict():
    data = request.get_json(force=True)
    text = data['text']
    
    text_df = pd.DataFrame({'text': [text]})
    text_df['text'] = text_df['text'].apply(lambda x: x.lower().strip().replace('\n', ' ').replace('\r', ' '))
    text_df['text'] = text_df['text'].str.replace(r'^.+@[^\.].*\.[a-z]{2,}$', 'emailaddress', regex=True)
    text_df['text'] = text_df['text'].str.replace(r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$', 'webaddress', regex=True)
    text_df['text'] =  text_df['text'].str.replace(r'£|\$', 'moneysymb', regex=True)
    text_df['text'] =  text_df['text'].str.replace(r'^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$','phonenumbr', regex=True)
    text_df['text'] =  text_df['text'].str.replace(r'\d+(\.\d+)?', 'numbr', regex=True)
    text_df['text'] =  text_df['text'].str.replace(r'[^\w\d\s]', ' ', regex=True)
    text_df['text'] =  text_df['text'].str.replace(r'\s+', ' ', regex=True)
    text_df['text'] =  text_df['text'].str.replace(r'^\s+|\s+?$', '', regex=True)
    stops = stopwords.words('english')
    text_df['text'] =  text_df['text'].apply(lambda x: ' '.join(term for term in x.split() if term not in stops))
    text_df['text'] = text_df['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    text_vec = transformer.transform([text_df['text'][0]])
  
    prediction = spam_message_detector_model.predict(text_vec)
    prediction_list = prediction.tolist()
    response_dict = {'category': prediction_list}
    response_json = json.dumps(response_dict)
    response = app.response_class(response=response_json, status=200, mimetype='application/json')
    
    return response
'''


@app.route('/traffic', methods=['GET', 'POST'])
@login_required
def traffic():
    return render_template('traffic_sign_detector.html')

'''
@app.route('/traffic_predict', methods=['GET', 'POST'])
def traffic_predict():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file_path = os.path.join(app.config['TRAFFIC_UPLOAD_FOLDER'], filename)
        file.save(file_path)

        img = cv2.imread(file_path)
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0

        pred = traffic_model.predict(np.expand_dims(img, axis=0), verbose=False)[0].argmax()
        classid_value = pred
        filtered_df = traffic_df[traffic_df['ClassId'] == classid_value]
        signature = filtered_df['Name'].values[0]

        response = {'signature': signature}
        return jsonify(response)
    return render_template('trafic_sign_detector.html')
'''



@app.route('/multiclass_text', methods=['GET', 'POST'])
@login_required
def multiclass_text():
    return render_template('multiclass-text-classification.html')

'''
@app.route('/multiclass_text_classification_predict', methods=['POST'])
def multiclass_text_classification_predict():
    data = request.get_json(force=True)
    text = data['text']
    
    text_df = pd.DataFrame({'text': [text]})
    text_df['lower_case'] = text_df['text'].apply(lambda x: x.lower().strip().replace('\n', ' ').replace('\r', ' '))
    text_df['alphabetic'] = text_df['lower_case'].apply(lambda x: re.sub(r'[^a-zA-Z\']', ' ', x)).apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', x))
    tokenizer = RegexpTokenizer(r'\w+')
    text_df['special_word'] = text_df.apply(lambda row: tokenizer.tokenize(row['alphabetic']), axis=1)
    stop = [word for word in stopwords.words('english') if word not in ["my","haven't"]]
    text_df['stop_words'] = text_df['special_word'].apply(lambda x: [item for item in x if item not in stop])
    text_df['stop_words'] = text_df['stop_words'].astype('str')
    text_df['short_word'] = text_df['stop_words'].str.findall('\w{2,}')
    text_df['text'] = text_df['short_word'].str.join(' ')
    text_df['text'] = text_df['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    text = multiclass_text_classification_count_vec.transform([text_df['text'][0]])
    text_vec = multiclass_text_classification_transformer.transform(text)
    prediction = multiclass_text_classification_model.predict(text_vec)
    prediction_list = prediction.tolist()
    response_dict = {'category': prediction_list}
    response_json = json.dumps(response_dict)
    response = app.response_class(response=response_json, status=200, mimetype='application/json')
    
    return response
'''



@app.route('/pneumonia', methods=['GET', 'POST'])
@login_required
def pneumonia():
    return render_template('pneumonia_detection.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['PNEUMONIA_UPLOAD_FOLDER'], filename)

'''
@app.route('/pneumonia_predict', methods=['GET', 'POST'])
def pneumonia_predict():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file_path = os.path.join(app.config['PNEUMONIA_UPLOAD_FOLDER'], filename)
        file.save(file_path)

        image = load_img(file_path, target_size=(224,224), color_mode="grayscale")
        input_arr = img_to_array(image)
        input_arr = np.array([input_arr])

        result = pneumonia_model.predict(input_arr)

        if result[0][0] == 1:
            prediction = 'PNEUMONIA'
        else:
            prediction = 'NORMAL'
        image_url = url_for('uploaded_file', filename='{}'.format(filename))
        response = {'prediction': prediction, 'image_url': image_url}
        return jsonify(response)
    return render_template('pneumonia_detection.html')
'''


@app.route('/summarizer', methods=['GET', 'POST'])
@login_required
def summarizer():
    return render_template('text_summarization.html')

'''
@app.route('/text-summarizer', methods=['POST'])
def text_summarizer():
    def summarize_text(text, models, tokenizers):
        summaries = []
        for model_name, model in models.items():
            tokenizer = tokenizers[model_name]
            length_penalty = 2.0
            num_beams = 3
            max_length = 1024
            min_length = max(round(0.33 * len(text.split())), 10)
            input_ids = tokenizer.encode(text, return_tensors='pt', max_length=max_length, truncation=True)
            summary_ids = model.generate(input_ids,
                                      num_beams=num_beams,
                                      length_penalty=length_penalty,
                                      max_length=max_length,
                                      min_length=min_length,
                                      early_stopping=True,
                                      pad_token_id=tokenizer.eos_token_id,
                                      attention_mask=input_ids.new_ones(input_ids.shape))
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)
        return summaries
    
    text = request.json['text']
   
    summaries = summarize_text(text, models, tokenizers)
    combined_summary = max(set(summaries), key=summaries.count)
    
    response = jsonify({'summarizeText': combined_summary})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response
'''



@app.route('/language', methods=['GET', 'POST'])
@login_required
def language():
    return render_template('language_detection.html')

'''
@app.route('/language-detection', methods=['POST'])
def language_detection():
    text = request.json['text']
    def word_token(sentence,flage=0):
        token=word_tokenize(sentence)
        if flage==1:
            return token
        return '  ||  '.join(token)

    def remove_stop_word(sentence):
        stop_words = stopwords.words('english')
        punct = list(punctuation)
        token=word_token(sentence,1)
        words=[]
        for word in token:
            if  word not in punct and not word.isdigit() :
                words.append(word.lower())
        return words  
    
    def get_code(N):
        for x,y in dict.items():
            if y==N:
                return x
                
    def prediction_function(sentence):
        sent=' '.join(remove_stop_word(sentence))
        sent=PipelineModel.transform([sent])
        sent=pd.DataFrame.sparse.from_spmatrix(sent)
        return get_code(np.argmax(model_language_detection.predict(sent)))

    predictionText = prediction_function(text)
   
    response = jsonify({'predictionText': predictionText})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response
'''


@app.route('/cataract', methods=['GET', 'POST'])
@login_required
def cataract():
    return render_template('cataract.html')

'''
@app.route('/cataract_predict', methods=['GET', 'POST'])
def cataract_predict():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file_path = os.path.join(app.config['CATARACT_UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        image = load_img(file_path, target_size=(512, 512))
        input_arr = img_to_array(image)
        input_arr = input_arr.reshape((1,) + input_arr.shape)
        preds = cataract_model.predict(input_arr)
        y_pred = np.argmax(preds, axis=1)
        
        if y_pred == 1:
            prediction = "Normal"
        else:
            prediction = "Cataract"

        response = {'signature': prediction}
        return jsonify(response)
        
    return render_template('cataract.html')
'''


@app.route('/fun_home')
def fun_home():
    message_of_guess = request.args.get('message_of_guess')
    message_of_rps = request.args.get('message_of_rps')
    return render_template('funs.html', message_of_guess=message_of_guess, message_of_rps=message_of_rps)


@app.route('/guess_number', methods=['POST'])
def guess_number():
    secret_number = random.randint(1, 100)
    tries = 0

    while tries < 10:
        guess = int(request.form['guess'])
        tries += 1

        if guess < secret_number:
            message_of_guess = f"Your guess of {guess} is too low. The secret number was {secret_number}."
        elif guess > secret_number:
            message_of_guess = f"Your guess of {guess} is too high. The secret number was {secret_number}."
        else:
            message_of_guess = f"Congratulations! You guessed the number in {tries} tries."
            break

    return redirect(url_for('fun_home', message_of_guess=message_of_guess))

@app.route('/rock_paper_scissors', methods=['POST'])
def rock_paper_scissors():
    user_choice = request.form['choice']
    if user_choice not in ["rock", "paper", "scissors"]:
        message_of_rps = "Invalid input, please try again!"
    else:
        computer_choice = random.choice(["rock", "paper", "scissors"])
        message_of_rps = f"You chose {user_choice}. Computer chooses {computer_choice}."
        if user_choice == computer_choice:
            message_of_rps += "\nIt's a tie!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            message_of_rps += "\nYou win!"
        else:
            message_of_rps += "\nComputer wins!"

    return redirect(url_for('fun_home', message_of_rps=message_of_rps))



@app.route('/palindrome_check', methods=['GET', 'POST'])
def palindrome_check():
    if request.method == 'POST':
        input_str = request.form['input_str']
        message_of_palindrome = is_palindrome(input_str)
        return render_template('funs.html', message_of_palindrome=message_of_palindrome, input_str=input_str)

    return render_template('funs.html')

def is_palindrome(string):
    return string == string[::-1]



@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
    if request.method == 'POST':
        n_terms = int(request.form['n_terms'])
        sequence = generate_fibonacci(n_terms)
        return render_template('funs.html', sequence=sequence)

    return render_template('funs.html')

def generate_fibonacci(n_terms):
    sequence = []
    n1, n2 = 0, 1
    count = 0

    if n_terms <= 0:
        sequence.append("Please enter a positive integer")
    elif n_terms == 1:
        sequence.append("Fibonacci sequence:")
        sequence.append(str(n1))
    else:
        sequence.append("Fibonacci sequence:")
        while count < n_terms:
            sequence.append(str(n1))
            nth = n1 + n2
            n1 = n2
            n2 = nth
            count += 1

    return sequence





@app.route('/utilities_home')
def utilities_home():
    password = request.args.get('password')
    tasks_param = request.args.get('tasks', '')
    tasks = urllib.parse.unquote(tasks_param).split(',') if tasks_param else []
    return render_template('utilities.html', password=password, tasks=tasks)

def generate_password(length):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    password_chars = f"{letters}{digits}{symbols}"
    password = ''.join(random.choice(password_chars) for _ in range(length))
    return password

@app.route('/generate_password', methods=['POST'])
def generate_password_route():
    password_length = int(request.form['length'])
    password = generate_password(password_length)
    return redirect(url_for('utilities_home', password=password))

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    tasks.append(task)
    tasks_param = urllib.parse.quote(','.join(tasks))
    return redirect(url_for('utilities_home', tasks=tasks_param))

@app.route('/remove_task', methods=['POST'])
def remove_task():
    task_num = int(request.form['task_num'])
    if task_num < 1 or task_num > len(tasks):
        return render_template('index.html', tasks=tasks, error="Invalid task number.")
    else:
        task = tasks.pop(task_num - 1)
        tasks_param = urllib.parse.quote(','.join(tasks))
        return redirect(url_for('utilities_home', tasks=tasks_param))



@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    url = request.form['url']
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(url)
    return render_template('utilities.html', short_url=short_url)



morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}



def to_morse_code(text):
    morse_code = ''
    for char in text:
        if char.upper() in morse_dict:
            morse_code += morse_dict[char.upper()] + ' '
        elif char == ' ':
            morse_code += '| '  
        else:
            morse_code += char
    return morse_code

def to_text(morse_code):
    text = ''
    morse_code = morse_code.split(' ')
    for code in morse_code:
        if code == '|':
            text += ' '  
        else:
            for key, value in morse_dict.items():
                if code == value:
                    text += key.lower()  
                    break
    return text



@app.route('/generate_morse_code', methods=['POST'])
def generate_morse_code():
    text = request.form['text']
    morse_code = to_morse_code(text)
    return render_template('utilities.html', morse_code=morse_code)


@app.route('/translate_morse_code', methods=['POST'])
def translate_morse_code():
    morse_code = request.form['morse_code']
    text = to_text(morse_code)
    return render_template('utilities.html', translated_text=text)




@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    data = request.form['data']

    qr = qrcode.QRCode(version=1, box_size=10, border=5)

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    encoded_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template('utilities.html', qr_code=f"data:image/png;base64,{encoded_img}")


@app.route('/text_to_audio_convert', methods=['POST'])
def text_to_audio_convert():
    text = request.form['text']

    tts = gTTS(text)
    tts.save('static/audio/audio.mp3')

    return render_template('utilities.html', audio_file='static/audio/audio.mp3')




@app.route('/number_conversion', methods=['GET', 'POST'])
def number_conversion():
    if request.method == 'POST':
        choice = request.form['choice']
        result = ""

        if choice == "1":
            decimal = int(request.form['decimal'])
            result = decimal_to_binary(decimal)
        elif choice == "2":
            decimal = int(request.form['decimal'])
            result = decimal_to_octal(decimal)
        elif choice == "3":
            decimal = int(request.form['decimal'])
            result = decimal_to_hexadecimal(decimal)
        elif choice == "4":
            binary = request.form['binary']
            result = binary_to_decimal(binary)
        elif choice == "5":
            binary = request.form['binary']
            result = binary_to_octal(binary)
        elif choice == "6":
            binary = request.form['binary']
            result = binary_to_hexadecimal(binary)
        elif choice == "7":
            octal = request.form['octal']
            result = octal_to_decimal(octal)
        elif choice == "8":
            octal = request.form['octal']
            result = octal_to_binary(octal)
        elif choice == "9":
            octal = request.form['octal']
            result = octal_to_hexadecimal(octal)
        elif choice == "10":
            hexadecimal = request.form['hexadecimal']
            result = hexadecimal_to_decimal(hexadecimal)
        elif choice == "11":
            hexadecimal = request.form['hexadecimal']
            result = hexadecimal_to_binary(hexadecimal)
        elif choice == "12":
            hexadecimal = request.form['hexadecimal']
            result = hexadecimal_to_octal(hexadecimal)
        
        return render_template('utilities.html', result=result)

    return render_template('utilities.html')

def decimal_to_binary(n):
    return bin(n)[2:]

def decimal_to_octal(n):
    return oct(n)[2:]

def decimal_to_hexadecimal(n):
    return hex(n)[2:]

def binary_to_decimal(n):
    return int(n, 2)

def binary_to_octal(n):
    decimal = binary_to_decimal(n)
    return decimal_to_octal(decimal)

def binary_to_hexadecimal(n):
    decimal = binary_to_decimal(n)
    return decimal_to_hexadecimal(decimal)

def octal_to_decimal(n):
    return int(n, 8)

def octal_to_binary(n):
    decimal = octal_to_decimal(n)
    return decimal_to_binary(decimal)

def octal_to_hexadecimal(n):
    decimal = octal_to_decimal(n)
    return decimal_to_hexadecimal(decimal)

def hexadecimal_to_decimal(n):
    return int(n, 16)

def hexadecimal_to_binary(n):
    decimal = hexadecimal_to_decimal(n)
    return decimal_to_binary(decimal)

def hexadecimal_to_octal(n):
    decimal = hexadecimal_to_decimal(n)
    return decimal_to_octal(decimal)


if __name__ == '__main__':
    app.run(debug=True)