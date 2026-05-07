from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import smtplib
from email.mime.text import MIMEText
import csv

# Gemini
import google.generativeai as genai

# Twilio
from twilio.rest import Client

# Utils
from utils.extract_text import extract_text_from_file
from utils.scoring import (
    score_resume, aggregate_scores,
    save_shortlist_csv, extract_contact_details
)

# ------------------------------
# API KEYS & SERVICES
# ------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")  # e.g., whatsapp:+14155238886

# Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Twilio
client = None
if TWILIO_SID and TWILIO_AUTH:
    client = Client(TWILIO_SID, TWILIO_AUTH)

# Flask
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


# ------------------------------
# CATEGORY DETECTION
# ------------------------------
def detect_category(text, filename):
    txt = (text + " " + filename).lower()

    if any(k in txt for k in ["data analyst", "analytics", "excel", "power bi", "tableau"]):
        return "Data Analytics"

    if any(k in txt for k in ["data engineer", "pipeline", "etl", "big data", "spark"]):
        return "Data Engineering"

    if any(k in txt for k in ["developer", "software", "fullstack", "react", "node"]):
        return "Software Engineering"

    return "Others"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


# ------------------------------
# UPLOAD PAGE – RANK RESUMES
# ------------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        selected_category = request.form.get("category")
        jd = request.form.get("job_description")
        req_skills = request.form.get("required_skills")

        files = request.files.getlist("resumes")
        resumes = []

        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                f.save(path)
                text = extract_text_from_file(path)
                resumes.append({"filename": filename, "text": text})

        results = []

        # Score resumes
        for r in resumes:
            jd_score, skills_score, matched = score_resume(
                r["text"], jd, req_skills
            )

            total = aggregate_scores(jd_score, skills_score)
            category = detect_category(r["text"], r["filename"])
            name, email, phone = extract_contact_details(r["text"])

            results.append({
                "filename": r["filename"],
                "name": name,
                "email": email,
                "phone": phone,
                "jd_score": jd_score,
                "skills_score": skills_score,
                "matched_skills": matched,
                "total_score": total,
                "category": category
            })

        # Filter selected category
        filtered = [r for r in results if r["category"] == selected_category]

        # Sort
        filtered = sorted(filtered, key=lambda x: x["total_score"], reverse=True)

        # Save shortlist for next page
        save_shortlist_csv(filtered, "uploads/latest_shortlist.csv")

        return render_template("dashboard.html",
                               results=filtered,
                               selected_category=selected_category,
                               job_description=jd,
                               required_skills=req_skills)

    return render_template("upload.html")


# ------------------------------
# NEXT PAGE — SORTED RESUMES
# ------------------------------
@app.route("/sorted_resumes")
def sorted_resumes():

    file = "uploads/latest_shortlist.csv"
    rows = []

    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            score = float(r["total_score"])
            r["total_score"] = score
            r["percentage"] = round(score * 100, 1)  # convert to %
            rows.append(r)

    # Filtering
    filter_type = request.args.get("filter", "none")

    if filter_type == "under70":
        rows = [r for r in rows if r["percentage"] < 70]

    elif filter_type == "under80":
        rows = [r for r in rows if r["percentage"] < 80]

    elif filter_type == "above80":
        rows = [r for r in rows if r["percentage"] >= 80]

    elif filter_type == "above90":
        rows = [r for r in rows if r["percentage"] >= 90]

    # Sort again
    rows = sorted(rows, key=lambda x: x["percentage"], reverse=True)

    return render_template("sorted_resumes.html", data=rows, filter=filter_type)


# ------------------------------
# SEND MESSAGE
# ------------------------------
@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")

    # Load shortlist CSV
    rows = []
    with open("uploads/latest_shortlist.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    # Email
    if EMAIL_USER and EMAIL_PASS:
        print(f"Attempting to send email from {EMAIL_USER}...")
        for r in rows:
            if r["email"] != "Not Found":
                try:
                    msg = MIMEText(message)
                    msg["Subject"] = "Shortlisted Notification"
                    msg["From"] = EMAIL_USER
                    msg["To"] = r["email"]

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(EMAIL_USER, EMAIL_PASS)
                        server.sendmail(EMAIL_USER, r["email"], msg.as_string())
                    print(f"Email sent to {r['email']}")
                except Exception as e:
                    print(f"Failed to send email to {r['email']}: {e}")
            else:
                print(f"Skipping {r['name']} (No email found)")
    else:
        print("EMAIL_USER or EMAIL_PASS not set. Skipping email sending.")

    # WhatsApp (Twilio)
    if client:
        for r in rows:
            if r["phone"] != "Not Found":
                try:
                    client.messages.create(
                        from_=TWILIO_NUMBER,
                        to=f"whatsapp:{r['phone']}",
                        body=message
                    )
                except:
                    pass

    return render_template("message_sent.html", msg=message)


@app.route("/download_latest")
def download_latest():
    return send_file("uploads/latest_shortlist.csv", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
