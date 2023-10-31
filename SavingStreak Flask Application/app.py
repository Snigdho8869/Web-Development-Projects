from flask import Flask, send_file, jsonify, flash, session, render_template, redirect, url_for,request, make_response, get_flashed_messages, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import InputRequired, Length, EqualTo, Email, DataRequired, NumberRange, ValidationError
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
from datetime import date
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import smtplib
import os 
import json
from flask_mysqldb import MySQL
from tkcalendar import DateEntry
from decimal import Decimal

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'SavingStreak'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'


UPLOAD_FOLDER = 'static/profile_pic'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['PROFILE_PICTURE_UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, username, password, first_name, last_name, email, favorite_number, picture, cash, bank, savings, credit_cards, lifetime_balance, lifetime_spending):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.favorite_number = favorite_number
        self.picture = picture
        self.cash = cash
        self.bank = bank
        self.savings = savings
        self.credit_cards = credit_cards
        self.lifetime_balance = lifetime_balance
        self.lifetime_spending = lifetime_spending


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    favorite_number = IntegerField('Favorite Number', validators=[DataRequired()])
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
        user = User(id=user_data[0], username=user_data[3], password=user_data[4], first_name=user_data[1], last_name=user_data[2], email=user_data[10], favorite_number=user_data[5], picture=user_data[11], cash=user_data[6], bank=user_data[7], savings=user_data[8], credit_cards=user_data[9], lifetime_balance=user_data[12], lifetime_spending=user_data[13])
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
        password = form.password.data
        favorite_number = form.favorite_number.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, username, email, password, favorite_number) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, username, email, password, favorite_number))
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
        if user_data and user_data[4] == password:
            user = User(id=user_data[0], username=user_data[3], password=user_data[4], first_name=user_data[1], last_name=user_data[2], email=user_data[10], favorite_number=user_data[5],picture=user_data[11], cash=user_data[6],  bank=user_data[7], savings=user_data[8], credit_cards=user_data[9], lifetime_balance=user_data[12], lifetime_spending=user_data[13])
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
@login_required
def home():
    username = current_user.username
    conn = mysql.connection
    cur = conn.cursor()
    
    today = date.today()
    cur.execute("SELECT SUM(amount) FROM expenses WHERE username = %s AND date = %s", (username, today))
    today_expense = cur.fetchone()[0]
    
    last_7_days = today - timedelta(days=7)
    cur.execute("SELECT SUM(amount) FROM expenses WHERE username = %s AND date >= %s AND date <= %s", (username, last_7_days, today))
    last_7_days_expense = cur.fetchone()[0]
    
    last_30_days = today - timedelta(days=30)
    cur.execute("SELECT SUM(amount) FROM expenses WHERE username = %s AND date >= %s AND date <= %s", (username, last_30_days, today))
    last_30_days_expense = cur.fetchone()[0]
    
    cur.execute("SELECT cash, bank,savings, credit_cards FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    return render_template('home.html', user=current_user, today_expense=today_expense, last_7_days_expense=last_7_days_expense, last_30_days_expense=last_30_days_expense)


@app.route('/update_account_balance', methods=['POST'])
@login_required
def update_account_balance():
    data = request.get_json()
    account_type = data['accountType']
    balance = float(data['balance'])
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET {account_type} = {account_type} + %s, lifetime_balance = lifetime_balance + %s WHERE username = %s", (balance, balance, current_user.username))
    conn.commit()
    cur.close()
    flash(f'Balance Added Successfully for {account_type.capitalize()}', 'success')

    return jsonify({'success': True})




@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    account_type = request.form['account_type']
    username = request.form['username']

    conn = mysql.connection
    cur = conn.cursor()
    
    cur.execute(f"SELECT {account_type} FROM users WHERE username = %s", (username,))
    account_balance = cur.fetchone()[0]
    
    if account_balance < amount:
        flash('Insufficient balance!', 'error')
    
    else:
        cur.execute(f"UPDATE users SET {account_type} = {account_type} - %s WHERE username = %s", (amount, username))
        cur.execute("INSERT INTO expenses (date, category, amount, username) VALUES (%s, %s, %s, %s)", (date, category, amount, username))
        cur.execute("UPDATE users SET lifetime_spending = lifetime_spending + %s WHERE username = %s", (amount, username))
        conn.commit()
        flash('Expense added successfully!', 'success')
        
    cur.close()
    return redirect(url_for('home'))




@app.route('/expenses_by_category')
@login_required
def expenses_by_category():
    conn = mysql.connection
    cur = conn.cursor()
    today = datetime.today()
    start_date = today - timedelta(days=30)
    cur.execute('SELECT category, SUM(amount) FROM expenses WHERE username = %s AND date BETWEEN %s AND %s GROUP BY category', (current_user.username, start_date, today))
    results = cur.fetchall()
    labels = [result[0] for result in results]
    values = [result[1] for result in results]
    data = {'labels': labels, 'values': values}
    return jsonify(data)



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)




@app.route('/upload_picture', methods=['POST'])
@login_required
def upload_picture():
    file = request.files['picture']
    if file and allowed_file(file.filename):
        username = current_user.username
        
        directory = os.path.join(app.config['PROFILE_PICTURE_UPLOAD_FOLDER'], username)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['PROFILE_PICTURE_UPLOAD_FOLDER'], username, filename))

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET picture=%s WHERE id=%s", [os.path.join(username, filename), current_user.id])
        mysql.connection.commit()
        cur.close()
        
        flash('Picture uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload a picture with one of the following extensions: jpg, jpeg, png, gif', 'error')
    
    return redirect(url_for('profile'))



@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE users SET email = %s, favorite_number= %s WHERE id = %s', (
        request.form['email'],
        request.form['favorite_number'],
        current_user.id
    ))
    mysql.connection.commit()
    cursor.close()
    flash('Profile Edited successfully', 'success')
    return redirect(url_for('profile'))


@app.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics():
    username = current_user.username
    conn = mysql.connection
    cur = conn.cursor()

    today = date.today()
    last_30_days = today - timedelta(days=30)
    cur.execute("SELECT date, SUM(amount) FROM expenses WHERE username = %s AND date >= %s AND date <= %s GROUP BY date", (username, last_30_days, today))
    daily_expenses = cur.fetchall()

    cur.execute("SELECT SUM(amount) FROM expenses WHERE username = %s AND date = %s", (username, today))
    today_expense = cur.fetchone()[0]

    last_7_days = today - timedelta(days=7)
    cur.execute("SELECT SUM(amount) FROM expenses WHERE username = %s AND date >= %s AND date <= %s", (username, last_7_days, today))
    last_7_days_expense = cur.fetchone()[0]

    last_30_days_expense = sum([expense[1] for expense in daily_expenses])

    cur.execute("SELECT cash, bank FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    return render_template('statistics.html', user=current_user, daily_expenses=daily_expenses, today_expense=today_expense, last_7_days_expense=last_7_days_expense, last_30_days_expense=last_30_days_expense)




@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        goal_name = request.form['goal_name'].title()
        need_amount = request.form['need_amount']
        username =  current_user.username
        cursor = mysql.connection.cursor()
        
        cursor.execute('SELECT * FROM goals WHERE username = %s AND goal_name = %s AND goal_status = %s', [username, goal_name, 'Incomplete'])
        existing_goal = cursor.fetchone()
        if existing_goal:
            flash('Can\'t add goal, it already exists', 'error')
        else:
            cursor.execute('INSERT INTO goals (username, goal_name, need_amount, savings_amount) VALUES (%s, %s, %s, %s)', (username, goal_name, need_amount, 0))
            mysql.connection.commit()
            flash('Goal Added Successfully', 'success')
        cursor.close()
        return redirect(url_for('goals'))
    else:
        cursor = mysql.connection.cursor()
        username = current_user.username
        cursor.execute('SELECT goal_name, need_amount, savings_amount, goal_status FROM goals WHERE username = %s', [username])
        goals_data = cursor.fetchall()
        cursor.close()
        return render_template('goals.html', goals=goals_data)




@app.route('/add_savings/<goal_name>', methods=['POST'])
@login_required
def add_savings(goal_name):
    savings_amount = Decimal(request.form['savings_amount'])
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM goals WHERE username = %s AND goal_name = %s", (current_user.username, goal_name))
    goal = cur.fetchone()
    columns = [column[0] for column in cur.description]
    goal = dict(zip(columns, goal))
    
    new_savings_amount = goal['savings_amount'] + savings_amount
    if new_savings_amount >= goal['need_amount']:
        new_goal_status = 'Complete'
    else:
        new_goal_status = 'In progress'
    
    cur.execute("UPDATE goals SET savings_amount = %s, goal_status = %s WHERE goal_name = %s", (new_savings_amount, new_goal_status, goal_name))
    flash('Amount Added Successfully', 'success')
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('goals'))



@app.route('/remove_goal/<goal_name>', methods=['POST'])
@login_required
def remove_goal(goal_name):
    cursor = mysql.connection.cursor()
    username = current_user.username
    cursor.execute('DELETE FROM goals WHERE username = %s AND goal_name = %s', (username, goal_name))
    mysql.connection.commit()
    cursor.close()
    flash('Goal Removed successfully', 'error')
    return redirect(url_for('goals'))




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
