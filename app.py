from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, session, Response
from auth import login_user
from referrals import submit_referral, get_user_referrals, upload_referrals_csv, add_referral
from users import create_user, get_user_info
from admin import approve_referral, reject_referral, add_points
import os
from storage import load_json
from config import REFERRALS_FILE
from io import StringIO
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super-secret-key"

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

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    return login_user(data['username'], data['password'])

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

@app.route('/approve_referral', methods=['POST'])
def approve():
    data = request.json
    return approve_referral(data)

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
    data = load_json(REFERRALS_FILE)
    referrals = data.get("referrals", [])

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    filtered = []
    for r in referrals:
        created_str = r.get("created_at", "")
        try:
            created = datetime.strptime(created_str, "%Y-%m-%d")
            if start <= created <= end:
                filtered.append(r)
        except ValueError:
            print(f"Skipping malformed date: {created_str}")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Referral ID", "Referrer", "Name", "Phone", "Email",
        "Status", "Course Interested", "Created At",
        "Converted At", "Admission Amount", "Points Awarded"
    ])

    for r in filtered:
        writer.writerow([
            str(r.get("id", "")),
            str(r.get("referrer", "")),
            str(r.get("name", "")),
            str(r.get("phone", "")),
            str(r.get("email", "")),
            str(r.get("status", "")),
            str(r.get("course_interested", "")),
            str(r.get("created_at", "")),
            str(r.get("converted_at", "")),
            str(r.get("admission_amount", "")),
            str(r.get("points_awarded", ""))
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=referral_report_{start_date}_to_{end_date}.csv"
        }
    )

@app.route('/referrals/admin', methods=['GET'])
def get_all_referrals():
    data = load_json(REFERRALS_FILE)
    return jsonify({"referrals": data.get("referrals", [])})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/submit_referral", methods=["POST"])
def submit_referral_route():
    data = request.get_json()
    return add_referral(data)

if __name__ == '__main__':
    app.run(debug=True)
