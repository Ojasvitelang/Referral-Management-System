from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, session
from auth import login_user
from referrals import submit_referral, get_user_referrals, upload_referrals_csv
from users import create_user, get_user_info
from admin import approve_referral, reject_referral, add_points, generate_report
import os

app = Flask(__name__)
app.secret_key = "super-secret-key"  # 🔐 required for session cookies

# Serve HTML pages from the templates folder
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect(url_for('home'))
    return render_template("dashboard.html")

@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template("admin.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Auth route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    return login_user(data['username'], data['password'])

# User routes
@app.route('/submit_referral', methods=['POST'])
def submit():
    data = request.json
    return submit_referral(data)

@app.route('/referrals/<username>', methods=['GET'])
def referrals(username):
    return get_user_referrals(username)

@app.route('/upload_referrals', methods=['POST'])
def upload_referrals():
    file = request.files['file']
    username = request.form['username']
    return upload_referrals_csv(file, username)

@app.route('/create_user', methods=['POST'])
def create():
    data = request.json
    return create_user(data)

@app.route('/user/<username>', methods=['GET'])
def user_info(username):
    return get_user_info(username)

# Admin routes
@app.route('/approve_referral', methods=['POST'])
def approve():
    data = request.json
    return approve_referral(data['referral_id'], data['admission_amount'])

@app.route('/reject_referral', methods=['POST'])
def reject():
    data = request.json
    return reject_referral(data['referral_id'])

@app.route('/add_points', methods=['POST'])
def add():
    data = request.json
    return add_points(data['username'], data['points'], data['reason'])

@app.route('/generate_report', methods=['GET'])
def report():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    return generate_report(start_date, end_date)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
