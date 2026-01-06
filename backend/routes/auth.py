from flask import Blueprint, jsonify, request
import os
from flask_login import current_user, login_user, logout_user, login_required 
from backend import db, bcrypt
from backend.models.user import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({"message": "You are already logged in"}), 200

    data = request.get_json()
    
 
    if not data or not data.get('username') or not data.get('email') or not data.get('password') or not data.get('fname') or not data.get('lname'):
        return jsonify({"error": "Missing data"}), 400

 
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "This email is already in use"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "This username is already taken"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        fname=data.get('fname', ''), 
        lname=data.get('lname', ''),
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        is_admin=False 
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Account created successfully! Log in now."}), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": "Error during account creation", "details": str(e)}), 500


@auth.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 200

    data = request.get_json()
    identifier = data.get('email') or data.get('username')
    password_recu = data.get('password')

    env_admin_email = os.environ.get('ADMIN_EMAIL')
    env_admin_pass = os.environ.get('ADMIN_PASSWORD')

    if identifier == env_admin_email or identifier == 'Admin':
        
        admin_user = User.query.filter(
            (User.email == env_admin_email) | (User.username == 'Admin')
        ).first()

        if not admin_user:
            hashed_pw = bcrypt.generate_password_hash(env_admin_pass).decode('utf-8')
            admin_user = User(
                username='Admin',
                email=env_admin_email,
                password=hashed_pw,
                fname='Super',
                lname='Admin',
                is_admin=True 
            )
            db.session.add(admin_user)
            db.session.commit()

        if bcrypt.check_password_hash(admin_user.password, password_recu):
            login_user(admin_user, remember=True)
            return jsonify({
                "message": "Admin login successful", 
                "username": "Admin",
                "role": "admin"  
            }), 200
        else:
            return jsonify({"error": "Incorrect Admin password"}), 401

    else: 
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        if user and bcrypt.check_password_hash(user.password, password_recu):
            login_user(user, remember=True)
            return jsonify({
                "message": "Login successful", 
                "username": user.username,
                "role": "user" 
            }), 200
        else:
            return jsonify({"error": "Incorrect email, username or password"}), 401



@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user() 
    return jsonify({"message": "Logout successful"}), 200