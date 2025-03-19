from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "database.db")}'
app.config['SECRET_KEY'] = 'kashish1020'  # Required for session management

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Define the UserProfile model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=True)
    username = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.String(500), nullable=True)
    skills = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<UserProfile {self.user_id}>'

# Create database tables
with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def home():
    # Check if the user is logged in
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('home.html', user=user)
    return render_template('home.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                # Store user ID in session
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                # Redirect to load.html with a success flag
                return redirect(url_for('load', success=True))
            else:
                flash('Invalid password!', 'error')
        else:
            flash('Email does not exist. Please register first.', 'error')
    return render_template('login.html')

# Load Page
@app.route('/load')
def load():
    success = request.args.get('success', False)  # Get the success flag from the URL
    return render_template('load.html', success=success)

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# User Profile Route
@app.route('/user_profile')
def user_profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))

    try:
        # Fetch the logged-in user's data
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('home'))

        # Fetch the user's profile data
        user_profile = UserProfile.query.filter_by(user_id=user.id).first()

        # Log the user and profile data for debugging
        app.logger.debug(f"User: {user}")
        app.logger.debug(f"User Profile: {user_profile}")

        # Render the user profile page with the user's data
        return render_template('userprofile.html', user=user, user_profile=user_profile)
    except Exception as e:
        app.logger.error(f"Error in user_profile route: {e}")
        return "An error occurred while loading the profile page.", 500

# Route to Handle Profile Updates
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to update your profile.'}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    # Get form data
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    bio = request.form.get('bio')
    skills = request.form.get('skills')

    # Fetch or create the user's profile
    user_profile = UserProfile.query.filter_by(user_id=user.id).first()
    if not user_profile:
        user_profile = UserProfile(user_id=user.id)
        db.session.add(user_profile)

    # Update profile data
    user_profile.name = name
    user_profile.username = username
    user_profile.email = email
    user_profile.bio = bio
    user_profile.skills = skills

    db.session.commit()

    # Return a JSON response
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully!',
        'name': name,
        'username': username,
        'email': email,
        'bio': bio,
        'skills': skills,
    })

# Delete Profile Route
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash('Please log in to delete your account.', 'error')
        return redirect(url_for('login'))

    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('home'))

        # Delete the user's profile data first (to avoid foreign key constraint violations)
        UserProfile.query.filter_by(user_id=user_id).delete()
        
        # Now delete the user
        db.session.delete(user)
        db.session.commit()
        
        # Clear the session
        session.clear()
        
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting account: {e}")
        flash('An error occurred while deleting your account.', 'error')
        return redirect(url_for('home'))
    
# Logout Route
@app.route('/logout')
def logout():
    # Remove user ID from session
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)