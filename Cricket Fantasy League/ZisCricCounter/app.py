from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, validators
from wtforms.validators import InputRequired, Length, EqualTo, Email, DataRequired, NumberRange, ValidationError
from email_validator import validate_email, EmailNotValidError
from werkzeug.utils import secure_filename
from operator import itemgetter
import os
import time

app = Flask(__name__)

app.config['STATIC_FOLDER'] = 'static'

app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'ziscriccounter'

mysql = MySQL(app)

UPLOAD_FOLDER = 'static/profile_pic'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, name, user_name, password, email, favorite_numbers, profile_picture_name, player_1_name, player_1_role, player_1_total_points, player_2_name, player_2_role, player_2_total_points, player_3_name, player_3_role, player_3_total_points,player_4_name, player_4_role, player_4_total_points,player_5_name, player_5_role, player_5_total_points,player_6_name, player_6_role, player_6_total_points,player_7_name, player_7_role, player_7_total_points,player_8_name, player_8_role, player_8_total_points,player_9_name, player_9_role, player_9_total_points,player_10_name, player_10_role, player_10_total_points,player_11_name, player_11_role, player_11_total_points,player_12_name, player_12_role, player_12_total_points,player_13_name, player_13_role, player_13_total_points,all_players_total_points, total_batsman_points, total_bowler_points, total_all_rounder_points, team_1_name, team_1_points, team_2_name, team_2_points, all_teams_total_points, combined_total_points):
        self.id = id
        self.name = name
        self.user_name = user_name
        self.password = password
        self.email = email
        self.favorite_numbers = favorite_numbers
        self.profile_picture_name = profile_picture_name
        self.player_1_name = player_1_name
        self.player_1_role = player_1_role
        self.player_1_total_points = player_1_total_points
        self.player_2_name = player_2_name
        self.player_2_role = player_2_role
        self.player_2_total_points = player_2_total_points
        self.player_3_name = player_3_name
        self.player_3_role = player_3_role
        self.player_3_total_points = player_3_total_points
        self.player_4_name = player_4_name
        self.player_4_role = player_4_role
        self.player_4_total_points = player_4_total_points
        self.player_5_name = player_5_name
        self.player_5_role = player_5_role
        self.player_5_total_points = player_5_total_points
        self.player_6_name = player_6_name
        self.player_6_role = player_6_role
        self.player_6_total_points = player_6_total_points
        self.player_7_name = player_7_name
        self.player_7_role = player_7_role
        self.player_7_total_points = player_7_total_points
        self.player_8_name = player_8_name
        self.player_8_role = player_8_role
        self.player_8_total_points = player_8_total_points
        self.player_9_name = player_9_name
        self.player_9_role = player_9_role
        self.player_9_total_points = player_9_total_points
        self.player_10_name = player_10_name
        self.player_10_role = player_10_role
        self.player_10_total_points = player_10_total_points
        self.player_11_name = player_11_name
        self.player_11_role = player_11_role
        self.player_11_total_points = player_11_total_points
        self.player_12_name = player_12_name
        self.player_12_role = player_12_role
        self.player_12_total_points = player_12_total_points
        self.player_13_name = player_13_name
        self.player_13_role = player_13_role
        self.player_13_total_points = player_13_total_points
        self.all_players_total_points = all_players_total_points
        self.total_batsman_points = total_batsman_points
        self.total_bowler_points = total_bowler_points
        self.total_all_rounder_points = total_all_rounder_points
        self.team_1_name = team_1_name
        self.team_1_points = team_1_points
        self.team_2_name = team_2_name
        self.team_2_points = team_2_points
        self.all_teams_total_points = all_teams_total_points
        self.combined_total_points = combined_total_points


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    user_name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    favorite_number = IntegerField('Favorite Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    user_name = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    favorite_numbers = IntegerField('Favorite Number', validators=[InputRequired()])
    new_password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Reset Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        user_name = form.user_name.data
        email = form.email.data
        favorite_number = form.favorite_number.data
        password = form.password.data

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (name, user_name, email, favorite_numbers, password) VALUES (%s, %s, %s, %s, %s)",
                        (name, user_name, email, favorite_number, password))
            mysql.connection.commit()
            cur.close()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error inserting user: {str(e)}")
            flash('An error occurred while registering. Please try again.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route('/check_username/<user_name>')
def check_username(user_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE user_name = %s", [user_name])
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})



# Route for password reset
@app.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        favorite_numbers = int(form.favorite_numbers.data)
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT favorite_numbers FROM users WHERE user_name = %s", (user_name,))
        result = cur.fetchone()

        if result is None:
            flash('Username is incorrect! Please try again.', 'danger')
            return redirect(url_for('password_reset'))

        user_favorite_number = int(result[0])

        if favorite_numbers != user_favorite_number:
            flash('Favorite number is incorrect! Please try again.', 'danger')
            return redirect(url_for('password_reset'))

        cur.execute("UPDATE users SET password = %s WHERE user_name = %s AND favorite_numbers = %s", (new_password, user_name, favorite_numbers))
        mysql.connection.commit()
        cur.close()

        flash('Password reset successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('password_reset.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        user = User(id=user_data[0], user_name=user_data[2], password=user_data[3], name=user_data[1], email=user_data[4], favorite_numbers=user_data[5], profile_picture_name=user_data[6], player_1_name=user_data[7], player_1_role=user_data[8], player_1_total_points=user_data[9], player_2_name=user_data[10], player_2_role=user_data[11], player_2_total_points=user_data[12], player_3_name=user_data[13], player_3_role=user_data[14], player_3_total_points=user_data[15], player_4_name=user_data[16], player_4_role=user_data[17], player_4_total_points=user_data[18], player_5_name=user_data[19], player_5_role=user_data[20], player_5_total_points=user_data[21], player_6_name=user_data[22], player_6_role=user_data[23], player_6_total_points=user_data[24], player_7_name=user_data[25], player_7_role=user_data[26], player_7_total_points=user_data[27], player_8_name=user_data[28], player_8_role=user_data[29], player_8_total_points=user_data[30], player_9_name=user_data[31], player_9_role=user_data[32], player_9_total_points=user_data[33], player_10_name=user_data[34], player_10_role=user_data[35], player_10_total_points=user_data[36], player_11_name=user_data[37], player_11_role=user_data[38], player_11_total_points=user_data[39], player_12_name=user_data[40], player_12_role=user_data[41], player_12_total_points=user_data[42], player_13_name=user_data[43], player_13_role=user_data[44], player_13_total_points=user_data[45], all_players_total_points=user_data[46], total_batsman_points=user_data[47], total_bowler_points=user_data[48], total_all_rounder_points=user_data[49], team_1_name=user_data[50], team_1_points=user_data[51], team_2_name=user_data[52], team_2_points=user_data[53], all_teams_total_points=user_data[54], combined_total_points=user_data[55])
        return user
    return None


# Route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_name=%s", [user_name])
        user_data = cur.fetchone()
        cur.close()
        if user_data and user_data[3] == password:
            user = User(id=user_data[0], user_name=user_data[2], password=user_data[3], name=user_data[1], email=user_data[4], favorite_numbers=user_data[5], profile_picture_name=user_data[6], player_1_name=user_data[7], player_1_role=user_data[8], player_1_total_points=user_data[9], player_2_name=user_data[10], player_2_role=user_data[11], player_2_total_points=user_data[12], player_3_name=user_data[13], player_3_role=user_data[14], player_3_total_points=user_data[15], player_4_name=user_data[16], player_4_role=user_data[17], player_4_total_points=user_data[18], player_5_name=user_data[19], player_5_role=user_data[20], player_5_total_points=user_data[21], player_6_name=user_data[22], player_6_role=user_data[23], player_6_total_points=user_data[24], player_7_name=user_data[25], player_7_role=user_data[26], player_7_total_points=user_data[27], player_8_name=user_data[28], player_8_role=user_data[29], player_8_total_points=user_data[30], player_9_name=user_data[31], player_9_role=user_data[32], player_9_total_points=user_data[33], player_10_name=user_data[34], player_10_role=user_data[35], player_10_total_points=user_data[36], player_11_name=user_data[37], player_11_role=user_data[38], player_11_total_points=user_data[39], player_12_name=user_data[40], player_12_role=user_data[41], player_12_total_points=user_data[42], player_13_name=user_data[43], player_13_role=user_data[44], player_13_total_points=user_data[45], all_players_total_points=user_data[46], total_batsman_points=user_data[47], total_bowler_points=user_data[48], total_all_rounder_points=user_data[49], team_1_name=user_data[50], team_1_points=user_data[51], team_2_name=user_data[52], team_2_points=user_data[53], all_teams_total_points=user_data[54], combined_total_points=user_data[55])
            login_user(user)
            flash('Login success', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password.', 'error')
            
    return render_template('login.html', form=form)

# Route for logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Route for home
@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        flash('You need to log in to access this page', 'danger')
        return redirect(url_for('login'))

# Route for home
@app.route('/home')
def home():
    return render_template('index.html', user=current_user)



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/upload_picture', methods=['POST'])
@login_required
def upload_picture():
    file = request.files['picture']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET profile_picture_name=%s WHERE user_id=%s", [filename, current_user.id])
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
    cursor.execute('UPDATE users SET email = %s, favorite_numbers = %s WHERE user_id = %s', (
        request.form['email'],
        request.form['favorite_number'],
        current_user.id
    ))
    mysql.connection.commit()
    cursor.close()
    flash('Profile Edited successfully', 'success')
    return redirect(url_for('profile'))



# Route for suggesting player names
@app.route('/suggest_player', methods=['GET'])
@login_required
def suggest_player():
    query = request.args.get('query')

    cur = mysql.connection.cursor()
    cur.execute("SELECT player_name FROM batsmans WHERE player_name LIKE %s", ("%" + query + "%",))
    batsman_names = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT player_name FROM bowlers WHERE player_name LIKE %s", ("%" + query + "%",))
    bowler_names = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT player_name FROM allrounders WHERE player_name LIKE %s", ("%" + query + "%",))
    allrounder_names = [row[0] for row in cur.fetchall()]
    suggested_names = list(set(batsman_names + bowler_names + allrounder_names))
    
    return jsonify(suggested_names)

# Route for getting the player's role
@app.route('/get_player_role', methods=['GET'])
@login_required
def get_player_role():
    player_name = request.args.get('player_name')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT role FROM batsmans WHERE player_name = %s", (player_name,))
    batsman_role = cur.fetchone()

    cur.execute("SELECT role FROM bowlers WHERE player_name = %s", (player_name,))
    bowler_role = cur.fetchone()

    cur.execute("SELECT role FROM allrounders WHERE player_name = %s", (player_name,))
    allrounder_role = cur.fetchone()

    cur.close()

    if batsman_role:
        return jsonify(batsman_role[0])
    elif bowler_role:
        return jsonify(bowler_role[0])
    elif allrounder_role:
        return jsonify(allrounder_role[0])
    else:
        return jsonify('') 

# Insert inning data route
@app.route('/insert_inning_data', methods=['POST'])
@login_required
def insert_inning_data():
    player_name = request.form.get('player_name')
    inning_no = request.form.get('inning_no')
    runs = request.form.get('runs')
    strike_rate = request.form.get('strike_rate')
    wickets = request.form.get('wickets')
    economy_rate = request.form.get('economy_rate')
    points = request.form.get('points')
    role = request.form.get('role')
    playerId = request.form.get('playerId')

    print("Received Data:")
    print("playerId:", playerId)
    print("Player Name:", player_name)
    print("Inning No:", inning_no)
    print("Runs:", runs)
    print("Strike Rate:", strike_rate)
    print("Wickets:", wickets)
    print("Economy Rate:", economy_rate)
    print("Points:", points)
    print("Role:", role)


    try:
        cursor = mysql.connection.cursor()

        if role == 'Batsman':
            query = "INSERT INTO batsmans (player_name, role, inning_{0}_runs, inning_{0}_strike_rate, inning_{0}_points) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE inning_{0}_runs = VALUES(inning_{0}_runs), inning_{0}_strike_rate = VALUES(inning_{0}_strike_rate), inning_{0}_points = VALUES(inning_{0}_points)".format(inning_no)
            cursor.execute(query, (player_name, role, runs, strike_rate, points))

        elif role == 'Bowler':
            query = "INSERT INTO bowlers (player_name, role, inning_{0}_wickets, inning_{0}_economy_rate, inning_{0}_points) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE inning_{0}_wickets = VALUES(inning_{0}_wickets), inning_{0}_economy_rate = VALUES(inning_{0}_economy_rate), inning_{0}_points = VALUES(inning_{0}_points)".format(inning_no)
            cursor.execute(query, (player_name, role, wickets, economy_rate, points))

        elif role == 'All-Rounder':
            query = "INSERT INTO allrounders (player_name, role, inning_{0}_runs, inning_{0}_strike_rate, inning_{0}_wickets, inning_{0}_economy_rate, inning_{0}_points) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE inning_{0}_runs = VALUES(inning_{0}_runs), inning_{0}_strike_rate = VALUES(inning_{0}_strike_rate), inning_{0}_wickets = VALUES(inning_{0}_wickets), inning_{0}_economy_rate = VALUES(inning_{0}_economy_rate), inning_{0}_points = VALUES(inning_{0}_points)".format(inning_no)
            cursor.execute(query, (player_name, role, runs, strike_rate, wickets, economy_rate, points))

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Inning data inserted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})




@app.route('/insert_player_total_points', methods=['POST'])
@login_required
def insert_player_total_points():
    player_name = request.form.get('player_name')
    role = request.form.get('role')
    total_points = request.form.get('total_points')
    print("Received Data:")
    print("Player Name: ", player_name)
    print("Player Role: ", role)
    print("Player Total Points: ", total_points)

    try:
        cursor = mysql.connection.cursor()

        table_name = None
        if role == 'Batsman':
            table_name = 'batsmans'
        elif role == 'Bowler':
            table_name = 'bowlers'
        elif role == 'All-Rounder':
            table_name = 'allrounders'

        if table_name:
            query = f"UPDATE {table_name} SET player_total_points = %s WHERE player_name = %s"
            cursor.execute(query, (total_points, player_name))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'Player total points inserted successfully'})
        else:
            return jsonify({'error': 'Invalid player role'})

    except Exception as e:
        return jsonify({'error': str(e)})




@app.route('/insert_player_data', methods=['POST'])
@login_required
def insert_player_data():
    player_name = request.form.get('player_name')
    player_role = request.form.get('player_role')
    player_total_points = request.form.get('player_total_points')

    print("Received Data:")
    print("Player Name: ", player_name)
    print("Player Role: ", player_role)
    print("Player Total Points: ", player_total_points)

    try:
        cursor = mysql.connection.cursor()

        for i in range(1, 14):
            column_name = f"player_{i}_name"
            role_column_name = f"player_{i}_role"
            points_column_name = f"player_{i}_total_points"

            check_query = f"SELECT {column_name} FROM users WHERE user_id = %s"
            cursor.execute(check_query, (current_user.id,))
            result = cursor.fetchone()

            if not result[0]:
                update_query = f"UPDATE users SET {column_name} = %s, {role_column_name} = %s, {points_column_name} = %s WHERE user_id = %s"
                cursor.execute(update_query, (player_name, player_role, player_total_points, current_user.id))
                mysql.connection.commit()
                cursor.close()
                return jsonify({'success': True, 'message': f'Player {i} data inserted successfully'})

        return jsonify({'success': False, 'error': 'No empty player slot available'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})




@app.route('/calculate_all_players_total_points', methods=['POST'])
@login_required
def calculate_all_players_total_points():
    try:
        user_id = current_user.id
        print("Data: ")
        print("User Id: ", user_id)

        if user_id is not None:
            cursor = mysql.connection.cursor()

            total_points = 0
            total_batsman_points = 0
            total_bowler_points = 0
            total_all_rounder_points = 0

            for player_id in range(1, 14):
                points_column_name = f"player_{player_id}_total_points"
                role_column_name = f"player_{player_id}_role"
                
                query = f"SELECT {points_column_name}, {role_column_name} FROM users WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                
                if result:
                    points = result[0]
                    role = result[1]

                    total_points += points  

                    if role == 'Batsman':
                        total_batsman_points += points
                    elif role == 'Bowler':
                        total_bowler_points += points
                    elif role == 'All-Rounder':
                        total_all_rounder_points += points

            update_query = "UPDATE users SET all_players_total_points = %s, total_batsman_points = %s, total_bowler_points = %s, total_all_rounder_points = %s WHERE user_id = %s"
            cursor.execute(update_query, (total_points, total_batsman_points, total_bowler_points, total_all_rounder_points, user_id))
            mysql.connection.commit()
            cursor.close()

            print("All Players Total Points: ", total_points)
            print("Batsman Total Points: ", total_batsman_points)
            print("Bowler Total Points: ", total_bowler_points)
            print("All-Rounder Total Points: ", total_all_rounder_points)

            return jsonify({'success': True, 'message': 'All players total points calculated and updated', 'total_points': total_points, 'total_batsman_points': total_batsman_points, 'total_bowler_points': total_bowler_points, 'total_all_rounder_points': total_all_rounder_points})
        else:
            return jsonify({'success': False, 'error': 'User not authenticated'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route('/suggest_team', methods=['POST'])
@login_required
def suggest_team():
    team_name = request.form.get('team_name')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT team_name FROM teams WHERE team_name LIKE %s", (f'%{team_name}%',))
    suggestions = [row[0] for row in cursor.fetchall()]
    print(suggestions)

    return jsonify(suggestions)


@app.route('/get_team_data', methods=['POST'])
@login_required
def get_team_data():
    team_name = request.form.get('team_name')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT highest_team_position, team_points FROM teams WHERE team_name = %s", (team_name,))
    team_data = cursor.fetchone()

    if team_data:
        position, points = team_data
        return jsonify({'position': position, 'points': points})
    else:
        return jsonify({'position': '', 'points': 0.0})


@app.route('/insert_team_data', methods=['POST'])
@login_required
def insert_team_data():
    user_id = current_user.id
    team_number = request.form.get('teamNumber')
    team_name = request.form.get('teamName')
    team_position = request.form.get('teamPosition')
    team_points = request.form.get('teamPoints')
    print("User ID: ", user_id)
    print("Team Number: ", team_number)
    print("Team Name: ", team_name)
    print("Team Position: ", team_position)
    print("Team Points: ", team_points)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT team_id FROM teams WHERE team_name = %s", (team_name,))
    team_id = cursor.fetchone()

    if not team_id:
        cursor.execute("INSERT INTO teams (team_name, highest_team_position, team_points) VALUES (%s, %s, %s)",
                       (team_name, team_position, team_points))
        mysql.connection.commit()

    if team_number == '1':
        cursor.execute("UPDATE users SET team_1_name = %s, team_1_points = %s WHERE user_id = %s",
                       (team_name, team_points, user_id))
    else:
        cursor.execute("UPDATE users SET team_2_name = %s, team_2_points = %s WHERE user_id = %s",
                       (team_name, team_points, user_id))
    mysql.connection.commit()

    return jsonify({'message': 'Data inserted successfully'})




@app.route('/update_all_teams_total_points', methods=['POST'])
@login_required
def update_all_teams_total_points():
    user_id = current_user.id
    all_teams_total_points = request.form.get('all_teams_total_points')

    print("User ID: ", user_id)
    print("All Team Total Points: ", all_teams_total_points)

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET all_teams_total_points = %s WHERE user_id = %s",
                   (all_teams_total_points, user_id))
    mysql.connection.commit()

    return jsonify({'message': 'Total points updated successfully'})


@app.route('/calculate_combined_total_points', methods=['POST'])
@login_required
def calculate_total_points():
    try:
        user_id = current_user.id
        print("User Id: ", user_id)

        if user_id is not None:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT all_players_total_points, all_teams_total_points FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()

            if result:
                all_players_total_points = result[0] or 0
                all_teams_total_points = result[1] or 0

                total_points = all_players_total_points + all_teams_total_points

                cursor.execute("UPDATE users SET combined_total_points = %s WHERE user_id = %s", (total_points, user_id))
                mysql.connection.commit()

                return jsonify({'total_points': total_points, 'all_players_total_points': all_players_total_points, 'all_teams_total_points': all_teams_total_points})

        return jsonify({'error': 'User not authenticated'})

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/get_leaderboard', methods=['GET'])
@login_required
def get_leaderboard():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_name, combined_total_points FROM users ORDER BY combined_total_points DESC")
        leaderboard_data = cursor.fetchall()
        cursor.close()

        leaderboard = [{'user_name': row[0], 'combined_total_points': row[1]} for row in leaderboard_data]
        return jsonify(leaderboard)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_top_players', methods=['GET'])
@login_required
def get_top_players():
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT player_name, role, player_total_points 
            FROM batsmans 
            UNION ALL
            SELECT player_name, role, player_total_points 
            FROM bowlers 
            UNION ALL
            SELECT player_name, role, player_total_points 
            FROM allrounders 
            ORDER BY player_total_points DESC 
            LIMIT 10
        """)
        combined_data = cursor.fetchall()

        cursor.close()

        top_players = []

        for row in combined_data:
            top_players.append({'player_name': row[0], 'role': row[1], 'player_total_points': row[2]})

        return jsonify(top_players)

    except Exception as e:
        return jsonify({'error': str(e)})



# route to get top 5 players for the user
@app.route('/get_top_5_players_of_user', methods=['GET'])
@login_required
def get_top_5_players_of_user():
    try:
        user_id = current_user.id
        cursor = mysql.connection.cursor()

        top_players = []
        for i in range(1, 14):
            cursor.execute(f"SELECT player_{i}_name, player_{i}_role, player_{i}_total_points FROM users WHERE user_id = %s", (user_id,))
            player_data = cursor.fetchone()

            if player_data:
                top_players.append({
                    'player_name': player_data[0],
                    'role': player_data[1],
                    'player_total_points': player_data[2]
                })

        top_players = sorted(top_players, key=lambda x: x['player_total_points'], reverse=True)[:5]
        cursor.close()

        return jsonify(top_players)

    except Exception as e:
        return jsonify({'error': str(e)})



# route to get all players for the user
@app.route('/get_all_players_of_user', methods=['GET'])
@login_required
def get_all_players_of_user():
    try:
        user_id = current_user.id
        cursor = mysql.connection.cursor()

        all_players = []
        for i in range(1, 14):
            cursor.execute(f"SELECT player_{i}_name, player_{i}_role, player_{i}_total_points FROM users WHERE user_id = %s", (user_id,))
            player_data = cursor.fetchone()

            if player_data:
                all_players.append({
                    'player_name': player_data[0],
                    'role': player_data[1],
                    'player_total_points': player_data[2]
                })

        all_players = sorted(all_players, key=itemgetter('player_total_points'), reverse=True)

        cursor.close()

        return jsonify(all_players)

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_all_batsman_players_of_user', methods=['GET'])
@login_required
def get_all_batsman_players_of_user():
    try:
        user_id = current_user.id
        cursor = mysql.connection.cursor()

        all_batsman_players = []
        for i in range(1, 14):
            cursor.execute(f"SELECT player_{i}_name, player_{i}_role, player_{i}_total_points FROM users WHERE user_id = %s", (user_id,))
            player_data = cursor.fetchone()

            if player_data and player_data[1] == 'Batsman':
                all_batsman_players.append({
                    'player_name': player_data[0],
                    'role': player_data[1],
                    'player_total_points': player_data[2]
                })

        all_batsman_players = sorted(all_batsman_players, key=itemgetter('player_total_points'), reverse=True)

        cursor.close()

        return jsonify(all_batsman_players)

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/get_all_bowler_players_of_user', methods=['GET'])
@login_required
def get_all_bowler_players_of_user():
    try:
        user_id = current_user.id
        cursor = mysql.connection.cursor()

        all_bowler_players = []
        for i in range(1, 14):
            cursor.execute(f"SELECT player_{i}_name, player_{i}_role, player_{i}_total_points FROM users WHERE user_id = %s", (user_id,))
            player_data = cursor.fetchone()

            if player_data and player_data[1] == 'Bowler':
                all_bowler_players.append({
                    'player_name': player_data[0],
                    'role': player_data[1],
                    'player_total_points': player_data[2]
                })

        all_bowler_players = sorted(all_bowler_players, key=itemgetter('player_total_points'), reverse=True)

        cursor.close()

        return jsonify(all_bowler_players)

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/get_all_allrounder_players_of_user', methods=['GET'])
@login_required
def get_all_allrounder_players_of_user():
    try:
        user_id = current_user.id
        cursor = mysql.connection.cursor()

        all_allrounder_players = []
        for i in range(1, 14):
            cursor.execute(f"SELECT player_{i}_name, player_{i}_role, player_{i}_total_points FROM users WHERE user_id = %s", (user_id,))
            player_data = cursor.fetchone()

            if player_data and player_data[1] == 'All-Rounder':
                all_allrounder_players.append({
                    'player_name': player_data[0],
                    'role': player_data[1],
                    'player_total_points': player_data[2]
                })

        all_allrounder_players = sorted(all_allrounder_players, key=itemgetter('player_total_points'), reverse=True)

        cursor.close()

        return jsonify(all_allrounder_players)

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/fetch_player_innings_info', methods=['GET'])
def fetch_player_innings_info():
    player_name = request.args.get('player_name')
    role = request.args.get('role')
    
    print(player_name)
    print(role)

    innings_info = []

    cursor = mysql.connection.cursor()

    for i in range(1, 12):
        inning_info = {}

        if role == 'Batsman':
            inning_query = f"SELECT inning_{i}_runs, inning_{i}_strike_rate, inning_{i}_points FROM batsmans WHERE player_name = %s"
        elif role == 'Bowler':
            inning_query = f"SELECT inning_{i}_wickets, inning_{i}_economy_rate, inning_{i}_points FROM bowlers WHERE player_name = %s"
        elif role == 'All-Rounder':
            inning_query = f"SELECT inning_{i}_runs, inning_{i}_strike_rate, inning_{i}_wickets, inning_{i}_economy_rate, inning_{i}_points FROM allrounders WHERE player_name = %s"
        else:
            return jsonify({'error': 'Invalid role'})

        cursor.execute(inning_query, (player_name,))
        inning_data = cursor.fetchone()

        if inning_data:
            if role == 'Batsman':
                inning_info = {
                    f'inning_{i}_runs': inning_data[0],
                    f'inning_{i}_strike_rate': inning_data[1],
                    f'inning_{i}_points': inning_data[2],
                }
            elif role == 'Bowler':
                inning_info = {
                    f'inning_{i}_wickets': inning_data[0],
                    f'inning_{i}_economy_rate': inning_data[1],
                    f'inning_{i}_points': inning_data[2],
                }
            elif role == 'All-Rounder':
                inning_info = {
                    f'inning_{i}_runs': inning_data[0],
                    f'inning_{i}_strike_rate': inning_data[1],
                    f'inning_{i}_wickets': inning_data[2],
                    f'inning_{i}_economy_rate': inning_data[3],
                    f'inning_{i}_points': inning_data[4],
                }

            innings_info.append(inning_info)

    cursor.close()
    print(innings_info)

    return jsonify(innings_info)






if __name__ == '__main__':
    app.run(debug=True)
