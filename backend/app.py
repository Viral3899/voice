from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import re
import uuid
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "appointments.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id TEXT PRIMARY KEY,
            user_phone TEXT,
            user_name TEXT,
            date TEXT,
            time TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

app = Flask(__name__)
CORS(app)
init_db()


def extract_entities(text):
    # Very small heuristics for name, phone, date, time
    phone = None
    name = None
    date = None
    time = None

    phone_match = re.search(r"(\+?\d[\d\-\s]{6,}\d)", text)
    if phone_match:
        phone = re.sub(r"[^0-9+]+", "", phone_match.group(1))

    # Name: assume capitalized words of length >1
    name_match = re.search(r"name is ([A-Z][a-z]+(?: [A-Z][a-z]+)*)", text)
    if name_match:
        name = name_match.group(1)

    # Date/time simple patterns
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    if date_match:
        date = date_match.group(1)

    time_match = re.search(r"(\d{1,2}:\d{2})(?:\s*(am|pm))?", text, flags=re.I)
    if time_match:
        time = time_match.group(1)
        ampm = time_match.group(2)
        if ampm:
            time = time + " " + ampm.lower()

    return {"name": name, "phone": phone, "date": date, "time": time}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/identify_user", methods=["POST"])
def identify_user():
    data = request.get_json() or {}
    phone = data.get("phone")
    if not phone:
        return jsonify({"error": "phone required"}), 400
    # For demo, phone is unique id
    user_id = phone
    return jsonify({"user_id": user_id, "phone": phone})


@app.route("/fetch_slots", methods=["GET"])
def fetch_slots():
    # Hardcoded slots for demo
    today = datetime.utcnow().date()
    slots = []
    for i in range(1, 8):
        day = today.replace(day=min(28, today.day + i))
        slots.append({"date": day.isoformat(), "times": ["09:00", "10:00", "14:00", "15:30"]})
    return jsonify({"slots": slots})


@app.route("/book_appointment", methods=["POST"])
def book_appointment():
    data = request.get_json() or {}
    phone = data.get("phone")
    name = data.get("name")
    date = data.get("date")
    time = data.get("time")
    if not (phone and date and time):
        return jsonify({"error": "phone, date, and time are required"}), 400

    conn = get_db()
    c = conn.cursor()
    # Prevent double booking same date+time
    c.execute("SELECT * FROM appointments WHERE date=? AND time=?", (date, time))
    if c.fetchone():
        conn.close()
        return jsonify({"error": "slot already booked"}), 409

    appt_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    c.execute(
        "INSERT INTO appointments (id, user_phone, user_name, date, time, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (appt_id, phone, name, date, time, created_at),
    )
    conn.commit()
    conn.close()
    return jsonify({"id": appt_id, "phone": phone, "name": name, "date": date, "time": time}), 201


@app.route("/retrieve_appointments", methods=["GET"])
def retrieve_appointments():
    phone = request.args.get("phone")
    if not phone:
        return jsonify({"error": "phone required"}), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM appointments WHERE user_phone=? ORDER BY created_at DESC", (phone,))
    rows = c.fetchall()
    conn.close()
    appts = [dict(r) for r in rows]
    return jsonify({"appointments": appts})


@app.route("/cancel_appointment", methods=["POST"])
def cancel_appointment():
    data = request.get_json() or {}
    appt_id = data.get("id")
    if not appt_id:
        return jsonify({"error": "id required"}), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE id=?", (appt_id,))
    conn.commit()
    changed = c.rowcount
    conn.close()
    if changed:
        return jsonify({"status": "cancelled", "id": appt_id})
    return jsonify({"error": "appointment not found"}), 404


@app.route("/modify_appointment", methods=["POST"])
def modify_appointment():
    data = request.get_json() or {}
    appt_id = data.get("id")
    new_date = data.get("date")
    new_time = data.get("time")
    if not appt_id:
        return jsonify({"error": "id required"}), 400
    conn = get_db()
    c = conn.cursor()
    # check collision
    if new_date and new_time:
        c.execute("SELECT * FROM appointments WHERE date=? AND time=? AND id!=?", (new_date, new_time, appt_id))
        if c.fetchone():
            conn.close()
            return jsonify({"error": "slot already booked"}), 409
    # perform update
    if new_date:
        c.execute("UPDATE appointments SET date=? WHERE id=?", (new_date, appt_id))
    if new_time:
        c.execute("UPDATE appointments SET time=? WHERE id=?", (new_time, appt_id))
    conn.commit()
    c.execute("SELECT * FROM appointments WHERE id=?", (appt_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "appointment not found"}), 404


@app.route("/end_conversation", methods=["POST"])
def end_conversation():
    data = request.get_json() or {}
    conversation = data.get("conversation", "")
    # Very small summary: count turns and extract simple entities
    entities = extract_entities(conversation)
    summary = {
        "summary": f"Conversation ended. Extracted name={entities.get('name')} phone={entities.get('phone')}",
        "timestamp": datetime.utcnow().isoformat(),
    }
    return jsonify(summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
